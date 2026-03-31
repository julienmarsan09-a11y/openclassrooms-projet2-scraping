import requests
from bs4 import BeautifulSoup
import csv
from pathlib import Path

# Récupération de l'url
product_page_url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
response = requests.get(product_page_url)
if response.status_code == 200:
    print("La page a bien été récupérée")
else:
    print("Erreur")

# Récupération html de la page
soup = BeautifulSoup(response.content, 'html.parser')

# Récupération du code upc
universal_product_code = soup.find("th", string="UPC").find_next_sibling("td").string

# Récupération du titre de la page
title = soup.find("h1").string

# Récupération du prix avec taxes
price_including_tax = soup.find("th", string="Price (incl. tax)").find_next_sibling("td").string

# Récupération du prix sans taxes
price_excluding_tax = soup.find("th", string="Price (excl. tax)").find_next_sibling("td").string

# Récupération du stock disponible
number_available = soup.find('th',string='Availability').find_next('td').string.replace("In stock ","").replace("(","").replace(")","").replace(" available","")

# Récupération de la description du produit
product_description = soup.find("div", id="product_description").find_next("p").get_text(strip=True)

# Récupération de la catégorie
category = soup.find('li', {'class':'active'}).find_previous('a').string

# Récupération de la note du livre et conversion de la note en chiffre
ratings = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

review_rating = ratings[soup.find("p", class_="star-rating")["class"][1]]

# Récupération de l'url de l'image du livre
image_url = soup.find("img").get("src").replace("../../","http://books.toscrape.com/")

# Création d'un header pour le csv pour les en-têtes
header = ["product page url", "universal product code", "title" ,"price including tax", "price excluding tax", "number available", "product description", "category", "review rating", "image url"]

# Récupération des données
product_data = {
    "product page url": product_page_url,
    "universal product code": universal_product_code,
    "title": title,
    "price including tax": price_including_tax,
    "price excluding tax": price_excluding_tax,
    "number available": number_available,
    "product description": product_description,
    "category": category,
    "review rating": review_rating,
    "image url": image_url
}

#obtention du chemin du dossier dans lequel se trouve le script
script_dir = Path(__file__).resolve().parent

# Création du fichier csv
csv_file = script_dir / "a_light_in_the_attic.csv"
with csv_file.open(mode='w', newline='') as f:
    writer = csv.writer(f,delimiter=',')

    #ecriture du header
    writer.writerow(header)

    #ecriture des donnees
    writer.writerow(product_data.values())