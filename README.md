# PasswordManager-Django
## Overview
The Password Manager is a Django-based web application designed to securely manage and store your passwords. It allows users to create, retrieve, and manage credentials in an organized and secure manner, leveraging Django’s robust framework to ensure data security.

## Features
User Authentication: Secure login and registration system to protect your data.

Password Storage: Save and organize multiple credentials under a single user account.

Encryption: Uses Django's security features to encrypt sensitive data.

User-Friendly Interface: Clean and intuitive design for ease of use.

CRUD Operations: Create, read, update, and delete saved credentials.

Secure Backend: Implements Django's built-in security features to prevent vulnerabilities like SQL injection and CSRF attacks.

## Installation
### Prerequisites
1. Python 3.8+

2. Django 4.0+

3. SQLite (default database for Django)

#### Steps
Clone the repository:
```
git clone https://github.com/ArnavTamrakar/PasswordManager-Django.git
cd PasswordManager-Django
```
Set up a virtual environment:
```
python -m venv env
source env/bin/activate   # For Linux/Mac
env\Scripts\activate     # For Windows
```

Install dependencies:
```
pip install -r requirements.txt
```

Apply migrations:
```
python manage.py migrate
```

Run the development server:
```
python manage.py runserver
```
Access the application at: http://127.0.0.1:8000

## Usage
Register or log in to your account.

Add a new password by providing details like website name, username, and password.

Manage your saved passwords by editing or deleting them.

## Project Structure
```
PasswordManager-Django/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── password_manager/      # Main application
│   ├── migrations/
│   ├── templates/
│   ├── views.py
│   ├── models.py
│   ├── urls.py
│   └── admin.py
└── static/               # Static files
```
