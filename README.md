**WHAT'S THAT**
Basically this is a store app with fallowing main functionalities:
- shop page
- registering new users
- taking orders
- payment processing (using Stripe)
- sending confirmation email
- showing order history for a registered user


**TECHNOLOGIES**
This project was developed using Python 3.6.
Packages used in development:
- Django 2.1
- Pillow 5.2.0
- stripe 2.5.0
- django-crispy-forms 1.7.2


**SETUP**
To get this working on your local machine you need to:
1. Download the repository.
2. Using the teminal go to the main directory of the project and use fallowing commands:
- `source ./virtualenv/bin/activate`
- `python ./ecommerce/manage.py runserver`
3. Then you can access the site using your web browser on http://127.0.0.1:8000/
4. At the end to leave the virtual environment use `deactivate` command in your terminal.


**ADMIN PAGE**
To access the admin page go to http://127.0.0.1:8000/admin/ and use fallowing credentials:
- login: admin
- password: admin

You can edit products and categories there as well as add a new one or change the available stock. 
 
 
Of course this is not a ready to deploy store but rather a training project to get some knowladge about Django 2 framework.
Anyway thank you for taking your time to take a look.
