# Контейнер для запуска Selenium-тестов
FROM python:3.10-alpine

COPY . /

RUN mkdir -p /test-reports

RUN ["pip", "install", "-r", "requirements.txt"]

ENV SELENIUM_DRIVER_KIND="remote"
ENV REMOTE_DRIVER_HOST="localhost"

CMD ["pytest", "test", "--html=/test-reports/report.html", "--self-contained-html"]
