from datetime import datetime
import json
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import uuid
from webscraper_module import Webscraper


class MyProteinScraper(Webscraper):    


    def _nutrition_button_click(self, xpath: str = '//a[@class="responsiveFlyoutMenu_levelOneLink responsiveFlyoutMenu_levelOneLink-hasChildren"]'):
        '''
        Finds 'Nutrition' catergory button and clicks it.

        Parameters
        -----------
        xpath: str
            The xpath of the nutrition button.
        '''   
        time.sleep(1)
        nutrition_button = self.click_element(xpath)

        return nutrition_button
        

    def _open_all_nutrition_products(self, xpath: str = '//a[@class="sectionPeek_allCta sectionPeek_allCta-show"]'):
        '''
        Clicks 'View All' button so that all Bestseller products are showing.

        Parameters
        -----------
        xpath: str
            Xpath of the 'View All' button on the NUtrition webpage.
        '''
        time.sleep(1)
        self.driver.execute_script("window.scrollTo(0, 1300)")
        time.sleep(1)
        nutrition_view_all = self.click_element(xpath)

        return nutrition_view_all
        

    def _find_product_links(self) -> list:
        '''
        Gets links to all products and stores these in a list.

        Returns
        -------
        product_link_list: list
            A list of the URL links to each product on the page.
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


    def _first_product_click(self):
        '''
        Clicks on the first product on the page. 
        '''
        time.sleep(1)
        first_product_link = self.click_element('//a[@class="athenaProductBlock_linkImage"]')
        time.sleep(1)

        return first_product_link


    def _get_product_image(self):
        '''
        Finds the 'href' (ie. link) to the product image.

        Returns
        -------
        product_image: str
            the URL link to the product image.
        '''
        time.sleep(1)
        product_image = self.driver.find_element(By.XPATH, '//img[@class="athenaProductImageCarousel_image"]').get_attribute('src')

        return product_image


    @staticmethod
    def _get_timestamp():
        '''
        Determines the current time and prints it in hours : minutes : seconds format.

        Returns
        -------
        current_time: str
            The current time
        '''
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        return current_time


    @staticmethod
    def _get_date_and_timestamp():
        '''
        Determines the current date and time and prints it in 'day month year _ hour minute second' format.

        Returns
        -------
        full_datestamp: str
            The current time
        '''
        now = datetime.now()
        full_datestamp = now.strftime("%d%m%Y_%H%M%S")

        return full_datestamp


    def _get_product_data(self):
        '''
        Finds xpath of product name, price, and rating of product and converts the information to a string format.

        Returns
        -------
        product_name: str
            The name of the product.
        
        product_price: str
            The price of the product.
        
        product_rating: str
            The ratings of the product.
        '''       
        product_name = self.driver.find_element(By.XPATH, '//h1[@class="productName_title"]').text 
        product_price = self.driver.find_element(By.XPATH, '//p[@class="productPrice_price  "]').text

        try:
            product_rating = self.driver.find_element(By.XPATH, '//span[@class="athenaProductReviews_aggregateRatingValue"]').text
        except:
            product_rating = 'None'
            pass
        
        return product_name, product_price, product_rating


    def _create_product_dict(self, product_name, product_price, product_rating) -> dict:     
        '''
        Creates a product dictionary using the below parameters.

        Parameters
        -----------
        product_name: str
            The name of the product.

        product_price: str
            The price of the product.

        product_rating: str
            The customer review rating of the product.

        Returns
        -------
        product_dict: dict
            A dictionary of the product data containing name, price and rating.
        '''
        product_dict = {}

        product_dict.update({
            "Product ID" : str(uuid.uuid4()),
            "Product Name" : product_name,
            "Price" : product_price,
            "Rating" : product_rating,
            "Time Scraped" : self._get_timestamp(),
            "Image Link" : self._get_product_image()            
            })

        return product_dict


    @staticmethod
    def _create_product_folder(filename):
        '''
        Creates a folder called 'raw_data' if it doesn't already exist, and then creates a folder within that, with the unique product ID as the filename.

        Parameters
        ----------
        filename: str
            The unique product ID of each product.
        '''
        if not os.path.exists('raw_data'):
            os.makedirs('raw_data')
            
        if not os.path.exists(f'raw_data/{filename}'):
            os.makedirs(f'raw_data/{filename}')


    def _write_json(self, data, filename):
        '''
        Writes the dictionary data to a json file and saves it within it's own product folder.

        Parameters
        ----------
        data: dict
            The product dictionary to be saved into the json format.
        
        filename: str
            The unique product ID.
        '''
        with open(f'raw_data/{filename}/data.json', 'w') as file:
            json.dump(data, file, indent = 4)   #indent = 4 makes the data more readable


    @staticmethod
    def _create_image_folder(filename):
        '''
        Creates 'images' folder if it doesn't already exist.
        
        Parameters
        ----------
        filename: str
            The unique product ID.
        '''
        if not os.path.exists(f'raw_data/{filename}/images'):
            os.makedirs(f'raw_data/{filename}/images')


    def _download_image(self, image_src, filename):
        '''
        Downloads and saves the relevant .jpg image within it with the product ID as the filename.

        Parameters
        ----------
        image_src: str
            The URL of the image to be downloaded.
        
        filename: str
            The unique product ID.
        '''
        image_src = requests.get(image_src).content
        image_filename = self._get_date_and_timestamp()

        with open(f'raw_data/{filename}/images/{image_filename}.jpg', 'wb') as file:     #wb means file is opened for writing in binary mode.
            file.write(image_src)


    def scraper(self, product_links):
        '''
        THe webscraper for one webpage, which iterates through URL links to find and save relevant product and image data from each.
        
        Parameters
        ----------
        product_links: list
            The list of product URLs to all products on the webpage.

        Returns
        -------
        product_data_list_all: list
            A list of dictionaries of the product data
        '''
        product_data_list_all= []                       #list of product dictionaries
        
        #for link in range(len(product_links)): 
        for link in range(0,2):                         #for testing (be careful when removing as this will download ALL images - space on harddrive)

            product_link = product_links[link]
            self.driver.get(product_link)
            time.sleep(1)

            product_data = self._get_product_data()
            product_dict = self._create_product_dict(product_data[0], product_data[1], product_data[2])

            filename = list(product_dict.values())[0]    #indexes the product ID value and uses it for folder name   

            self._create_product_folder(filename)
            self._write_json(product_data, filename)     #writes the dictionary to a json file within the folder created above

            product_data_list_all.append(product_data)

            self._create_image_folder(filename)
            image = self._get_product_image()
            self._download_image(image, filename)
        
        return product_data_list_all


if __name__ == "__main__":

    scrape=MyProteinScraper()

    scrape.close_email_signup()
    scrape.accept_cookies()
    scrape._nutrition_button_click()
    scrape._open_all_nutrition_products()
    
    pages = scrape.driver.find_element(By.XPATH, '//li/a[@class="responsivePaginationButton responsivePageSelector   responsivePaginationButton--last"]').text

    #for page in range(1, 3):                   #for testing
    for page in range(1, int(pages) + 1):
        links = scrape._find_product_links()
        time.sleep(2)

        scrape.scraper(links)
        time.sleep(2)

        scrape.driver.get(f'https://www.myprotein.com/nutrition/bestsellers-en-gb.list?pageNumber={page}')
        time.sleep(2)

        try:
            WebDriverWait(scrape, 5).until(EC.presence_of_element_located((By.XPATH, '//button[@class="responsivePaginationNavigationButton paginationNavigationButtonNext"]')))
            scrape.click_next_page()
            time.sleep(2)
        except:
            scrape.driver.quit()
