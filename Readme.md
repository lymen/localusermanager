Steps:

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
   
    python manage.py runserver
    
    
    Starting development server at http://127.0.0.1:8000/``` <-- user this link to access the web site
    
Links:

*http://127.0.0.1:8000/superadmin <-- to access the superadmin page

*http://127.0.0.1:8000/user <-- to access the user page

*http://127.0.0.1:8000/ <-- to access the object page
