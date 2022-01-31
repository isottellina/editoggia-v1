FROM node:latest AS build-node

COPY package.json yarn.lock /
RUN yarnpkg install --modules-folder editoggia_node_modules

FROM python:3.10

RUN pip install pipenv
COPY Pipfile Pipfile.lock /editoggia/
WORKDIR /editoggia
RUN pipenv install --system

COPY . /editoggia
COPY --from=build-node /editoggia_node_modules /editoggia/editoggia/static/node_modules

CMD ["gunicorn", "editoggia.wsgi:app", "--bind", "0.0.0.0:8000"]
