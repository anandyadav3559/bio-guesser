class Animal:
    def __init__(self, animal_name,species_key,image_url,fact):
        self.animal_name = animal_name
        self.species_key = species_key
        self.image_url = image_url
        self.fact = fact
    def to_dict(self):
        return {
            "animal_name": self.animal_name,
            "species_key": self.species_key,
            "image_url": self.image_url,
            "fact": self.fact
        }
class location:
    def __init__(self,species_key,locations,geo_hashes):
        self.locations = locations
        self.geo_hashes = geo_hashes
        self.species_key = species_key
    def to_dict(self):
        return {
            "species_key": self.species_key,
            "locations": self.locations,
            "geo_hashes": self.geo_hashes
        }