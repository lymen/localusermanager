## Prerequisites:
- Install Apache
    ```>> sudo apt update```
    ```>> sudo apt install apache2```
    ```>> sudo ufw allow "Apache Full"```

- Clone repo to ```/var/www/localusermanager/```

## Steps:
#### Prepare Environment
1. Install python
    ```>> sudo apt-get install python-pip python-virtualenv python-setuptools python-dev build-essential  python3.8```
  
2. Create virtualenv on the root directory of this repo (/var/www/localusermanager/)
    ```>> virtualenv -p python3 localusermanagerenv```
   
3. Start virtualenv
    ```>> source localusermanagerenv/bin/activate```
   
4. Install needed requirements
    ```>> pip install django```
    ```>> pip install -r requirements.txt```

5. Run the django server
    ```>> python manage.py runserver ```
    Starting development server at ```http://127.0.0.1:8000/``` <-- user this link to access the web site

6. Add your Linux Server IP or domain name for the allowed hosts
    - Open ```/var/www/localusermanager/settings.py```
    - Add your domain or ip address in the ``ALLOWED_HOSTS`` section.
    
7. Collect static
    ```>> python manage.py collectstatic```

#### Host using Apache

1. Modify file ```/etc/apache2/sites-available/000-default.conf```
```
<VirtualHost *:80>
	ServerName http://domainname.com/ #Input domain name if it exists
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
    ```>> sudo a2ensite 000-default.conf```
    ```>> sudo a2enmod rewrite```
    ```>> sudo systemctl restart apache2.service```

3. Test website access by visiting the domain name or Linux Server IP


#### Certify using self signed certificate
Reference: https://www.digitalocean.com/community/tutorials/how-to-create-a-self-signed-ssl-certificate-for-apache-in-ubuntu-16-04

1. Create SSL Certificate
    ```>> sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/apache-selfsigned.key -out /etc/ssl/certs/apache-selfsigned.crt```

    Fill out the proper information especially the ```Common Name (e.g. server FQDN or YOUR name) []:server_IP_address```. Input here the domain name or the IP address of the server.
    
2. Create a DH group
    ```>> sudo openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048```

3. Configure Apache to Use SSL
    Create a new snippet in the ```/etc/apache2/cpnf-available``` directory:

    ```>> sudo nano /etc/apache2/conf-available/ssl-params.conf```
    ```
    # from https://cipherli.st/
    # and https://raymii.org/s/tutorials/Strong_SSL_Security_On_Apache2.html
    
    SSLCipherSuite EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH
    SSLProtocol All -SSLv2 -SSLv3
    SSLHonorCipherOrder On
    # Disable preloading HSTS for now.  You can use the commented out header line that includes
    # the "preload" directive if you understand the implications.
    #Header always set Strict-Transport-Security "max-age=63072000; includeSubdomains; preload"
    Header always set Strict-Transport-Security "max-age=63072000; includeSubdomains"
    Header always set X-Frame-Options DENY
    Header always set X-Content-Type-Options nosniff
    # Requires Apache >= 2.4
    SSLCompression off
    SSLSessionTickets Off
    SSLUseStapling on
    SSLStaplingCache "shmcb:logs/stapling-cache(150000)"
    
    SSLOpenSSLConfCmd DHParameters "/etc/ssl/certs/dhparam.pem"
    ```
    Save and close.
    
4. Modify the Default Apache SSL Virtual Host File
    ```>> sudo cp /etc/apache2/sites-available/default-ssl.conf /etc/apache2/sites-available/default-ssl.conf.bak```
    ```>> sudo nano /etc/apache2/sites-available/default-ssl.conf```

    ```
    <IfModule mod_ssl.c>
    	<VirtualHost _default_:443>
    		ServerAdmin webmaster@localhost
            ServerName http://domainname.com/ #Input domain name if it exists
            
    		DocumentRoot /var/www/localusermanager/
    
    		ErrorLog /var/www/localusermanager/logs/error.log
    		CustomLog /var/www/localusermanager/logs/access.log combined
    
    		SSLEngine on
    
    		SSLCertificateFile	/etc/ssl/certs/apache-selfsigned.crt
    		SSLCertificateKeyFile /etc/ssl/private/apache-selfsigned.key
    
    		Alias /static /var/www/localusermanager/static/
    		
    		<FilesMatch "\.(cgi|shtml|phtml|php)$">
    				SSLOptions +StdEnvVars
    		</FilesMatch>
    		<Directory /usr/lib/cgi-bin>
    				SSLOptions +StdEnvVars
    		</Directory>
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
    
    		BrowserMatch "MSIE [2-6]" \
                                   nokeepalive ssl-unclean-shutdown \
                                   downgrade-1.0 force-response-1.0
    
    	</VirtualHost>
    </IfModule>
    
    # vim: syntax=apache ts=4 sw=4 sts=4 sr noet
    ```
    Save and close.
    
5. Modify the Unencrypted Virtual Host File to Redirect to HTTPS
    ```>> sudo nano /etc/apache2/sites-available/000-default.conf```

    ```
    <VirtualHost *:80>
    	#ServerAdmin webmaster@localhost
    	Redirect "/" "https://domainname_or_ip_address.com/" #Input domain name or ipaddress here
    	ServerName http://domainname.com/ #Input domain name if it exists
    
    	DocumentRoot /var/www/localusermanager/
    
    	ErrorLog /var/www/localusermanager/logs/error.log
    	CustomLog /var/www/localusermanager/logs/access.log combined
    
    	Alias /static /var/www/localusermanager/static/
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
    
    	#WSGIDaemonProcess localusermanager user=lymen python-path=/var/www/localusermanager python-home=/var/www/localusermanager/localusermanagerenv
    	#WSGIProcessGroup localusermanager
    	#WSGIScriptAlias / /var/www/localusermanager/localusermanager/wsgi.py
    
    </VirtualHost>
    
    # vim: syntax=apache ts=4 sw=4 sts=4 sr noet
    ```
    Save and close.
    
6. Adjust the firewall
    ```>> sudo ufw allow 'Apache Full'```
    ```>> sudo ufw delete allow 'Apache'```

7. Enable the Changes in Apache
	```>> sudo a2enmod ssl```
	```>> sudo a2enmod headers```
	```>> sudo a2ensite default-ssl```
	```>> sudo a2enconf ssl-params```
	```>> sudo apache2ctl configtest```
	```>> sudo systemctl restart apache2```

8. Test by using ```https://domainname_or_ip_address.com/```


Links:

    *http://domainname/superadmin <-- to access the superadmin page

    *http://domainname/user <-- to access the user page

    *http://domainname/ <-- to access the object page

