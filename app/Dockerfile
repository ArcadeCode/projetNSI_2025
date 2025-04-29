# Dockerfile for Buildozer
# 
# This Dockerfile sets up an environment for using Buildozer, a tool for packaging Python applications for Android, iOS, Windows, OSX, and/or Linux.
# 
# The base image is chosen to provide a minimal environment with the necessary dependencies for Buildozer.
# 
# The Dockerfile performs the following steps:
# 1. Updates the package list and installs required system packages.
# 2. Installs Python and pip.
# 3. Installs Buildozer and its dependencies using pip.
# 4. Sets up the necessary environment variables.
# 5. Defines the entry point for the Docker container.
# 
# Commentary:
# This file is a fork from https://github.com/tshirtman/Buildozer-docker/blob/master/Dockerfile
FROM ubuntu:22.04

# Path of the project, there is where the project is on your pc
ARG APP_PATH="/app"
ENV APP_PATH=${APP_PATH}

# Installing dependencies
RUN apt-get update \
 && apt-get install -y \
    git zlib1g-dev openjdk-17-jdk-headless autoconf curl libtool \
    libpq-dev libssl-dev ccache unzip zip python3 \
    python3-virtualenv python3-pip pkg-config cmake libffi-dev \
 && pip3 install cython==0.29.33 buildozer \
 && echo "python3 -m virtualenv" > /usr/bin/virtualenv \
 && chmod +x /usr/bin/virtualenv

# Create app directory inside the container
RUN mkdir -p /buildozer/app
# Copy the project from the build context (project should be in the same folder as the Dockerfile)
COPY ./app /buildozer/app/
# Set the working directory
WORKDIR /buildozer/app

RUN yes | buildozer init . \
 #sed -i 's/^param1=.*/param1=my_value/' fichier.ini
 && sed -i 's/warn_on_root.*/warn_on_root = 0/' buildozer.spec \
 && sed -i 's/log_level.*/log_level = 2/' buildozer.spec \
 && sed -i 's/title.*/title = Sportify app/' buildozer.spec \
 && sed -i 's/package.name.*/package.name = org.sportify/' buildozer.spec \
 && sed -i 's/package.name.*/package.domain = org.sportify/' buildozer.spec \
 && sed -i 's/android.permissions*/android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION/' buildozer.spec \
 && yes | buildozer android debug

# We go back in buildozer because "/buildozer/app/" doesn't need to be persistent
WORKDIR /buildozer/

# Reserved by buildozer, we will extract builds from here
VOLUME /buildozer/
# Reserved by Python for android
VOLUME /p4a/
# Reserved by ?
VOLUME /opt/
# WORKDIR is ./buildozer/
WORKDIR /buildozer/

CMD ["yes", "|", "buildozer", "android", "debug", "-v"]
