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

### Next install the VueJS frontend dependencies:

```shell script
cd frontend
npm install
```
Note: When you pull changes that others have made, you may want to do `npm install` again to ensure any additional dependencies have been added.

Now to build the frontend, there are two ways:

Watches for any changes in the filetree and recompiles when detects a change.
```
npm run watch
```

Compiles and minifies for production.
```
npm run build
```

### Using Docker (these instructions are for Windows only):

Create `.env` file with one line saying `DEBUG=1`.

Install pipenv environment:
```
pipenv install
```

Build docker image.
```
docker build -t supervisio -f Dockerfile .
```

Run container.
```
docker run -it -p 80:8000 supervisio   
```

Since we used port `80`, access `http://localhost/` to view the project.
