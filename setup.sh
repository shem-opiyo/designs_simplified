#!/usr/bin/env bash
clear 
# create a virtual environment for the project
echo  "==================> Creating a virtual environment for the project"
pip install virtualenv && \

# create a virtual environment for the project
sudo virtualenv -p python3 server/.venv && \

# activate the virtual environment
echo  "==================> Activating the virtual environment"
source server/.venv/bin/activate && \



pip install -r server/requirements.txt  && \


# grant nginx user permission to access the static files and media files 

echo   "==================> Granting  nginx user permission to access the static files and media files"


# grating the  home user permmissions to read and  execute 

namei -om /home/shem/projects/django/shem/server/static 
# grant the www-data user permission to execute  files from the home directory

echo  "==================> Granting the www-data user permission to execute files from the home directory"



sudo chown shem:www-data /home/shem    
sudo  chmod g+x  /home/shem   



# setting gunicorn reload the server when the code changes
echo  "==================> Setting gunicorn to reload the server when the code changes"
sudo  touch /etc/systemd/system/shem.service & \

sudo bash -c 'echo -e  "[Unit]\n\
Description=shem Interiors  \n\
After=network.target \n \

[Service]  \n \
User=www-data  \n \
Group=www-data  \n \
WorkingDirectory=$PWD/server/  \n \
Environment=\"PATH=$PWD/server/.venv/bin\" \n \

ExecStart=$PWD/server/.venv/bin/gunicorn --workers 3  --bind  0.0.0.0:8001 -m 007 wsgi:app  --log-level info --log-file ./shem.log  --reload  


[Install] \n  \
WantedBy=multi-user.target \n "  > /etc/systemd/system/shem.service ' &&   \

#set script to break if any command fails


echo  "==================> Systemd service file created"


# reload the systemd daemon
sudo systemctl daemon-reload  && \

echo  "==================> Systemd daemon reloaded"

sudo systemctl start shem  && \

echo  "==================> shem Interiors service started"

# sudo systemctl enable shem




