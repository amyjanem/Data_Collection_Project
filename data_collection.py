from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import uuid

class Webscraper:


    def __init__(self, url: str = "https://www.myprotein.com/"):
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        self.driver.maximize_window()
    
    
    def click_element(self, xpath: str):
        '''
        Finds a specific element on the webpage and clicks it

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
        Finds elements within a specifed container and stores them in a list

        Parameters
        ----------
        xpath_container: str
            The xpath of the container
        
        tag_elements: str
            The tag for the elements within the container
        '''
        container = self.driver.find_element(By.XPATH, xpath_container)
        elements_in_container = container.find_elements(By.XPATH, f'./{tag_elements}')
        print(elements_in_container)

        return elements_in_container


    def scroll_website(self, scroll_height: int):
        '''
        Scrolls to a specified point on the website. #is this a static method, along with click and find element? **

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
        

    def find_product_links(self) -> list:
        '''
        Gets links to all products and stores the links to these in a list (product_link_list)

        '''
        product_link_list = []

        products = self.find_element_in_container('//ul[@class="productListProducts_products"]', 'li' )
        time.sleep(1)

        for product in products: #finds each 'a' tag within list, finds the associated href (URL) and stores in a list
            product_link = product.find_element(By.XPATH, './/a').get_attribute('href')
            product_link_list.append(product_link)

        return product_link_list


    def first_product_click(self):
        '''
        Clicks on the first product on the page. (for testing purposes for now!)
        '''
        time.sleep(1)
        first_product = self.click_element('//a[@class="athenaProductBlock_linkImage"]')
        time.sleep(1)



# TODO: Your dictionary should include all details for each record, its unique ID, timestamp of when it was scraped and links to any images associated with each record.

    def get_product_image(self):
        '''
        Finds the href to the product image?

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
        #print(current_time)

        return current_time


    def get_product_data(self, product_link) -> dict:
        '''
        Finds xpath of product name, price, and rating of product and creates a dictionary of all the data.

        Parameters:
        -----------
        product_link: str
            the xpath of the url link to an individual product
        '''
        self.driver.get(product_link)
        
        product_dict = {}
       
        product_name = self.driver.find_element(By.XPATH, '//h1[@class="productName_title"]').text 
        product_price = self.driver.find_element(By.XPATH, '//p[@class="productPrice_price  "]').text
        product_rating = self.driver.find_element(By.XPATH, '//span[@class="athenaProductReviews_aggregateRatingValue"]').text
        

        product_dict.update({
            "Product ID" : str(uuid.uuid4()),
            "Product Name" : product_name,
            "Price" : product_price,
            "Rating" : product_rating,
            "Time Scraped" : self.get_timestamp()
            })

        return product_dict


    def scrape_pages(self, product_link_list) -> list:

        product_data_list_all= []
        product_dict_all = {}

        for link in product_link_list:
            
            self.driver.get(link)

            product_data = self.get_product_data(link)
            product_dict_individual = product_dict_all.update(product_data)

            product_image = self.get_product_image()
            product_dict_individual = product_dict_all.update(product_image)

            timestamp = self.get_timestamp()
            product_dict_individual = product_dict_all.update(timestamp)

            product_data_list_all.append(product_dict_individual)

        return product_data_list_all




if __name__ == "__main__":

    scrape = MyProteinScraper()
    scrape.close_email_signup()
    scrape.accept_cookies()
    scrape.nutrition_button_click()
    scrape.open_all_nutrition_products()
    #links = scrape.find_product_links()
    #print(links)

    scrape.first_product_click()




