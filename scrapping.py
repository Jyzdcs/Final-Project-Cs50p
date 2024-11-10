import requests
import json
import re
from bs4 import BeautifulSoup

url = "https://www.marmiton.org/recettes/index/categorie/dessert/"
response = requests.get(url)

def main():
	if response.status_code == 200:
		soup = BeautifulSoup(response.content, "html.parser")
		recette_link = soup.find_all('a', class_='recipe-card-link', limit=10)

		bdd = {}

		for link in recette_link:
			response_recette = requests.get(link['href'])
			soup = BeautifulSoup(response_recette.content, "html.parser")
			actual_key = soup.find('h1').get_text()
			bdd[actual_key] = {}
			scrap_ingredients(soup, bdd, actual_key)
			scrap_preparations(soup, bdd, actual_key)

		export_to_json(bdd)
	
def	scrap_ingredients(soup, bdd, actual_key):
	ingredients_card = soup.find_all("div", class_="mrtn-recette_ingredients-items")

	bdd[actual_key].update({"Ingredients" : []})
	for card in ingredients_card:
		for span_ingredient in card.find_all("span", "card-ingredient-title"):
			ingredient_text = ""
			ingredient_text += span_ingredient.get_text().strip()
			ingredient_text = re.sub(r'\s+', ' ', ingredient_text).strip()
			bdd[actual_key]["Ingredients"].append(ingredient_text)


def scrap_preparations(soup, bdd, actual_key):
	preparation_panel = soup.find_all("div", class_="recipe-step-list")

	bdd[actual_key]["Preparation"] = []
	
	for div in preparation_panel:
		for span in div.find_all("p"):
			prep = ""
			prep += span.get_text().strip()
			prep = re.sub(r'\s+', ' ', prep).strip()
			bdd[actual_key]["Preparation"].append(prep)


def export_to_json(bdd, filename="data.json"):
	with open(filename, 'w', encoding="utf-8") as f:
		json.dump(bdd, f, ensure_ascii=False, indent=4)

main()