import logging as logger

import requests
from bs4 import BeautifulSoup

import pandas as pd

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import sendgrid_api_config
import config

# Setup Logger configuration
logger.basicConfig(format=config.FORMAT, level=logger.INFO)

def get_places_of_interest():
    try : 
        logger.info("Get Covid-19 places of interest from MoH")


        response = requests.get(config.url, headers=config.headers)
        response.raise_for_status()

        logger.info(f"MoH returned {response.status_code}")
        logger.info(f"Parsing page contents using bs4")
        moh_page = BeautifulSoup(response.content,"lxml")

        your_places=[]  # List of places you are interested in
        logger.info(f"Finding all table rows")
        for child in moh_page.find_all('tr') :
            place_details_list = [detail.strip(' ') for detail in child.get_text().split('\n')]
            for interested_place in config.interested_places_list:
                logger.debug(interested_place)
                logger.debug(place_details_list)
                if interested_place in place_details_list[2]:
                    your_places.append(place_details_list)

        logger.debug(your_places)
        logger.info(f"Got {len(your_places)} places")

        return your_places
    except:
        logger.exception('Error Occurred : ')

def convert_list_to_table(places_list):
    # Get all data in list of lists into a dataframe
    places_table_full = pd.DataFrame(places_list)
    # Select only the 4 columns we are interested in
    places_table_selected = places_table_full.iloc[:,1:5]
    # Set headers
    places_table_selected.columns=["Place", "Address", "Date", "Time"]
    # Convert to HTML
    places_table = places_table_selected.to_html()

    pd.set_option("display.max_rows", None, "display.max_columns", None)
    logger.debug(places_table)

    return places_table

def send_email(places_table):
    # Send email
    try:
        message = Mail(
            from_email=sendgrid_api_config.FROM_EMAIL,
            to_emails=sendgrid_api_config.TO_EMAIL,
            subject=sendgrid_api_config.SUBJECT,
            html_content=f"<html> <body> <p> {places_table} </p> </body> </html>")

        sg = SendGridAPIClient(sendgrid_api_config.SENDGRID_API_KEY)
        response = sg.send(message)

        logger.debug(f"SendEmail returned : {response.status_code} : {response.body} : {response.headers}")
        logger.info(f"SendEmail returned : {response.status_code}")

        return True

    except Exception as error:
        logger.exception(error.message)
        raise error.message

if __name__ == "__main__":
    try : 
        logger.info("Starting Covid-19 places of interest checker")

        places_list = get_places_of_interest()

        places_table = convert_list_to_table(places_list)
        
        send_email(places_table)

        logger.info(f"Completed Covid-19 places of interest checker - Found {len(places_list)} Places")
    except Exception as error:
        logger.exception(error)

