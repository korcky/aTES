hosFROM python:3.9.7-alpine3.14

RUN apk update && apk add libpq gcc python3-dev musl-dev postgresql-dev libffi-dev