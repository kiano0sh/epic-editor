**Requirements:**

```
python=3.5+
Django==2.1.5
Pillow==5.4.1
django-materializecss-form==1.1.11

```


**Installation guide:**

```
Note: Assumed that you're in the . directory.

.
└── epic_editor
    ├── accounts
    ├── epic
    ├── main
    ├── manage.py
    ├── requirements.txt
    ├── static
    └── templates


Step 1: pip install virtualenv
Step 2: cd epic_editor
Step 3: python -m venv venv
Step 4:
Windows:
venv\Scripts\activate
Linux:
source ./venv/bin/activate
Step 5: pip install -r requirements.txt
Step 6: python manage.py migrate
Step 7: python manage.py makemigrations main
Step 8: python manage.py migrate
Step 9: python manage.py runserver

All Done!
```

If you need to create a superuser (admin user) run the code below in the root directory of the project and enter the require information:

```
python manage.py createsuperuser
```