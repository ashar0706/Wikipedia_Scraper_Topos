
import logging

from wiki_scrapper.scrapper.collect_city_data import generate_cities_data

Logger = logging.getLogger(__name__)


def get_city_data_save_to_file() -> None:

    try:
        city_df = generate_cities_data()

        with open("data.csv", "w") as temp:
            city_df.to_csv(temp.name)

            # data.csv will be created in path running, just do what ever you want with this.



    except Exception:
        Logger.exception(F"Process failed quiting without further follow up")




if __name__ == '__main__':
    get_city_data_save_to_file()
