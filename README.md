
# Requirements
* Python 3.6+
* postgresql


# Standards
* Black
```
{
    "black_line_length": 79,
}
```
* Flake8


# Install & Setup
* It is assumed you have Python3 & pip3 already installed and configured

## Install Necessary Packages
```
pip3 install requirements.txt
sudo apt install postgresql
```

## Setup Application
* Create postgres user and setup DB
```
sudo passwd postgres
su - postgres
psql
\password postgres

CREATE DATABASE inventory;
CREATE USER inventory;
GRANT ALL PRIVILEGES ON DATABASE inventory TO inventory;
\password inventory
```
* Execute SQL
```
psql -h 127.0.0.1 -d inventory -U inventory -f database_setup.sql
```
* Process and insert CSV data into DB
```
python3 process_csv.py data.csv
```
* Configure Flask
```
export FLASK_ENV=dev
export FLASK_APP=run.py
```
* Run Flask
```
python3 -m flask run
```

# Usage
* From any browser, go to http://127.0.0.1:5000/


# Possibilities
* Use nginx to handle Auth and Static File severing for requests
* Use ReactJS for cleaner UI and modern Javascript design
