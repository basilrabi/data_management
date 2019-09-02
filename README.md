# TMC Data Management

## Dependencies

The packages below are required to be installed:

- python3 (>= 3.5.3)
- python3-pip
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
git clone http://192.169.101.20:3000/brabi/data_management.git
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
