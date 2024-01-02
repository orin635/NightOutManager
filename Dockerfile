##
## Dockerfile to generate a Docker image from a GeoDjango project
##
# Start from an existing image with Miniconda installed
FROM continuumio/miniconda3
MAINTAINER OrinMcD
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=awm_project.settings


# Ensure that everything is up-to-date
#RUN apt-get -y update && apt-get -y upgrade
RUN apt-get update && \
    apt-get install -y sudo nano && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN conda update -n base conda && conda update -n base --all


# Make a working directory in the image and set it as working dir.
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
# Get the following libraries. We can install them "globally" on the image as it will contain only our project
#RUN apt-get -y install build-essential python-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info

# You should have already exported your conda environment to an "ENV.yml" file.
# Now copy this to the image and install everything in it. Make sure to install uwsgi - it may not be in the source environment.
COPY ENV.yml /usr/src/app
RUN conda env create -n awm_project --file ENV.yml
# Make RUN commands use the new environment
# See https://pythonspeed.com/articles/activate-conda-dockerfile/ for explanation
RUN echo "conda activate awm_project" >> ~/.bashrc
SHELL ["/bin/bash", "--login", "-c"]

# Set up conda to match our test environment
RUN conda config --add channels conda-forge && conda config --set channel_priority strict
RUN cat ~/.condarc
RUN conda install uwsgi

# Create the static directory
RUN mkdir -p /usr/src/app/static
# Copy everything in your Django project to the image.
COPY . /usr/src/app
# Make sure that static files are up to date and available
RUN python manage.py collectstatic --no-input
#RUN python manage.py makemigrations
#RUN python manage.py migrate

# Expose port 8001 on the image. We'll map a localhost port to this later.
EXPOSE 8001

# Run "uwsgi". uWSGI is a Web Server Gateway Interface (WSGI) server implementation that is typically used to run Python
# web applications.
CMD uwsgi --ini uwsgi.ini