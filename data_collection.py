from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import uuid
import os
import json
import requests


class Webscraper:


    def __init__(self, url: str = "https://www.myprotein.com/"):
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        self.driver.maximize_window()
    
    
    def click_element(self, xpath: str):
        '''
        Finds a specific element on the webpage and clicks it.

        Parameters
        ---------
        xpath: str
            The xpath of the element to be clicked
        '''
        time.sleep(2)

        element = self.driver.find_element(By.XPATH, xpath)
        element.click()


    def find_element_in_container(self, xpath_container: str, tag_elements: str) -> list:
        '''
        Finds elements within a specifed container and stores them in a list.

        Parameters
        ----------
        xpath_container: str
            The xpath of the container
        
        tag_elements: str
            The tag for the elements within the container
        '''
        container = self.driver.find_element(By.XPATH, xpath_container)
        elements_in_container = container.find_elements(By.XPATH, f'./{tag_elements}')

        return elements_in_container


    def scroll_website(self, scroll_height: int):
        '''
        Scrolls to a specified point on the website. 

        Parameters:
        ----------
        scroll_height: int
            The desired height to scroll the webpage to.
        '''
        self.driver.execute_script(f"window.scrollTo(0, {scroll_height})")


    def close_email_signup(self, xpath: str = '//button[@class="emailReengagement_close_button"]'):
        '''
        Open MyProtein and close email newletter sign up pop-up

        Returns
        -------
        driver: webdriver.Chrome
            This driver is already in the MyProtein webpage
        '''       
        try:
            time.sleep(1) 
            self.click_element(xpath)
        except:
            pass
    

    def accept_cookies(self, xpath: str = '//button[@class="cookie_modal_button"]'):
        '''
        Accepts the cookies on the webpage
        
        Parameters
        ----------
        xpath: str
            The xpath of the "Accept Cookies" button
        '''
        try:
            time.sleep(1)
            self.click_element(xpath)
        except:
            pass



