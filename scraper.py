import json
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ScraperFlow:
    def __init__(self):
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)
    
    def fetch_page(self, url):
        self.driver.get(url)
        return self.driver.page_source
    
    def parse_content(self, content):
        return BeautifulSoup(content, "html.parser")
    
    def get_total_count(text):
        count_match = re.search(r'\((\d+)\)', text)
        
        if count_match:
            total_count = int(count_match.group(1))
            return total_count
        else:
            return None
            
    #  FLOW ---- 1
    def get_list_of_search_space_data(self, url):
        content = self.fetch_page(url)
        content_soup = self.parse_content(content)
        
        data_main = content_soup.find('div', class_='spza_filterGroupContent')
        list_of_data = []

        if data_main:
            data_title = data_main.find_all('li',class_='filterPaneItemRoot')
            
            for list_item in data_title:
                a_tag = list_item.find('a')          
                item_title = a_tag.get_text()
                item_link = a_tag.get('href')
                
                if(item_title=="Get Started"):
                    continue
                
                element = self.driver.find_element(By.LINK_TEXT, item_title)
                element.click()
     
                try:
                    WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "childFilterGroup")))
                    updated_content = self.driver.page_source
                    updated_soup = self.parse_content(updated_content)
                    childFilterGroup = updated_soup.find(class_='childFilterGroup')
                    children_data = childFilterGroup.find_all('a')
                    self.get_list_of_childs(children_data=children_data)
                    self.driver.back()
                    WebDriverWait(self.driver, 10).until(EC.url_to_be(url))
                    
                except Exception as e:
                    self.driver.back()
                    element.click()
                    WebDriverWait(self.driver, 10).until(EC.url_to_be(url))

        return list_of_data
        

    #  FLOW ---- 2 
    def get_list_of_childs(self,children_data):    
         for child in children_data:
            child_title = child.get_text()
            child_link = child.get('href')
            if(child_title=="All"):
                continue
            element = self.driver.find_element(By.LINK_TEXT, child_title)
            element.click()
            # self.get_list_of_child_apps(self)
            
            
    # FLOW ---- 3
    def get_list_of_child_apps(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "spza_filteredTileContainer"))) 
        updated_content = self.driver.page_source
        updated_soup = self.parse_content(updated_content)
        list_of_apps = updated_soup.find(class_='spza_filteredTileContainer')
        apps_data = list_of_apps.find_all('a')
        print(apps_data)
     
                
    def close_driver(self):
        self.driver.quit()

    def run(self, url):
        list_of_search_space_data = self.get_list_of_search_space_data(url)
        self.close_driver()
        return list_of_search_space_data

# Usage
scraper = ScraperFlow()
data = scraper.run('https://azuremarketplace.microsoft.com/en-us/marketplace/apps')

