# TMC Data Management

## Dependencies

The packages below are required to be installed:

- nginx
- python3 (>= 3.8.5)
- python3-virtualenvwrapper (via package or pip)

Ensure that the database connection is properly set-up as required in
`data_management.settings.DATABASES`

## Deployment

### Set-up virtual environment

This step might not be needed in Fedora 32+.
TODO: confirm in the next fresh installation of F33.

Anyway, add the following lines in your `.bashrc`

```bash
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export VIRTUALENVWRAPPER_VIRTUALENV_ARGS=' -p /usr/bin/python3 '
export PROJECT_HOME=$HOME/Devel
source /usr/bin/virtualenvwrapper.sh
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

#### Fedora 33

See [server_conf](http://datamanagement.tmc.nickelasia.com:3000/basilrabi/server_conf) for:

1. `/etc/nginx/nginx.conf`
1. `/etc/systemd/system/data_management.service`
1. `~/.gunicorn_env`


##### SELinux Adventures

If you want SELinux activated, running the service might fail since SELinux will prevent a lot of things.
You may [compile](https://relativkreativ.at/articles/how-to-compile-a-selinux-policy-package) the type enforcement files in the `SELinux/` directory from [here](http://datamanagement.tmc.nickelasia.com:3000/basilrabi/server_conf).

See [this](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/6/html/security-enhanced_linux/sect-security-enhanced_linux-fixing_problems-allowing_access_audit2allow)
for further clarification of SELinux.

##### NGINX

After the configuration file, run the following:

```bash
# Add your account to the group `nginx` so it will be able to access your
# directory. Change $USER to your user name
usermod -a -G $USER nginx
systemctl start nginx
systemctl enable nginx
```
