FROM python:3.6

WORKDIR /app

RUN wget https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -P /usr/local/bin \
    && chmod +x /usr/local/bin/wait-for-it.sh

# Install Chromedriver
RUN wget -N http://chromedriver.storage.googleapis.com/85.0.4183.87/chromedriver_linux64.zip -P ~/ \
    && unzip ~/chromedriver_linux64.zip -d ~/ \
    && rm ~/chromedriver_linux64.zip \
    && mv -f ~/chromedriver /usr/local/share/ \
    && chmod +x /usr/local/share/chromedriver \
    && ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver \
    && apt-get update \
    && apt-get install -y libnss3-dev libx11-xcb-dev

# Install Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

# Install pip requirements
ARG REQUIREMENTS=requirements.txt
COPY requirements.txt dev_requirements.txt /app/

RUN pip install -r $REQUIREMENTS --disable-pip-version-check

ADD . /app