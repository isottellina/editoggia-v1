FROM node:latest AS build-node

COPY package.json yarn.lock /
RUN yarnpkg install --modules-folder editoggia_node_modules

FROM python:3.10

ENV FLASK_APP=editoggia.wsgi:app \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONUNBUFFERED=1

RUN pip install poetry
COPY pyproject.toml poetry.lock /editoggia/
WORKDIR /editoggia
RUN poetry install -E production

COPY . /editoggia
COPY --from=build-node /editoggia_node_modules /editoggia/editoggia/static/node_modules

CMD ["gunicorn", "editoggia.wsgi:app", "--bind", "0.0.0.0:8000"]
