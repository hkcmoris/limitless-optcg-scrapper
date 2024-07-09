import json
import re
import mechanicalsoup


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

    # print(browser.get_current_page())

    # Get the filter element
    seriesElement = browser.get_current_page().find("div", class_="searchCol").find("div", class_="seriesCol")
    seriesElement = seriesElement.find("select", id="series").find_all("option")
    seriesElements = [option for option in seriesElement if option.has_attr('value') and option['value']]
    
    # Extract text and value, ignoring HTML tags
    series_data = [{option['value']: re.sub('<[^<]+?>', '', option.get_text())} for option in seriesElements]
    series_json = json.dumps(series_data, indent=4)

    seriesUrl = "https://en.onepiece-cardgame.com/cardlist/?series="

    for series in series_data:
        seriesId = list(series.keys())[0]
        seriesName = list(series.values())[0]
        print(f"{seriesId}: {seriesName}")
        browser.open(seriesUrl + seriesId)
        set = browser.get_current_page().find("div", class_="resultCol").find_all("dl", class_="modalCol")
        print(set)
        pause = input("Press Enter to continue...")

if __name__ == '__main__':
    run()
