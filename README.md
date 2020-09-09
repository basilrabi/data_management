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
git clone http://datamanagement.tmc.nickelasia.com:3000/basilrabi/data_management.git
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

Edit your databse connection variables and django superuser credentials (if
you will use the automated bash scripts) in `data_management/local.py`.

Set-up the django project

```bash
./manage.py migrate
./manage.py collecstatic
./manage.py createsuperuser
```

### Serving

#### Fedora 32

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
EnvironmentFile=/pathto/somefilewith_secrets
WorkingDirectory=/home/$USER/data_management
ExecStart=/home/$USER/.virtualenvs/data_management/bin/gunicorn --workers 3 --timeout 6000 --bind unix:/home/$USER/data_management/data_management.sock data_management.wsgi:application

[Install]
WantedBy=multi-user.target
```

##### SELinux Adventures

If you want SELinux activated, running the service might fail since SELinux will prevent a lot of things.
You may [compile](https://relativkreativ.at/articles/how-to-compile-a-selinux-policy-package) the type enforcement files in the `SELinux/` directory.

See [this](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/6/html/security-enhanced_linux/sect-security-enhanced_linux-fixing_problems-allowing_access_audit2allow)
for further clarification of SELinux.

##### NGINX

Configure nginx to proxy pass to gunicorn by adding a new `server` block to `/etc/nginx/nginx.conf`:

```config
# Change $USER to your user name
server {
    listen 80;
    server_name $SERVER_DOMAIN_OR_IP;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/$USER/data_management;
    }

    location / {
        client_body_temp_path /home/$USER/client_body_temp 1 2;
        proxy_temp_path /home/$USER/tmp 1 2;
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://unix:/home/$USER/data_management/data_management.sock;
    }
}

server {
    listen 81;
    server_name $SERVER_DOMAIN_OR_IP;
    location = /favicon.ico { access_log off; log_not_found off; }
    location / {
        root /media/tmc/nginx/81;
        index index.html;
        autoindex on;
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
