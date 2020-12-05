## Prerequisites:
Apache installed

Clone repo to ```/var/www/localusermanager/```

## Steps:
**Prepare Environment**
1. Install python
 
    ```sudo apt-get install python-pip python-virtualenv python-setuptools python-dev build-essential  python3.8```
  
 2. Create virtualenv on the root directory of this repo
 
    ```virtualenv -p python3 localusermanagerenv```
   
 3. Start virtualenv
 
    ```source localusermanagerenv/bin/activate```
   
 4. Install needed requirements
 
    ```pip install django```
    
    ```pip install -r requirements.txt```
    
  5. Run the django server

    ```python manage.py runserver```

    Starting development server at ```http://127.0.0.1:8000/``` <-- user this link to access the web site

  6. Add your Linux Server IP or domain name for the allowed hosts
   - Open ```/var/www/localusermanager/settings.py```
   - Add your domain or ip address in the ``ALLOWED_HOSTS`` section.
    



**Host using Apache**

1. Modify file ```/etc/apache2/sites-available/000-default.conf```

```
<VirtualHost *:80>
	#ServerAdmin webmaster@localhost
	DocumentRoot /var/www/localusermanager/

	ErrorLog /var/www/localusermanager/logs/error.log
	CustomLog /var/www/localusermanager/logs/access.log combined

	Alias /static /localusermanager/static/
	<Directory /var/www/localusermanager/static/>
		Require all granted
		Options Indexes FollowSymLinks
		AllowOverride All
	</Directory>

	<Directory /var/www/localusermanager/localusermanager/>
		<Files wsgi.py>
			Require all granted
		</Files>
	</Directory>

	WSGIDaemonProcess localusermanager python-path=/var/www/localusermanager python-home=/var/www/localusermanager/localusermanagerenv
	WSGIProcessGroup localusermanager
	WSGIScriptAlias / /var/www/localusermanager/localusermanager/wsgi.py
</VirtualHost>
```

2. Enable new conf then restart apache

    ```sudo a2ensite 000-default.conf```

    ```sudo a2enmod rewrite```

    ```sudo systemctl restart apache2.service```

3. Test website access by visiting the domain name or Linux Server IP


**Certify using self signed certificate**
1. ```sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/apache-selfsigned.key -out /etc/ssl/certs/apache-selfsigned.crt```


Links:

    *http://domainname/superadmin <-- to access the superadmin page

    *http://domainname/user <-- to access the user page

    *http://domainname/ <-- to access the object page

