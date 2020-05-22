from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from unidecode import unidecode
import csv
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('Submarino.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class books_submarino:
    def __init__(self):
        self.driver = webdriver.Chrome('/home/semantix/SeleniumDriver/chromedriver_linux64/chromedriver')
        self.driver.get('https://www.submarino.com.br/')
        self.wait = WebDriverWait(self.driver, 10)
        self.time_init = datetime.now()

    def clean_category_name(self, categories_list):
        categories =[]
        for g in range(0,len(categories_list)):
            category = categories_list[g].lower()
            category = category.replace(",", "")
            category = category.replace("/", " ")
            category = category.replace("&", "e")
            category = category.replace("º", "o")
            category = category.replace("+", "")
            category = category.replace("(", "")
            category = category.replace(")", "")
            category = category.replace("-", " ")
            category = category.replace("  ", " ")
            category = category.replace(" ", "-")
            category = category.replace("--", "-")
            category = unidecode(category)
            categories.append(category)
        return categories

    def get_attribute(self):
        namesXpath = "//*[@id='content-middle']/div[4]/div/div/div/div[1]/div/div/div[2]/a/section/div[2]/div[1]/h2"
        pricesXpath = "//*[@id='content-middle']/div[4]/div/div/div/div[1]/div/div/div[2]/a/section/div[2]/div[2]/div[2]/span"
        self.wait.until(EC.presence_of_all_elements_located((By.XPATH, namesXpath)))
        self.wait.until(EC.presence_of_all_elements_located((By.XPATH, pricesXpath)))
        names_list = self.driver.find_elements(By.XPATH, namesXpath)
        prices_list = self.driver.find_elements(By.XPATH, pricesXpath)
        names = []
        prices = []
        for f in range(0, len(names_list)):
            names.append(names_list[f].get_attribute("textContent"))
            try:
                prices.append(prices_list[f].get_attribute("textContent"))
            except:
                prices.append('NaN')
        return [names, prices]

    def write(self, categoria, subcategoria, nomes, precos):
        with open('SubmarinoBooks1.csv', mode='a') as csvfile:
            catalog = csv.writer(csvfile, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for a in range(0,len(nomes)):
                nome = nomes[a].replace('Livro - ', '')
                preco = precos[a].replace('R$ ', '')
                catalog.writerow([nome, categoria, subcategoria, preco])

    def get_books(self):
        a = 0
        while a == 0:
            try:
                nav_bar = "//*[@id='h_menu']/div/div/a"
                nav_bar_books = "//*[@id='h_menu']/div/div/div/div/div[2]/ul/li[2]/a"
                self.wait.until(EC.element_to_be_clickable((By.XPATH, nav_bar)))
                self.driver.find_element(By.XPATH, nav_bar).click()
                self.wait.until(EC.element_to_be_clickable((By.XPATH, nav_bar_books)))
                self.driver.find_element(By.XPATH, nav_bar_books).click()
                a += 1
            except:
                self.driver.refresh()
        categoryXpath = "//*[@id='collapse-categorias']/ul/li"
        self.wait.until(EC.presence_of_all_elements_located((By.XPATH, categoryXpath)))
        categories_list = self.driver.find_elements(By.XPATH, categoryXpath)
        categories = []
        for b in range(0,len(categories_list)):
            categories.append(categories_list[b].get_attribute("textContent"))
        category = books_submarino.clean_category_name(self, categories)
        for c in range(0,len(category)):
            if category[c] == "assinatura-de-revista-e-jornal":
                self.driver.get("https://www.submarino.com.br/categoria/livros/assinatura-de-revista-e-jornal?ordenacao=relevance")
            else:
                self.driver.get(f"https://www.submarino.com.br/categoria/livros/{category[c]}/l/B2W?ordenacao=relevance")
            try:
                subcategoriesXpath = "//*[@id='collapse-categorias']/ul/li"
                self.wait.until(EC.presence_of_all_elements_located((By.XPATH, subcategoriesXpath)))
                subcategories_list = self.driver.find_elements(By.XPATH, subcategoriesXpath)
                subcategories = []
                for d in range(0,len(subcategories_list)):
                    subcategories.append(subcategories_list[d].get_attribute("textContent"))
                subcategory = books_submarino.clean_category_name(self, subcategories)
                for e in range(0, len(subcategory)):
                    if subcategory[e][-1] == "-":
                        subcategory[e] = subcategory[e][:-1]
                    self.driver.get(f"https://www.submarino.com.br/categoria/livros/{category[c]}/{subcategory[e]}/l/B2W?ordenacao=relevance")
                    atr = books_submarino.get_attribute(self)
                    books_submarino.write(self, categories[c], subcategories[e], atr[0], atr[1])
                    try:
                        self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='content-middle']/div[4]/div/div/div/div[2]/div/ul/li")))
                        pages = self.driver.find_elements(By.XPATH,"//*[@id='content-middle']/div[4]/div/div/div/div[2]/div/ul/li")
                        for h in range(2, len(pages)-1):
                            self.driver.get(f"https://www.submarino.com.br/categoria/livros/{category[c]}/{subcategory[e]}/l/B2W/pagina-{h}?ordenacao=relevance")
                            atr = books_submarino.get_attribute(self)
                            books_submarino.write(self, categories[c], subcategories[e], atr[0], atr[1])
                    except:
                        pass
            except:
                atr = books_submarino.get_attribute(self)
                books_submarino.write(self, categories[c], subcategories[e], atr[0], atr[1])
                try:
                    self.wait.until(EC.presence_of_all_elements_located(
                        (By.XPATH, "//*[@id='content-middle']/div[4]/div/div/div/div[2]/div/ul/li")))
                    pages = self.driver.find_elements(By.XPATH,
                                                      "//*[@id='content-middle']/div[4]/div/div/div/div[2]/div/ul/li")
                    for h in range(2, len(pages) - 1):
                        self.driver.get(
                            f"https://www.submarino.com.br/categoria/livros/{category[c]}/{subcategory[e]}/l/B2W/pagina-{h}?ordenacao=relevance")
                        atr = books_submarino.get_attribute(self)
                        books_submarino.write(self, categories[c], subcategories[e], atr[0], atr[1])
                except:
                    pass
        self.time_end = datetime.now()
        time_delta = f"{self.time_end - self.time_init}"
        time_delta = time_delta.split(".")[0]
        logger.info(f"finish in {time_delta}")
        self.driver.quit()

if __name__ == '__main__':
    books_submarino().get_books()
