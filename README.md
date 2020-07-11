<!-- README.md --- 
;; 
;; Filename: README.md
;; Author: Louise <louise>
;; Created: Sat May  2 01:12:36 2020 (+0200)
;; Last-Updated: Sat Jul 11 21:10:11 2020 (+0200)
;;           By: Louise <louise>
 -->
# Editoggia

Editoggia is a webapp intended to let people share their writings, whether
they be original stories or fanfiction.

## Installation

Use the tool pipenv to create a virtual environment with all required dependencies,
automatically. You also have to use yarn to get all front-end dependencies.

```bash
pipenv install
yarn install --modules-folder editoggia/static/node_modules
```

Before using it, when you have configured the database (using POSTGRES_USER, 
POSTGRES_PASSWORD, and POSTGRES_DB if you are in production), you need to run:

```bash
flask create-db
```

You might also want to set an user as an admin. Once you have created the user,
run:

```bash
flask set-admin <username>
```

## Usage

You can run the development server by setting the `FLASK_APP` and `FLASK_DEBUG`
environment variables and running `flask run`.

```bash
export FLASK_APP=editoggia
export FLASK_DEBUG=True
flask run
```

To run it in production, you can run editoggia.wsgi:app with your favourite method
(I use uWSGI). Don't forget to set the EDITOGGIA_SECRET_KEY env variable.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
