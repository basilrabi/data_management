# TMC Data Management

## Dependencies

### System packages

The system packages below are required to be installed in Fedora 33+:

- nginx
- postgis-llvmjit
- postgresql-llvmjit
- python3
- python3-virtualenvwrapper

System packages are installed using `dnf`:

```bash
sudo dnf install nginx
```

### R packages

There are also R packages needed for development:

1. DBI
1. RPostgres
1. dplyr

Ensure that the database connection is properly set-up as required in
`data_management.settings.DATABASES`

## Deployment and Development

### Set-up virtual environment

Add the following lines in your `.bashrc`

```bash
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export VIRTUALENVWRAPPER_VIRTUALENV_ARGS=' -p /usr/bin/python3 '
export PROJECT_HOME=$HOME/Devel
source /usr/bin/virtualenvwrapper.sh # if installed via system
source /usr/local/bin/virtualenvwrapper.sh # if installed via pip
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
git clone http://datamanagement.tmc.nickelasia.com:3000/ORMM/data_management.git
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

Edit your database connection variables and django superuser credentials (if
you will use the automated bash scripts) in `data_management/local.py`.

Set-up the django project

```bash
./manage.py migrate
./manage.py collecstatic
./manage.py createsuperuser
```

### Development Environment

To ensure that your local changes work fine with the data presently in the production server, it is recommended to export and use the actual data from production.
You can export the data by running the script `./scripts/export_data.sh`, however, you need to put the password of the psql user `developer` in `~/.pgpass`.

Password-less psql shell will not work if `~/.pgpass` is not configured correctly.
A sample configuration is shown below.
Also, the file mode should be `600`.
This can be done by running `chmod 600 ~/.pgpass`

```
# ~/.pgpass
#hostname:port:database:username:password
*:*:*:developer:get_password_from_brabi
```

In running your own instance of the website, the environment variables below must be set:

```bash
# ~/.bashrc
export DATA_MANAGEMENT_DB_HOST=datamanagement.tmc.nickelasia.com
export DATA_MANAGEMENT_DB_NAME=data_management_db_name
export DATA_MANAGEMENT_DB_USER=data_management_user
export DATA_MANAGEMENT_DB_PASSWORD=data_management_password
export DATA_MANAGEMENT_DB_PORT=5432
export DATA_MANAGEMENT_GEOLOGY=geology_password
export DATA_MANAGEMENT_GRADECONTROL=gradecontrol_password
export DATA_MANAGEMENT_PLANNING=planning_password
export DATA_MANAGEMENT_READER=reader_password
export DATA_MANAGEMENT_SURVEY=survey_password
# Variables below should be the same in datamanagement/local.py
export DJANGO_SUPERUSER_USERNAME=username
export DJANGO_SUPERUSER_PASSWORD=password
export DJANGO_SUPERUSER_EMAIL=sample.email@domain.com
```

### Serving

#### Fedora 33+

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
