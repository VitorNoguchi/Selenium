import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

bestseller_catalog = {'nome': [], 'categoria': [], 'subcategoria': [], 'preco': []}
release_catalog = {'nome': [], 'categoria': [], 'subcategoria': [], 'preco': []}

class submarino:
    def __init__(self):
        self.driver = webdriver.Chrome('/home/semantix/SeleniumDriver/chromedriver_linux64/chromedriver')
        self.driver.get('https://www.submarino.com.br/')
        self.driver.find_element_by_css_selector("a[title=Livros]").click()
        self.wait = WebDriverWait(self.driver, 10)

    def best_sellers(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='collapse-os mais buscados']/ul/li[3]/a"))).click()
        self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='main-top']/div[3]/div/div/div/div")))
        count = self.driver.find_elements(By.XPATH, "//*[@id='main-top']/div[3]/div/div/div/div")
        for a in range(1, len(count)):
            self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//*[@id='main-top']/div[3]/div/div/div/div[{a}]/div[2]/section/a")))
            self.driver.find_element(By.XPATH, f"//*[@id='main-top']/div[3]/div/div/div/div[{a}]/div[2]/section/a").click()
            bestseller_catalog['nome'].append(self.wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="product-name-default"]'))).get_attribute("textContent"))
            bestseller_catalog['categoria'].append(self.wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='content']/div/div/div[2]/div/section/div/div[1]/div/div[3]/a/div/span"))).get_attribute("textContent"))
            try:
                bestseller_catalog['subcategoria'].append(self.wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='content']/div/div/div[2]/div/section/div/div[1]/div/div[4]/a/div/span"))).get_attribute("textContent"))
            except:
                bestseller_catalog['subcategoria'].append('none')
            bestseller_catalog['preco'].append(self.wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='content']/div/div/div[2]/div/section/div/div[2]/div[2]/div/div[1]/div/div[1]/div/div/span"))).get_attribute("textContent"))
            print(bestseller_catalog)
            self.driver.back()
        self.driver.quit()
        return bestseller_catalog

    def release(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='collapse-os mais buscados']/ul/li[2]/a")))
        self.driver.find_element(By.XPATH, "//*[@id='collapse-os mais buscados']/ul/li[2]/a").click()
        for i in range(2,5):
            self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='content-middle']/div[3]/div/div/div/div[1]/div")))
            count = self.driver.find_elements(By.XPATH, "//*[@id='content-middle']/div[3]/div/div/div/div[1]/div")
            for b in range(1, len(count)+1):
                self.wait.until((EC.element_to_be_clickable((By.XPATH, f"//*[@id='content-middle']/div[3]/div/div/div/div[1]/div[{b}]/div/div[2]/a"))))
                self.driver.find_element(By.XPATH, f"//*[@id='content-middle']/div[3]/div/div/div/div[1]/div[{b}]/div/div[2]/a").click()
                release_catalog['nome'].append(self.wait.until(EC.presence_of_element_located((By.ID, 'product-name-default'))).get_attribute("textContent"))
                release_catalog['categoria'].append(self.wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='content']/div/div/div[2]/div/section/div/div[1]/div/div[3]/a/div/span"))).get_attribute("textContent"))
                try:
                    release_catalog['subcategoria'].append(self.wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='content']/div/div/div[2]/div/section/div/div[1]/div/div[4]/a/div/span"))).get_attribute("textContent"))
                except:
                    release_catalog['subcategoria'].append('none')
                release_catalog['preco'].append(self.wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='content']/div/div/div[2]/div/section/div/div[2]/div[2]/div/div[1]/div/div[1]/div[1]/div/span"))).get_attribute("textContent"))
                print(release_catalog)
                self.driver.back()
                time.sleep(2)
            i += 1
            self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//*[@id='content-middle']/div[3]/div/div/div/div[2]/div/ul/li[{i}]/a"))).click()
            time.sleep(2)
        self.driver.quit()
        return release_catalog

    def write_release(self):
        data_rl = submarino.release(self)
        with open('release.csv', mode='w') as release_csv:
            catalog_rl = csv.writer(release_csv, delimiter = ',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for a in range(0, len(data_rl['nome'])):
                catalog_rl.writerow([data_rl['nome'][a], data_rl['categoria'][a], data_rl['subcategoria'][a], data_rl['preco'][a]])

    def write_bestseller(self):
        data_bs = submarino.best_sellers(self)
        with open('bestseller.csv', mode='w') as bestseller_csv:
            catalog_bs = csv.writer(bestseller_csv, delimiter = ',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for b in range(0, len(data_bs['nome'])):
                catalog_bs.writerow([data_bs['nome'][b], data_bs['categoria'][b], data_bs['subcategoria'][b], data_bs['preco'][b]])


if __name__ == '__main__':
    books = submarino().write_bestseller()
    print(books)