# Employee task
===============
0. Update python to 3.10 ::

	sudo add-apt-repository ppa:deadsnakes/ppa
	sudo apt update
	sudo apt install python3.10 python3-pip 
	sudo apt install python3.10-venv python3.10-dev libpq-dev postgresql postgresql-contrib nginx curl 

1. Clone repository ::

	git clone https://github.com/Atomnory/wallcrafttask-employee.git sources/Django/WallCraftTask

2. Create .venv ::

    python3.10 -m venv sources/Django/WallCraftTask/.venv

3. Activate venv with ::

	. sources/Django/WallCraftTask/.venv/bin/activate
	python3.10 -m pip install --upgrade pip

4. Install dependencies ::

	pip install -r sources/Django/WallCraftTaskrequirements.txt
	deactivate

5. Start postgresql service ::

	sudo service postgresql start

6. Create db to app ::

	sudo -u postgres psql

	CREATE DATABASE wallcrafttask;
	CREATE USER <username> WITH PASSWORD '<password>';
	ALTER ROLE <username> SET client_encoding TO 'utf8';
	ALTER ROLE <username> SET default_transaction_isolation TO 'read committed';
	ALTER ROLE <username> SET timezone TO 'UTC';
	GRANT ALL PRIVILEGES ON DATABASE wallcrafttask TO <username>;
	\q

7. Change variables in conf.py file ::

	WALLCRAFT_TASK_SECRET_KEY="<secret_key>"
	DB_POSTGRES_WALLCRAFT_NAME='wallcrafttask'
	DB_POSTGRES_USER='<username>'
	DB_POSTGRES_USER_PASSWORD='<password>'
	DB_POSTGRES_HOST='127.0.0.1'
	DB_POSTGRES_PORT='5432'

9. Activate venv with ::

	cd sources/Django/WallCraftTask
	. .venv/bin/activate

10. Migrate app database ::

	python manage.py migrate

11. Create super user ::

	python manage.py createsuperuser

12. Test gunicorn ::

	gunicorn --bind 0.0.0.0:8000 config.wsgi
	deactivate

13. Creating socket and systems files for Gunicorn ::

	sudo vim /etc/systemd/system/gunicorn.socket

   Inside ::

    [Unit]
    Description=gunicorn socket

    [Socket]
    ListenStream=/run/gunicorn.sock

    [Install]
    WantedBy=sockets.target

   Create service ::

	sudo vim /etc/systemd/system/gunicorn.service

   Inside ::

    [Unit]
    Description=gunicorn daemon
    Requires=gunicorn.socket
    After=network.target

    [Service]
    User=<os_username>
    WorkingDirectory=<home_path>/sources/Django/WallCraftTask
    ExecStart=<home_path>/sources/Django/WallCraftTask/.venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock config.wsgi:application

    [Install]
    WantedBy=multi-user.target

14. Start and actvate socket ::

	sudo systemctl start gunicorn.socket
	sudo systemctl enable gunicorn.socket

   Test ::

	sudo systemctl status gunicorn.socket
	file /run/gunicorn.sock -> /run/gunicorn.sock: socket

15. Test and activate socket ::

	sudo systemctl status gunicorn
	curl --unix-socket /run/gunicorn.sock localhost

16. SetUp Nginx as proxy ::

	sudo vim /etc/nginx/sites-available/config

   Inside ::

    server {
        listen 80;
        server_name 0.0.0.0;

        location = /favicon.ico { access_log off; log_not_found off; }
        location /staticfiles/ {
            root <home_path>/<path to folder has manage.py>;
        }

        location / {
            include proxy_params;
            proxy_pass http://unix:/run/gunicorn.sock;
        }
    }

   Create link and restart nginx ::
	sudo ln -s /etc/nginx/sites-available/config /etc/nginx/sites-enabled
	sudo nginx -t
	sudo systemctl restart nginx


Restarts ::

sudo systemctl daemon-reload
sudo systemctl restart gunicorn
sudo systemctl restart nginx
