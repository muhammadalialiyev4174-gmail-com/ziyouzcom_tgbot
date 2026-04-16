import sqlite3
import requests
   
import re

from bs4 import BeautifulSoup

"""
def add_category_books(name, typ, link):
    conn = sqlite3.connect("main.db")
    cursor = conn.cursor()

    sql = "INSERT INTO category_books (name, typ, link) VALUES (?, ?, ?)"
    cursor.execute(sql, (name, typ, link))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    url = "https://n.ziyouz.com/kutubxona/category/204-bibliografik-nashrlar"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    subcategories = soup.find_all("div", class_="pd-subcategory")
    
    for subcategory in subcategories:
        link = subcategory.find("a")["href"]
        try:
            add_category_books(name=subcategory.text, typ="Bibliografik nashrlar", link=link)
        except Exception as err:
            print(err)
"""
"""
head_url= "https://n.ziyouz.com"
url =head_url+"/kutubxona/category/38-o-zbek-xalq-og-zaki-ijodi"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
subcategories = soup.find_all("div", class_="pd-float")
for subcategory in subcategories:
    link = subcategory.find("a")["href"] 
    if re.search("1777",link):
        print("Link found:", link)
        break
    else: 
        print("another")
"""
    
"""
subcategories = soup.find_all("div", class_="pd-float")
for subcategory in subcategories:
    link = subcategory.find("a")["href"]
    print(link)
    def has_link(text):
        match = re.search(r"downloa\d+=\d+", text)
        if match:
            return True
        else:
            return False
    print(has_link("downloand=1777"))
"""