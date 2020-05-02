<!-- README.md --- 
;; 
;; Filename: README.md
;; Author: Louise <louise>
;; Created: Sat May  2 01:12:36 2020 (+0200)
;; Last-Updated: Sat May  2 06:05:28 2020 (+0200)
;;           By: Louise <louise>
 -->
# Editoggia

Editoggia is a webapp intended to let people share their writings, whether
they be original stories, fanfictions, or even essays. It's currently in
very early stages.

## Installation

Use the tool pipenv to create a virtual environment with all required dependencies,
automatically.

```bash
pipenv install
```

## Usage

You can run the development server by setting the `FLASK_APP` and `FLASK_DEBUG`
environment variables and running `flask run`.

```bash
export FLASK_APP=editoggia
export FLASK_DEBUG=True
flask run
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
