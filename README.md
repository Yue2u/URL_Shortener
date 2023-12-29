This is link shortener project like tinyURL or goo.gl

There two ways of using:
* Interface
* API

Docs for api can be found on /api/docs
site supports token authorization, you need to signup and visit your cabinet

Installation:
python >=3.10.12

Copy repo
git clone git@github.com:Yue2u/URL_Shortener.git

Create venv
python3 -m venv venv

Install postgresql
sudo apt install postgresql postgresql-contrib libpq-dev python3-dev


Install requirements
pip isntall -r requirements.txt

Set ENV dependencies:
export DATABASE_URL="postgres://user:password@127.0.0.1:5432/db_name" - databse url
export DEBUG="True"
export MAX_CODE_LENGTH="8" - length of shortened code

