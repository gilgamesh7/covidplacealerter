# covidplacealerter

This Python script that will access the Ministry of Health website of Places of Interest , extraxcts just the ones you ar interested in, and emails it to your email of choice using sendgrid.

# How to Install
- Clone repository from github
- create venv using python -m venv venv
- pip install -r requirements.txt

# To configure
- open config.py and configure the places you are interested in, in the entry
    - interested_places_list = []
- Create a sendgrid account (https://sendgrid.com/)
- Remember to verify your sender email
- create a file called sendgrid_api_config with the entries
    - SENDGRID_API_KEY = "your key"
    - FROM_EMAIL="verified email"
    - TO_EMAIL="verified email"
    - SUBJECT="COVID-19 Customised Places Of Interest"

# To run
Run check_covid_places_of_interest.py and wait for email