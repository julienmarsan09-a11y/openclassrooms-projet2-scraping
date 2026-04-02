import requests
from bs4 import BeautifulSoup
import csv
from pathlib import Path

# Chemin du dossier où se trouve le script
script_dir = Path(__file__).resolve().parent
# Dossier pour les images
image_dir = script_dir / "donnees_extraites" / "images"
# Test si le dossier images existe
image_dir.mkdir(parents=True, exist_ok=True)


# Fonction pour récupérer l'url de la page et les liens des catégories
def get_categories():
    url = "https://books.toscrape.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

# Récupération des liens des catégories
    url_categories = []
    for links in soup.select(".nav-list ul li a"):
        link = links.get("href")
        url_categories.append("https://books.toscrape.com/" + link)
    return url_categories


# Fonction Extraction des données
def extract_data_books(product_page_url):
    page_response = requests.get(product_page_url)
    soup = BeautifulSoup(page_response.content, 'html.parser')

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
    image_url = soup.find("img").get("src").replace("../../", "https://books.toscrape.com/")


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


# Fonction pour récupérer les liens de tous les livres d'une catégorie
def get_books_urls(categorie_url):
    url_product_page = []
    page_url = categorie_url

    while page_url:
        response = requests.get(page_url)
        soup = BeautifulSoup(response.content, "html.parser")

        for links in soup.select("h3 a"):
            link = links.get("href").replace("../", "")
            url_product_page.append("https://books.toscrape.com/catalogue/" + link)

        next_page = soup.find("li", class_="next")
        if next_page:
            next_href = next_page.find("a")["href"]
            page_url = categorie_url.replace("index.html", next_href)
        else:
            page_url = None

    return url_product_page

# Fonction pour télécharger et sauvegarder les images des livres
def download_images(all_books, image_dir):
    # Téléchargement des images
    for livre in all_books:
        filename = f"{livre['universal product code']}.jpg"
        response = requests.get(livre['image url'])
        with open(image_dir / filename, "wb") as f:
            f.write(response.content)


# Programme principal pour chaque catégorie, récupère les livres, extrait les données, télécharge les images et exporte en CSV
url_categories = get_categories()

for categorie_url in url_categories:
    categorie_nom = categorie_url.split("/")[-2].rsplit("_", 1)[0]

    url_product_page = get_books_urls(categorie_url)

    all_books = []
    for product_url in url_product_page:
        donnees = extract_data_books(product_url)
        all_books.append(donnees)

    download_images(all_books, image_dir)

    csv_file = script_dir / "donnees_extraites" / "csv" / (categorie_nom + ".csv")
    csv_file.parent.mkdir(parents=True, exist_ok=True)

    with csv_file.open(mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(all_books)

    print(f"Catégorie : {categorie_nom} - {len(url_product_page)} livres - {len(all_books)} images téléchargées")