import requests
from bs4 import BeautifulSoup
import csv
from pathlib import Path


# Récupération de l'url de la page d'accueil
url = "https://books.toscrape.com/"
response = requests.get(url)
if response.status_code == 200:
    print("La page a bien été récupérée")
else:
    print("Erreur")
# Récupération html de la page catégorie
soup = BeautifulSoup(response.content, "html.parser")


# Récupération des liens des catégories
url_categories = []
for links in soup.select(".nav-list ul li a"):
    link = links.get("href")
    url_categories.append("https://books.toscrape.com/" + link)


# Fonction Extraction des données
def extract_data_books(product_page_url):
    response = requests.get(product_page_url)
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
    number_available = soup.find('th', string='Availability').find_next('td').string.replace("In stock ", "").replace(
        "(", "").replace(")", "").replace(" available", "")

    # Récupération de la description du produit
    description_div = soup.find("div", id="product_description")
    if description_div:
        product_description = description_div.find_next("p").get_text(strip=True)
    else:
        product_description = ""

    # Récupération de la catégorie
    category = soup.find('li', {'class': 'active'}).find_previous('a').string

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
    image_url = soup.find("img").get("src").replace("../../", "http://books.toscrape.com/")


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
    return product_data


# Création d'un header pour le csv pour les en-têtes
header = ["product page url", "universal product code", "title" ,"price including tax", "price excluding tax", "number available", "product description", "category", "review rating", "image url"]

# Chemin du dossier où se trouve le script
script_dir = Path(__file__).resolve().parent


# Pour chaque catégorie
for categorie_url in url_categories:

    # Récupération de la page catégories
    response = requests.get(categorie_url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Récupération des liens des livres de la catégorie
    url_product_page = []
    for links in soup.select("h3 a"):
        link = links.get("href").replace("../", "")
        url_product_page.append("https://books.toscrape.com/catalogue/" + link)

    # Extraction des données de chaque livre
    all_books = []
    for product_url in url_product_page:
        donnees = extract_data_books(product_url)
        all_books.append(donnees)


    # Chemin du fichier CSV dans le dossier donnees_extraites
    categorie_nom = categorie_url.split("/")[-2]
    csv_file = script_dir / "donnees_extraites" / (categorie_nom + ".csv")

    # Création du fichier csv
    with csv_file.open(mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(header)
        for livre in all_books:
            writer.writerow(livre.values())