class MyProteinScraper(Webscraper):    


    def nutrition_button_click(self, xpath: str = '//a[@class="responsiveFlyoutMenu_levelOneLink responsiveFlyoutMenu_levelOneLink-hasChildren"]'):
        '''
        Finds 'Nutrition' catergory and clicks it.

        Parameters:
        -----------
        xpath: str
            The xpath of the nutrition button
        '''   
        time.sleep(1)
        nutrition_button = self.click_element(xpath)

        return nutrition_button
        

    def open_all_nutrition_products(self, xpath: str = '//a[@class="sectionPeek_allCta sectionPeek_allCta-show"]'):
        '''
        Clicks 'View All' button so that all Bestseller products are showing.

        Parameters:
        -----------
        xpath: str
            Xpath of the 'View All' button on the NUtrition webpage
        '''
        time.sleep(1)
        self.driver.execute_script("window.scrollTo(0, 1300)")
        time.sleep(1)
        nutrition_view_all = self.click_element(xpath)

        return nutrition_view_all
        

    def find_product_links(self) -> list:
        '''
        Gets links to all products and stores the links to these in a list (product_link_list)
        '''
        product_link_list = []

        products = self.find_element_in_container('//ul[@class="productListProducts_products"]', 'li' )
        time.sleep(1)

        for product in products: #finds each 'a' tag within list, finds the associated href (URL) and stores in a list
            try:
                product_link = product.find_element(By.XPATH, './/div/div/a[@class="athenaProductBlock_linkImage"]').get_attribute('href')
                product_link_list.append(product_link)
            except:
                pass

        return product_link_list


    def first_product_click(self):
        '''
        Clicks on the first product on the page. (for testing purposes for now!)
        '''
        time.sleep(1)
        first_product_link = self.click_element('//a[@class="athenaProductBlock_linkImage"]')
        time.sleep(1)

        return first_product_link


    def get_product_image(self):
        '''
        Finds the href to the product image.
        '''
        time.sleep(1)
        product_image = self.driver.find_element(By.XPATH, '//img[@class="athenaProductImageCarousel_image"]').get_attribute('src')

        return product_image


    @staticmethod
    def get_timestamp():
        '''
        Prints the timestamp of current time.
        '''
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        return current_time


    @staticmethod
    def get_date_and_timestamp():
        '''
        Prints the current date and time.
        '''
        now = datetime.now()
        full_datestamp = now.strftime("%d%m%Y_%H%M%S")

        return full_datestamp


    def get_product_data(self):
        '''
        Finds xpath of product name, price, and rating of product and creates a dictionary of all the data.

        Parameters:
        -----------
        product_link: str
            the xpath of the url link to an individual product
        '''       
        product_name = self.driver.find_element(By.XPATH, '//h1[@class="productName_title"]').text 
        
        product_price = self.driver.find_element(By.XPATH, '//p[@class="productPrice_price  "]').text

        try:
            product_rating = self.driver.find_element(By.XPATH, '//span[@class="athenaProductReviews_aggregateRatingValue"]').text
        except:
            product_rating = 'None'
            pass
        
        return product_name, product_price, product_rating


    def create_product_dict(self, product_name, product_price, product_rating) -> dict:     
        '''
        Creates a product dictionary using the below parameters.

        Parameters:
        -----------
        product_name:
            the name of the product

        product_price:
            the price of the product

        product_rating:
            the customer review rating of the product
        '''
        product_dict = {}

        product_dict.update({
            "Product ID" : str(uuid.uuid4()),
            "Product Name" : product_name,
            "Price" : product_price,
            "Rating" : product_rating,
            "Time Scraped" : self.get_timestamp(),
            "Image Link" : self.get_product_image()            
            })

        return product_dict


    def scrape_pages(self, product_link_list) -> list:
        '''
        Iterates through URL links on webpage and scrapes data from each, and stores the data in a list.
        

        Parameters:
        ----------
        product_link_list:
            list of URL's ("href" tags) for each product shown on the webpage.
        '''
        product_data_list_all= []   #list of product dictionaries
        
        #for link in range(len(product_link_list)): 
        for link in range(0,2):                        #for testing (be careful when removing as this will download ALL images - space on harddrive)
            
            product_link = product_link_list[link]
            self.driver.get(product_link)
            time.sleep(1)

            product_data = self.get_product_data()
                 
            filename = list(product_data.values())[0]   #indexes the product ID value and uses it for folder name   

            self.create_product_folder(filename)
            self.write_json(product_data, filename)     #writes the dictionary to a json file within the folder created above

            product_data_list_all.append(product_data)
                        
        return product_data_list_all


    def create_product_folder(self, filename):
        '''
        Creates a folder called 'raw_data' if it doesn't already exist, and then creates a folder within that, with the unique product ID as the filename.

        Parameters:
        -----------
        filename:
            The unique product ID of each product.
        '''
        if not os.path.exists('raw_data'):
            os.makedirs('raw_data')
            
        if not os.path.exists(f'raw_data/{filename}'):
            os.makedirs(f'raw_data/{filename}')


    def write_json(self, data, filename):
        '''
        Writes the dictionary data to a json file and saves it within it's own product folder.

        Parameters:
        -----------
        data:
            the product dictionary to be saved into the json format
        
        filename:
            the unique product ID to be used as a folder name.
        '''
        with open(f'raw_data/{filename}/data.json', 'w') as file:
            json.dump(data, file, indent = 4)   #indent = 4 makes the data more readable


    def download_image(self, image_src):
        '''
        Creates 'images' folder if it doesn't already exist, and then downloads and saves the relevant .jpg image within it with the product ID as the filename.

        Parameters:
        ----------
        image_src:
            the URL of the image to be downloaded
        '''
        if not os.path.exists('images'):
            os.makedirs('images')

        #image_src = self.get_product_image()        #to be this as parameter image_src when you call download_image
        image_src = requests.get(image_src).content

        image_filename = self.get_date_and_timestamp()

        with open(f'images/{image_filename}.jpg', 'wb') as file:     #wb means file is opened for writing in binary mode.
            file.write(image_src)



if __name__ == "__main__":

    scrape=MyProteinScraper()

    scrape.close_email_signup()
    scrape.accept_cookies()
    scrape.nutrition_button_click()
    scrape.open_all_nutrition_products()
    links = scrape.find_product_links()
    data_list_all = scrape.scrape_pages(links)
    data_list_all[] #'index the image link?'
    
    #Question: Trying to split up my scrape pages and download image methods. Scrape_pages iterates through product links and collects data, including the image jpg. 
    #Would the best way to get this link be to index each dictionary in the list to its image link, and then call download_images? Or another way?
    #Or better to keep in the scrape pages method

    #If indexing dictionary is the best way, how do I go about doing this?

    scrape.download_images()
    scrape.quit()
#   
#  #

#  #print(links)

#   #scrape.first_product_click()