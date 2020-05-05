import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from login import login_data
import csv

photos = {'URL': [], 'Likes': [], 'Date': []}


class insta:
    def __init__(self):
        self.driver = webdriver.Chrome('/home/semantix/SeleniumDriver/chromedriver_linux64/chromedriver')
        self.driver.get('https://www.instagram.com/')
        self.wait = WebDriverWait(self.driver, 5)

    def login(self):
        self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
        username = self.driver.find_element_by_name("username")
        password = self.driver.find_element_by_name("password")
        username.send_keys(login_data.username)
        password.send_keys(login_data.password)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='react-root']/section/main/article/div[2]/div[1]/div/form/div[4]/button")))
        self.driver.find_element(By.XPATH, "//*[@id='react-root']/section/main/article/div[2]/div[1]/div/form/div[4]/button").click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div/div[3]/button[1]")))
        self.driver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[3]/button[1]").click()
        time.sleep(1)


    def search(self, profile):
        insta.login(self)
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='react-root']/section/nav/div[2]/div/div/div[2]/input")))
        srch =  self.driver.find_element(By.XPATH, "//*[@id='react-root']/section/nav/div[2]/div/div/div[2]/input")
        srch.send_keys(profile)
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='react-root']/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]")))
        self.driver.find_element(By.XPATH, "//*[@id='react-root']/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]").click()
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='react-root']/section/main/div/div[1]/a[1]")))
            self.driver.find_element(By.XPATH, "//*[@id='react-root']/section/main/div/div[1]/a[1]").click()
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='react-root']/section/main/div/header/section/ul/li[1]/span/span")))
            photo_count = str(self.driver.find_element(By.XPATH, "//*[@id='react-root']/section/main/div/header/section/ul/li[1]/span/span").get_attribute("textContent"))
            photo_count = photo_count.replace('.','')
            self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//*[@id='react-root']/section/main/div/div[2]/article/div/div/div/div[1]/a/div/div[2]")))
            self.driver.find_element(By.XPATH,f"//*[@id='react-root']/section/main/div/div[2]/article/div/div/div/div[1]/a/div/div[2]").click()
        except:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='react-root']/section/main/div/div[2]/a[1]")))
            self.driver.find_element(By.XPATH, "//*[@id='react-root']/section/main/div/div[2]/a[1]").click()
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='react-root']/section/main/div/header/section/ul/li[1]/span/span")))
            photo_count = str(self.driver.find_element(By.XPATH,"//*[@id='react-root']/section/main/div/header/section/ul/li[1]/span/span").get_attribute("textContent"))
            photo_count = photo_count.replace('.', '')
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='react-root']/section/main/div/div[3]/article/div[1]/div/div[1]/div[1]/a/div/div[2]")))
            self.driver.find_element(By.XPATH,"//*[@id='react-root']/section/main/div/div[3]/article/div[1]/div/div[1]/div[1]/a/div/div[2]").click()
        for a in range(0, int(photo_count)):
            try:
                self.wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div[2]/div/article/div[2]/section[2]/div/div[2]/button/span")))
                likes = str(self.driver.find_element(By.XPATH,"/html/body/div[4]/div[2]/div/article/div[2]/section[2]/div/div[2]/button/span").get_attribute("textContent"))
                likes = int(likes.replace('.',''))
                likes += 1
            except:
                self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[2]/div/article/div[2]/section[2]/div/span")))
                self.driver.find_element(By.XPATH,"/html/body/div[4]/div[2]/div/article/div[2]/section[2]/div/span").click()
                self.wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div[2]/div/article/div[2]/section[2]/div/div/div[4]/span")))
                likes = str(self.driver.find_element(By.XPATH,"/html/body/div[4]/div[2]/div/article/div[2]/section[2]/div/div/div[4]/span").get_attribute("textContent"))
                likes = likes.replace('.','')
                self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[2]/div/article/div[2]/section[2]/div/div/div[1]")))
                self.driver.find_element(By.XPATH,"/html/body/div[4]/div[2]/div/article/div[2]/section[2]/div/div/div[1]").click()
            self.wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div[2]/div/article/div[2]/div[2]/a/time")))
            date = self.driver.find_element(By.XPATH,"/html/body/div[4]/div[2]/div/article/div[2]/div[2]/a/time").get_attribute("title")
            url = self.driver.current_url
            if a == 0:
                self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[1]/div/div/a")))
                self.driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div/div/a").click()
            elif a == int(photo_count)-1:
                self.driver.quit()
            else:
                self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[1]/div/div/a[2]")))
                self.driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div/div/a[2]").click()
            photos['URL'].append(url)
            photos['Likes'].append(likes)
            photos['Date'].append(date)
        return photos

    def write(self, profile):
        db = insta.search(self, profile)
        with open(f'{profile}.csv', mode='w') as profile_csv:
            profile_data = csv.writer(profile_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for b in range(0, len(photos['URL'])):
                profile_data.writerow([db['URL'][b], db['Likes'][b], db['Date'][b]])


if __name__ == '__main__':
    profile = 'semantixbr'
    a = insta().write(profile)
    print(a)
