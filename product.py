

class Product:
    def __init__(self, name, price, prev_price, discount, link, prime):
        self.name = name
        self.price = price
        self.prev_price = prev_price
        self.discount = discount
        self.link = link
        self.prime = prime
    
    def serialize(self):
        return {
            "name" : self.name,
            "price" : self.price,
            "prev_price" : self.prev_price,
            "discount" : self.discount,
            "link" : self.link,
            "prime": self.prime
        }
    
    def from_json(self, json_):
        self.name = json_["name"]
        self.price = json_["price"]
        self.prev_price = json_["prev_price"]
        self.discount = json_["price_change"]
        self.link = json_["link"]
        self.prime = json_["prime"]