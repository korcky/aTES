FROM service_image

WORKDIR /opt/project
COPY . .

RUN mkdir -p /etc/cron.d
COPY cron_scheduler /etc/crontabs/root

RUN pip install -r requirements.txt