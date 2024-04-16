import requests
from bs4 import BeautifulSoup

def extract_data_from_single_elements(soup):

    product_search_element = soup.find(id="woocommerce-product-search-field-0")
    print(product_search_element,"\n")

    # get the first <h1> element
    # on the page
    h1_element = soup.find("h1")
    print(h1_element,"\n")

    # find the first element on the page
    # with "search_field" class
    search_input_element = soup.find(class_="search_field")
    print(search_input_element, "\n")

    # find the first element on the page
    # with the name="s" HTML attribute
    search_input_element2 = soup.find(attrs={"name": "s"})
    print(search_input_element2, "\n")

    # find the first element identified
    # by the "input.search-field" CSS selector
    search_input_element3 = soup.select_one("input.search-field")
    print(search_input_element3, "\n")

    # On text content HTML elements, extract their text with get_text():
    h1_title = soup.select_one(".beta.site-title").getText()
    print(h1_title)

    product_search_element = soup.find(id="woocommerce-product-search-field-0")
    # making sure product_search_element is present on the page
    # before trying to access its data
    if product_search_element is not None:
        placeholder_string = product_search_element["placeholder"]
        print(placeholder_string)


def select_nested_elements(soup):
    venosaur_element = soup.find(class_="post-730")
    # extracting data from the nested nodes
    # extracting data from the nested nodes
    # inside the Venosaur product element
    venosaur_image_url = venosaur_element.find("img")["src"]
    venosaur_price = venosaur_element.select_one(".amount").get_text()

    print(venosaur_image_url)
    print(venosaur_price)

    wartortle_element = soup.find(class_="post-735")
    wartortle_url = wartortle_element.find("a")["href"]
    wartortle_name = wartortle_element.find("h2").get_text()
    print(wartortle_element)
    print(wartortle_url)
    print(wartortle_name)


def look_for_hidden_elements():
    response = requests.get("https://scrapeme.live/shop/Charizard/")
    soup = BeautifulSoup(response.content, "html.parser")

    additional_info_div = soup.select_one(".woocommerce-Tabs-panel--additional_information")
    print(additional_info_div.prettify())


def get_data_from_table():
    response2 = requests.get("https://scrapeme.live/shop/Charizard/")
    soup2 = BeautifulSoup(response2.content, "html.parser")

    additional_info_div = soup2.select_one(".woocommerce-Tabs-panel--additional_information")
    # get the table contained inside the
    # "Additional Information" div
    additional_info_table = additional_info_div.find("table")

    # iterate over each row of the table
    for row in additional_info_table.find_all("tr"):
        category_name = row.find("th").get_text()
        cell_value = row.find("td").get_text()
        print(category_name, cell_value)


def get_data_from_table2():
    response3 = requests.get("https://en.wikipedia.org/wiki/List_of_SpongeBob_SquarePants_episodes")
    soup3 = BeautifulSoup(response3.content, "html.parser")
    episode_table = soup3.select_one(".wikitable.plainrowheaders.wikiepisodetable")

    # skip the header row
    for row in episode_table.find_all("tr")[1:]:
        # to store cell values
        cell_values = []

        # get all row cells
        cells = row.find_all("td")
        # iterating over the list of cells in
        # the current row
        for cell in cells:
            # extract the cell content
            cell_values.append(cell.get_text())

        print("; ".join(cell_values))



def scrape_a_list_of_elements(soup):
    product_elements = soup.select("li.product")

    for product_element in product_elements:
        name = product_element.find("h2").get_text()
        url = product_element.find("a")["href"]
        image = product_element.find("img")["src"]
        price = product_element.select_one(".amount").get_text()

        print(name, url, image, price)

    print("__________________________________________________")
    # the list of dictionaries containing the
    # scrape data
    pokemon_products = []
    for product_element in product_elements:
        name = product_element.find("h2").get_text()
        url = product_element.find("a")["href"]
        image = product_element.find("img")["src"]
        price = product_element.select_one(".amount").get_text()

        # define a dictionary with the scraped data
        new_pokemon_product = {
            "name": name,
            "url": url,
            "image": image,
            "price": price
        }
        # add the new product dictionary to the list
        pokemon_products.append(new_pokemon_product)

    print(pokemon_products)
    print("__________________________________________________")
    export_to_csv(pokemon_products)
    print("__________________________________________________")
    export_to_json(pokemon_products)
    print("__________________________________________________")

def export_to_csv(pokemon_products):
    import csv

    # scraping logic...

    # create the "products.csv" file
    csv_file = open('products.csv', 'w', encoding='utf-8', newline='')

    # initialize a writer object for CSV data
    writer = csv.writer(csv_file)

    # convert each element of pokemon_products
    # to CSV and add it to the output file
    for pokemon_product in pokemon_products:
        writer.writerow(pokemon_product.values())

    # release the file resources
    csv_file.close()
    print("CSV file created")


def export_to_json(pokemon_products):
    import json

    # scraping logic...

    # create the "products.json" file
    json_file = open('data.json', 'w')

    # convert pokemon_products to JSON
    # and write it into the JSON output file
    json.dump(pokemon_products, json_file)

    # release the file resources
    json_file.close()
    print("JSON file created")


print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")

# // download the HTML document
# // with an HTTP GET request
response = requests.get("https://scrapeme.live/shop/")

# if the response is 2xx
if response.ok:
    # scraping logic here...
    # // print the HTML code
    # print(response.text)

    soup = BeautifulSoup(response.content, "html.parser")
    # print(soup)

    extract_data_from_single_elements(soup)
    print("\n################################################################################################################################")
    select_nested_elements(soup)
    print("\n################################################################################################################################")
    look_for_hidden_elements()
    print("\n################################################################################################################################")
    get_data_from_table()
    print("\n################################################################################################################################")
    get_data_from_table2()
    print("\n################################################################################################################################")
    scrape_a_list_of_elements(soup)
    print("\n################################################################################################################################")

else:
    # log the error response
    # in case of 4xx or 5xx
    print(response)
