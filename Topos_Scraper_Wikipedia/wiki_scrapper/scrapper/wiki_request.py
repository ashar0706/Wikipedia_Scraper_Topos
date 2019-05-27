import logging

import requests

from wiki_scrapper.scrapper.exception import Non200Response, UnsupportedResponse

Logger = logging.getLogger(__name__)


def get_response(web_url: str="https://simple.wikipedia.org/wiki/List_of_United_States_cities_by_population") -> str:
    """
    PRovide the wiki URL from which response has to be recieved and this will return the text response that has been
    returned

    :arg:
        web_url: URL which we are expecting data

    :return:
        str
    """
    Logger.info(f"fetching response for URL {web_url}")
    response = requests.get(web_url)

    if response is None:
        Logger.error(f"response from URL is none")
        raise UnsupportedResponse("No reponse when hitting the URL")

    if response.status_code != 200:
        Logger.error(f"Response status is {response.status_code}")
        raise Non200Response(f"status for response {response.status_code}")

    Logger.info(f"Response status is 200")

    return response.text

