# Base Image.
FROM python:3.6

# Create and set working directory.
RUN mkdir /app
WORKDIR /app

# Add current directory code to working directory.
ADD . /app/

# Set default environment variables.
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive 

# Set project environment variables
# grab these via Python's os.environ
# these are 100% optional here.
ENV PORT=8000
# ENV DEBUG=0  # For production

# Install system dependencies.
RUN apt-get update && apt-get install -y --no-install-recommends \
        tzdata \
        python3-setuptools \
        python3-pip \
        python3-dev \
        python3-venv \
        git \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# Install environment dependencies.
RUN pip3 install --upgrade pip 
RUN pip3 install pipenv

# Install project dependencies.
RUN pipenv install --skip-lock --system --dev

EXPOSE 8000
CMD waitress-serve --listen=*:$PORT supervisio.wsgi:application
# CMD gunicorn cfehome.wsgi:application --bind 0.0.0.0:$PORT  # For unix