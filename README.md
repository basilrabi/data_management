# TMC Data Management

## Dependencies

The packages below are required to be installed:

- nginx
- python3 (>= 3.5.3)
- python3-virtualenvwrapper (via package or pip)

Ensure that the database connection is properly set-up as required in
`data_management.settings.DATABASES`

## Deployment

### Set-up virtual environment

Add the following lines in your `.bashrc`

```bash
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export VIRTUALENVWRAPPER_VIRTUALENV_ARGS=' -p /usr/bin/python3 '
export PROJECT_HOME=$HOME/Devel
source /usr/local/bin/virtualenvwrapper.sh # for debian-like
source /usr/bin/virtualenvwrapper.sh       # for fedora
```

Then reload the file:

```bash
source ~/.bashrc
```

Create the virtual environment:

```bash
mkvirtualenv data_management
deactivate
```

### Initial set-up

Clone the source code:

```bash
cd
git clone http://tmc:3000/basilrabi/data_management.git
```

Install the requirements:

```bash
cd ~/data_management
workon data_management
pip3 install -r requirements.txt
```

Set-up your local settings

```bash
cp data_management/local.py.sample data_management/local.py
```

Edit your databse connection variables in `data_management/local.py`.

Set-up the django project

```bash
./manage.py migrate
./manage.py collecstatic
./manage.py createsuperuser
```

### Serving

#### Raspbian (or Debian-like)

Add the following files in your system:

```config
# /etc/systemd/system/data_management.socket
[Unit]
Description=gunicorn data_management app socket

[Socket]
ListenStream=/run/data_management.sock

[Install]
WantedBy=sockets.target
```

```config
# /etc/systemd/system/data_management.service
# Change $USER to your user name
[Unit]
Description=gunicorn data_management app daemon
Requires=data_management.socket
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=/home/$USER/data_management
ExecStart=/home/$USER/.virtualenvs/data_management/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/data_management.sock \
          data_management.wsgi:application

[Install]
WantedBy=multi-user.target
```

Enable gunicorn data_management app socket:

```bash
sudo systemctl start data_management.socket
sudo systemctl enable data_management.socket
```

Add nginx configuration file:

```config
# /etc/nginx/sites-available/data_management
# Change $HOSTNAME to your server's IP or hostname
# Change $USER to your user name

server {
    listen 82;
    server_name $HOSTNAME;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/$USER/data_management;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/data_management.sock;
    }
}
```

Then link the configuration file:

```bash
sudo ln -s /etc/nginx/sites-available/data_management /etc/nginx/sites-enabled/data_management
```

Lastly, restart your system.

#### Fedora 31

##### Service File

Add the following files in your system:

```config
# /etc/systemd/system/data_management.service
# Change $USER to your user name
[Unit]
Description=Data Management Website daemon
After=network.target

[Service]
User=$USER
Group=nginx
WorkingDirectory=/home/$USER/data_management
ExecStart=/home/$USER/.virtualenvs/data_management/bin/gunicorn --workers 3 --bind unix:/home/$USER/data_management/data_management.sock data_management.wsgi:application

[Install]
WantedBy=multi-user.target
```

##### SELinux Adventures

If you want SELinux activated, running the service might fail since SELinux will prevent a lot of things.
To have a local policy, run:

```bash
setsebool -P domain_can_mmap_files 1 # TODO: might not be needed in F32
setsebool -P httpd_read_user_content 1
setenforce 0
systemctl start data_management
systemctl restart data_management
grep gunicorn /var/log/audit/audit.log | audit2allow -M mydatamanagement
semodule -i mydatamanagement.pp
setenforce 1
systemctl enable data_management
```

See <https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/6/html/security-enhanced_linux/sect-security-enhanced_linux-fixing_problems-allowing_access_audit2allow>
for further clarification of SELinux.

##### NGINX

Configure nginx to proxy pass to gunicorn by adding a new `server` block to `/etc/nginx/nginx.conf`:

```config
# Change $USER to your user name
server {
    listen 80;
    server_name server_domain_or_IP;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/$USER/data_management;
    }

    location / {
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://unix:/home/$USER/data_management/data_management.sock;
    }
}
```

After the configuration file, run the following:

```bash
# Add your account to the group `nginx` so it will be able to access your
# directory. Change $USER to your user name
usermod -a -G $USER nginx
systemctl start nginx
systemctl enable nginx
```

Again, because of SELinux, nginx will not be able to write on the unix socket.
See <https://stackoverflow.com/questions/23948527/13-permission-denied-while-connecting-to-upstreamnginx>.
Fix this by running the following:

```bash
setsebool -P httpd_can_network_connect 1 # TODO: might not be needed
grep nginx /var/log/audit/audit.log | audit2allow -M mynginx
semodule -i mynginx.pp
systemctl restart data_management
systemctl restart nginx
```

##### PostgreSQL

Due to SELinux again, gunicorn would not be able to connect to the postgres database.

```bash
grep postgres /var/log/audit/audit.log | audit2allow -M db
semodule -i db.pp
```
