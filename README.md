# TMC Data Management

## Dependencies

### System packages

The system packages below are required to be installed in Fedora 37+:

- gammu-devel
- nginx
- postgis-llvmjit
- postgresql-llvmjit
- python3-devel
- python3-virtualenvwrapper
- rabbitmq-server

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

### Set-up RabbitMQ Message Broker

```bash
sudo rabbitmqctl add_user myuser mypassword
sudo rabbitmqctl add_vhost myvhost
sudo rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"
```

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

### Set-up gammu

You will need to have `~/gammu-smsdrc` set-up with something like for your testing environment:

```
[gammu]
connection = bluephonet
device = 00:00:00:00:00:00 # Your phone MAC bluetooth MAC address
logformat = textall

[smsd]
commtimeout = 30
debuglevel = 0
hangupcalls = 1
logfile = $HOME/gammu.log # You need to substitue your absolute $HOME
maxretries = 100
phoneid = the_phone
pin = 1234
receivefrequency = 15
retrytimeout = 600
sendtimeout = 30
service = NULL

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
export DATA_MANAGEMENT_MEDIA_ROOT=where_your_media_root_is
export DATA_MANAGEMENT_MEDIA_URL=where_your_media_root_or_url_is
# Variables below should be the same in datamanagement/local.py
export DJANGO_SUPERUSER_USERNAME=username
export DJANGO_SUPERUSER_PASSWORD=password
export DJANGO_SUPERUSER_EMAIL=sample.email@domain.com
```

When all environment variables in `~/.bashrc` and variables in `data_management/local.py` are set properly,
uploading the exported production data and migrating (testing) your changes is done using the commands below:

```
# export the production files
./scripts/export_data.sh

# set-up an empty database with all models fully migrated
./scripts/clean_db.sh

# upload the production data into your development environment
./scripts/upload_data.sh

# run you development instance
./manage.py runserver
```
