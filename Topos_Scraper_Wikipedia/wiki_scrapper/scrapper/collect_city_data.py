
from typing import Dict, Optional

import logging
import pandas as pd
import numpy as np
import re
import shutil
import tempfile
from bs4 import BeautifulSoup

from wiki_scrapper.scrapper.exception import UnsupportedResponse, Non200Response
from wiki_scrapper.scrapper.wiki_request import get_response


Logger = logging.getLogger(__name__)


WIKI_LINK = "https://simple.wikipedia.org{}"


city_rows_headers = ["Rank", "City", "State", "17 Estimate", "10 Census", "Change", "Area Km", "Area Mi", "Density km",
                    "Density mi"]


class CityAddRows:
    wiki_link = "Wiki link"
    climate = "Climate"
    mayor = "Mayor"
    official_website = "Official Website"


# this function is not used
def collect_main_city_table() -> pd.DataFrame:
    """
    Uses Pandas to extract tale from html

    :return:
        pd.DataFrame
    """
    index_page_response = get_response()
    index_tables = pd.read_html(index_page_response)
    city_table = index_tables[2]
    city_table['City'] = city_table['City'].map(lambda x: re.sub(r'[\[\]0-9]', '', x))
    city_table['Climate'] = np.NaN
    city_table['Mayor'] = np.NaN
    city_table['Official Website'] = np.NaN
    city_table['Wiki link'] = np.NaN
    return city_table


def collect_main_city_table_html() -> Optional[pd.DataFrame]:
    """
    Extracts data from the main table using beautiful soup.

    :return:
        pd.DataFrame
    """
    index_page_response = get_response()
    page_soup = BeautifulSoup(index_page_response, features="lxml")
    table_soup = page_soup.find_all("table", {"class": "wikitable"})

    city_table = table_soup[1]

    # First row still gets headers
    city_rows = city_table.find("tbody").find_all("tr")[1:]

    city_dict_list = []

    for inde, city_row in enumerate(city_rows):
        city_elems = city_row.find_all("td")
        city_dict = {}
        try:
            for index, city_elem in enumerate(city_elems):
                if index >= 10:
                    # Ignore coordingates and other data
                    continue

                if index == 1:
                    # This is to get the exact link to the city page to get further data
                    city_ele = city_elem.find("a")
                    city_dict[city_rows_headers[index]] = city_ele.text.replace("\n", "")
                    city_dict[CityAddRows.wiki_link] = city_ele['href']
                else:
                    # All other cells only the text data is needed
                    city_dict[city_rows_headers[index]] = city_elem.text.replace("\n", "")
        except Exception :
            # handle cases when the table data is inconsistent
            Logger.error(f"Index {index} is not in formatted as expected")
            continue

        if city_dict:
            city_dict_list.append(city_dict)

    city_df = pd.DataFrame(city_dict_list)
    city_df['Climate'] = np.NaN
    city_df['Mayor'] = np.NaN
    city_df['Official Website'] = np.NaN

    return city_df


def collect_data_from_city_page(city_row: pd.Series) -> pd.Series:
    """
    wen the city row is sent, it dertermines the WIki link to the city page and gets the response and from this
    extracts Climate desc, Elecation, Mayor, official website and adds the data to Series

    :param city_row: Series object for the city that is being processed

    :return:
        None
    """
    wiki_url_meta = city_row[CityAddRows.wiki_link]

    city_response = get_response(WIKI_LINK.format(wiki_url_meta))
    city_soup = BeautifulSoup(city_response, features="lxml")

    # Collect climate data
    climate_span = city_soup.find('span', id='Climate')
    if not climate_span:
        climate_span = city_soup.find('span', id="Weather")

    if climate_span:
        parent_element = climate_span.parent

        climate_data = parent_element.find_next("p").text

        if climate_data:
            city_row["Climate"] = climate_data.replace("\xa0", "")

    # Mayor
    info_box = city_soup.find("table", {"class": "infobox"})

    # Mayor
    mayor_element = info_box.find("a", text="Mayor")

    if not mayor_element:
        mayor_element = info_box.find_all("th", string=re.compile("Mayor"))[0]

    mayor_name = mayor_element.find_next("a").text if mayor_element else None

    if mayor_name:
        city_row["Mayor"] = mayor_name

    off_website_ele = info_box.find("th", text="Website")

    off_website = off_website_ele.find_next("td").text if off_website_ele else None

    if off_website:
        city_row["Official Website"] = off_website

    return city_row


def generate_cities_data() -> pd.DataFrame:
    """
    Goes to the index link of top ccities based on population and than extracts data for each city and saves a temp
    csv file

    :return:
        str
    """
    try:
        city_df = collect_main_city_table_html()
    except (UnsupportedResponse, Non200Response) as e:
        Logger.exception(e)
        raise e

    for i, city_row in city_df.iterrows():
        try:
            city_row = collect_data_from_city_page(city_row)
            city_df.loc[i] = city_row
        except Exception as e:
            Logger.error(f"Unsupported response from the URI for the city {city_row['City']}")
            continue

    return city_df
