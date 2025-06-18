# from urllib.request import urlopen
from selenium import webdriver
import time
from selenium.webdriver import chrome
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

service = Service(ChromeDriverManager().install())
option = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=option)


driver.get("https://ctf.cgii.gob.bo/")
time.sleep(4)

search_box = driver.find_element(By.XPATH, "/html/body/nav/div/div/ul[1]/li[5]/a").click()

time.sleep(4)
driver.quit()


