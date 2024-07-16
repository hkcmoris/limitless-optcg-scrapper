import json
import os
import re
import mechanicalsoup
from models import OPCG_Card, OPCG_Collection, OPCG_Set


def run():
    """
    Run the application.
    """
    print('Running the application...')

    # Initialize the browser
    browser = mechanicalsoup.StatefulBrowser()

    # Set the URL of the page containing the cards
    url = "https://en.onepiece-cardgame.com/cardlist/"

    # Open the URL
    browser.open(url)

    # Get the filter element
    seriesElement = browser.get_current_page().find("div", class_="searchCol").find("div", class_="seriesCol")
    seriesElement = seriesElement.find("select", id="series").find_all("option")
    seriesElements = [option for option in seriesElement if option.has_attr('value') and option['value']]
    
    # Extract text and value, ignoring HTML tags
    series_data = [{option['value']: re.sub('<[^<]+?>', '', option.get_text())} for option in seriesElements]
    from collections import OrderedDict
    # order series_data by the ID
    series_data = sorted(series_data, key=lambda x: list(x.keys())[0])
    seriesUrl = "https://en.onepiece-cardgame.com/cardlist/?series="

    collection = OPCG_Collection()

    for series in series_data:
        seriesId = list(series.keys())[0]
        seriesText = list(series.values())[0]
        seriesName = seriesText
        seriesCode = "×"
        seriesSeries = "×"

        if " -" in seriesText:
            seriesSeries = seriesText.split(" -")[0]
            seriesName = seriesText.split(" -")[1]
            if "- [" in seriesName:
                seriesCode = seriesName.split("- [")[1]
                if "]" in seriesName:
                    seriesCode = seriesCode.split("]")[0]
                seriesName = seriesName.split("- ")[0]
        opcg_set = OPCG_Set(seriesId, seriesCode, seriesName, seriesSeries, "")
        collection.AddSet(opcg_set)

    for opcg_set in collection.sets:
        print(f"Processing {opcg_set.name} ({opcg_set.series})")
        if opcg_set.series == "STARTER DECK" or opcg_set.series == "ULTRA DECK": series = 'decks'
        elif opcg_set.series == "BOOSTER PACK" or opcg_set.series == "EXTRA BOOSTER": series = 'boosters'
        else: series = 'other'
        code = opcg_set.code.lower()
        if opcg_set.series == "STARTER DECK": 
            if code == "st01" or code == "st02" or code == "st03" or code == "st04":
                code = "st01-04"
        if code == 'op05':
            opcg_set.image = 'https://en.onepiece-cardgame.com/products/boosters/op05/images/mv_chara.png'
        else:
            imageUrl = f'https://en.onepiece-cardgame.com/products/{series}/{code}.php'
            response = browser.open(imageUrl)
            if response.status_code != 200:
            # if browser.get_current_page() is None or browser.get_current_page().text == "File not found":
                print(f"Warning: No image found for set {opcg_set.series} {opcg_set.name}")
                continue
            image = browser.get_current_page().find("main", class_="mainCol").find("div", class_="productsSlider").find("ul", class_="productsMainSlider").find("li").find("p").find("img")
            opcg_set.image = image.get('src').replace("../..", "https://en.onepiece-cardgame.com")
        browser.open(seriesUrl + opcg_set.id)
        set_data = browser.get_current_page().find("div", class_="resultCol").find_all("dl", class_="modalCol")
        total_cards = len(set_data)
        index = 0
        for set in set_data:
            index += 1
            print(f"\rProcessing card {index}/{total_cards}", end='', flush=True)
            card = OPCG_Card()
            card.parse_card_data(set)
            card.card_sets['id'] = opcg_set.id
            opcg_set.AddCard(card.id)
            collection.AddCard(card)
        print("\n")
    
    version = 'v2'
    file_path = f'limitless-optcg-scrapper/src/collection.{version}.json'
    # Check if the file exists
    if not os.path.exists(file_path):
        # If the file does not exist, log a message or perform other actions, and create the file
        print(f"{file_path} does not exist, will be created.")


    # Save to collection.json
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(collection.toJSON())
        print(f'Collection saved to {file_path}')


if __name__ == '__main__':
    run()
