Project Title

Wiki scrapper, This gets the details of top cities in US based on population and Than goes to individual city page 
and extracts additional details as in Climate, Mayor, City official URL

If the city does not have any wiki page it will only add the data that has been recieved from main table from URL 
- https://simple.wikipedia.org/wiki/List_of_United_States_cities_by_population

It uses Beautiful Soup it scrap data from page and creates a panda object and creates a CSV file from pandas which 
gets saved as data.csv in the folder where this project is being run.


These instructions will get you a copy of the project up and running on your local machine for development and testing

You will need Python > 3.6
And pip

Google is easy way to get them and quick search will you get going

With respect to this project create a virtual environment and install all the requirements mentioned in the 
requiremnts.txt

you ciould use :- 
pip install -r requirements.txt

This is it, You are good to go.

To run the file, Run runner.py.. This has the main that will take care of remianing calls and get you a data.csv file
