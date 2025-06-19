# PasswordManager-Django
## Overview
The Password Manager is a Django-based web application designed to securely manage and store your passwords. It allows users to create, retrieve, and manage credentials in an organized and secure manner, leveraging Django’s robust framework to ensure data security.

## Features
- User authentication (sign up, log in, log out)
- Email verification with code on login
- Secure password storage (encrypted with Fernet)
- Add, update, and delete saved passwords
- Automatic favicon fetching for each website
- Responsive, modern UI (Bootstrap 5)
- Copy to clipboard for email and password
- Show/hide password toggle
- User-specific data (each user sees only their own passwords)

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
