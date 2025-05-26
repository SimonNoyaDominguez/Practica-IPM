import requests

class Model:
    URL_CocktailDB = "https://www.thecocktaildb.com/api/json/v1/1"

    def search_cocktail_by_name(self, cocktail_name):
        url = f"{self.URL_CocktailDB}/search.php?s={cocktail_name}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("drinks", [])

    def get_random_cocktail(self):
        url = f"{self.URL_CocktailDB}/random.php"
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("drinks", [])[0]
