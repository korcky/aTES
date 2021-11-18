FROM python:3.9.7-alpine3.14

RUN apk update && apk add libpq gcc python3-dev musl-dev postgresql-dev libffi-dev


WORKDIR /opt/internal_libs
COPY internal_libs .
WORKDIR /opt/internal_libs/event_schema_registry
RUN python setup.py bdist_wheel
RUN pip install dist/event_schema_registry-0.1.0-py3-none-any.whl