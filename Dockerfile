# syntax=docker/dockerfile:1
FROM python:3.8.11
RUN apt-get update && apt-get -y install cron
RUN apt-get -y install libxml2-dev libxslt-dev python-dev python3-lxml

RUN useradd --create-home appuser

RUN groupadd docker
RUN usermod appuser -aG docker

#USER appuser
WORKDIR /home/appuser

COPY --chown=appuser:appuser requirements.txt requirements.txt
RUN  pip install --upgrade pip
RUN  pip install -r requirements.txt
#RUN mkdir /home/appuser/logs


ADD --chown=appuser:appuser enviratron_logger enviratron_logger

# install the python package:
#USER root
WORKDIR /home/appuser/enviratron_logger
RUN python3.8 setup.py install

WORKDIR /home/appuser
#USER appuser


COPY logger.sh logger.sh
RUN chmod +x logger.sh

#USER root
COPY --chown=appuser:appuser example_logger_config.yaml logger.yml
COPY --chown=appuser:appuser logger-cron /etc/cron.d/logger-cron
RUN chmod 0664 /etc/cron.d/logger-cron
# Apply cron job
RUN crontab /etc/cron.d/logger-cron
# Create the log file to be able to run tail
RUN touch ./cron.log

# Run the command on container startup
#USER root
CMD cron && tail -f ./cron.log
#CMD cron && tail -f ./cron.log
#USER appuser


#CMD ["python", "-m", "enviratron_logger", "./logger.yml"]

