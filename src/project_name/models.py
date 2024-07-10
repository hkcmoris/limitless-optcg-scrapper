import json


class OPCG_Card:
    """
    A class to represent a One Piece Card Game card.

    Attributes
    ----------
    id : str
        the card's ID
    code : str
        the card's code
    classification : str
        the card's classification
    type : str
        the card's type
    name : str
        the card's name
    image_src : str
        the card's image URL¨
    cost : str
        the card's cost
    life : str
        the card's life
    attribute : str
        the card's attribute
    power : str
        the card's power
    counter : str
        the card's counter
    color : str
        the card's color
    feature : str
        the card's feature
    effect : str
        the card's effect
    card_sets : str
        the card's card sets
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the card object.
        """
        self.id = ""
        self.code = ""
        self.rarity = ""
        self.type = ""
        self.name = ""
        self.image_src = ""
        self.cost = ""
        self.attribute = ""
        self.power = ""
        self.counter = ""
        self.color = ""
        self.colorShort = ""
        self.feature = ""
        self.effect = ""
        self.card_sets = ""

    def parse_card_data(self, dl_tag):
        self.id = dl_tag.get('id')
        
        infoCol = dl_tag.find("div", class_="infoCol")
        info_spans = infoCol.find_all("span")
        self.code = info_spans[0].text
        self.rarity = info_spans[1].text
        if (" CARD" in self.rarity):
            self.rarity = self.rarity.split(" CARD")[0]
        self.type = info_spans[2].text
        
        self.name = dl_tag.find("div", class_="cardName").text
        
        frontCol = dl_tag.find("div", class_="frontCol")
        self.image_src = frontCol.find("img").get('src').replace("..", "https://en.onepiece-cardgame.com")

        backCol = dl_tag.find("div", class_="backCol")
        
        cost_info = backCol.find("div", class_="cost").find("h3").next_sibling.strip()
        attribute_info = backCol.find("div", class_="attribute").find("i").text
        power_info = backCol.find("div", class_="power").find("h3").next_sibling.strip()
        counter_info = backCol.find("div", class_="counter").find("h3").next_sibling.strip()
        color_info = backCol.find("div", class_="color").find("h3").next_sibling.strip()
        feature_info = backCol.find("div", class_="feature").find("h3").next_sibling.strip()
        effect_info = backCol.find("div", class_="text").find("h3").next_sibling.strip()
        card_set_info = backCol.find("div", class_="getInfo").find("h3").next_sibling.strip()
        
        self.cost = cost_info
        self.attribute = attribute_info
        if ("/" in self.attribute):
            self.attribute = self.attribute.split("/")
        self.power = power_info
        self.counter = counter_info
        if (self.counter == "-"):
            self.counter = "0"
        self.color = color_info
        self.colorShort = self.color[0][0]
        if ("/" in self.color):
            self.color = self.color.split("/")
            self.colorShort += "/" + color_info.split("/")[1][0]
        self.feature = feature_info
        if ("/" in self.feature):
            self.feature = self.feature.split("/")
        self.effect = effect_info
        self.card_sets = card_set_info

    def __str__(self):
        """
        Returns a string representation of the card object.

        Returns
        -------
        str
            a string representation of the card object
        """
        return f"[{self.code}] {self.rarity.ljust(5)} {self.colorShort.ljust(3)} {self.name.ljust(35)} - {self.type.ljust(9)} - {self.image_src}"
    
    def __repr__(self):
        """
        Returns a string representation of the card object.

        Returns
        -------
        str
            a string representation of the card object
        """
        return f"[{self.code}] {self.rarity.ljust(5)} {self.colorShort.ljust(3)} {self.name.ljust(35)} - {self.type.ljust(9)} - {self.image_src}"
    
    def toJSON(self):
        card_data = {
            'id': self.id,
            'code': self.code,
            'rarity': self.rarity,
            'type': self.type,
            'name': self.name,
            'image_src': self.image_src,
            'cost': self.cost,
            'attribute': self.attribute,
            'power': self.power,
            'counter': self.counter,
            'color': self.color,
            'colorShort': self.colorShort,
            'feature': self.feature,
            'effect': self.effect,
            'card_sets': self.card_sets
        }
        card_dict = { self.id: card_data }
        json_output = json.dumps(card_dict, indent=4, ensure_ascii=False)
        return card_dict

class OPCG_Set:
    """
    A class to represent a One Piece Card Game set.

    Attributes
    ----------
    id : str
        the set's ID
    code : str
        the set's code
    name : str
        the set's name
    series : str
        the set's series
    cards : OPCG_Card
        the set's cards
    image : str
        the set's image URL
    """

    def __init__(self, id, code, name, series, image):
        """
        Constructs all the necessary attributes for the set object.

        Parameters
        ----------
        id : str
            the set's ID
        code : str
            the set's code
        name : str
            the set's name
        series : str
            the set's series
        cards : OPCG_Card
            the set's cards
        image : str
            the set's image URL
        """
        self.id = id
        self.code = code
        self.name = name
        self.series = series
        self.cards = []
        self.image = image

    def AddCard(self, card):
        """
        Adds a card to the set.

        Parameters
        ----------
        card : OPCG_Card
            the card to add to the set
        """
        self.cards.append(card)

    def __str__(self):
        """
        Returns a string representation of the set object.

        Returns
        -------
        str
            a string representation of the set object
        """
        return f"[{self.code}] {self.name} ({self.series}) - {self.cards.count} - {self.image}"

    def __repr__(self):
        """
        Returns a string representation of the set object.

        Returns
        -------
        str
            a string representation of the set object
        """
        return f"[{self.code}] {self.name} ({self.series}) - {self.cards.count} - {self.image}"
    
    def toJSON(self):
        # cards_data = [json.loads(opcg_card.toJSON()) for opcg_card in self.cards]
        cards_data = { card_id: card_data for card in self.cards for card_id, card_data in card.toJSON().items() }
        set_data = {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'series': self.series,
            'cards': cards_data,
            'image': self.image
        }
        set_dict = { self.id: set_data }
        json_output = json.dumps(set_dict, indent=4, ensure_ascii=False)
        return set_dict
    
class OPCG_Collection:
    """
    A class to represent a One Piece Card Game collection.

    Attributes
    ----------
    """

    def __init__(self):
        """
        Constructs all the necessary attributes for the collection object.
        """
        self.sets = []

    def AddSet(self, set):
        """
        Adds a set to the collection.

        Parameters
        ----------
        set : OPCG_Set
            the set to add to the collection
        """
        self.sets.append(set)

    def __str__(self):
        """
        Returns a string representation of the collection object.

        Returns
        -------
        str
            a string representation of the collection object
        """
        return f"{self.sets}"
    
    def __repr__(self):
        """
        Returns a string representation of the collection object.

        Returns
        -------
        str
            a string representation of the collection object
        """
        return f"{self.sets}"
    
    def toJSON(self):
        # sets_data = [json.loads(opcg_set.toJSON()) for opcg_set in self.sets]
        sets_data = { set_id: set_data for opcg_set in self.sets for set_id, set_data in opcg_set.toJSON().items() }
        collection_data = {
            'sets': sets_data
        }
        json_output = json.dumps(collection_data, indent=4, ensure_ascii=False)
        return json_output