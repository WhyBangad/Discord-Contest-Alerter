# Discord Alerter Bot

## To run : 
`pip install -r requirements.txt`

Set the required environment variables, then : `python main.py`

## Aim : 
The aim of the project is to create a bot that sends alerts in a channel a set time before a contest on one of the selected list of websites.
The bot should also send a list of contests every day at a chosen time. 
The bot should also respond to queries from users and provide a list of contests as requested by the user.

## Version 1 :

* Bot can respond to queries with the name of the site provided.
* The time delta is hardcoded to 24 hours.
* Does not send reminders automatically.