import json
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

    # <option value="569105">BOOSTER PACK &lt;br class="spInline"&gt;-AWAKENING OF THE NEW ERA- [OP-05]</option>

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
        browser.open(seriesUrl + opcg_set.id)
        set_data = browser.get_current_page().find("div", class_="resultCol").find_all("dl", class_="modalCol")
        for set in set_data:
            card = OPCG_Card()
            card.parse_card_data(set)
            opcg_set.AddCard(card)

    # Save to collection.json
    with open('collection.json', 'w', encoding='utf-8') as file:
        file.write(collection.toJSON())
        print('Collection saved to collection.json')


if __name__ == '__main__':
    run()
