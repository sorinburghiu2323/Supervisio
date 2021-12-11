# Supervisio

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 📖 About

2021/2022 Dissertation: Content-based recommender system to augment the project selection process

## 🛠️ Setup

First set up your python virtual environment.
```
python -m venv .venv
```

Then activate it with:
```
.venv\Scripts\activate.bat      # Windows
.venv\bin\activate              # Linux
```

Install python dependencies:
```
pip install -r requirements-base.txt
```

Set app development as True when developing:
```
SET APP_DEVELOPMENT=True         # Windows
export APP_DEVELOPMENT=True      # Linux
```

Do your migrations (create your development database):
```
python manage.py migrate
```

Run the django server using:
```
python manage.py runserver
```
