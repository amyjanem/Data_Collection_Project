from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
from datetime import datetime


class Webscraper:

    def click_element(self, xpath: str):
        '''
        Finds a specific element on the webpage and clicks it

        Parameters
        ---------
        xpath: str
            The xpath of the element to be clicked
        '''
        time.sleep(2)

        element = driver.find_element(By.XPATH, xpath)
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
        
        container = driver.find_element(By.XPATH, xpath_container)
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
        driver.execute_script(f"window.scrollTo(0, {scroll_height})")


    def close_email_signup(self, xpath: str = '//button[@class="emailReengagement_close_button"]'):
        '''
        Open MyProtein and close email newletter sign up pop-up

        Returns
        -------
        driver: webdriver.Chrome
            This driver is already in the MyProtein webpage
        '''       
        time.sleep(1) 
        try:
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
        time.sleep(1) 
        try:
            self.click_element(xpath)
        except:
            pass

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


    def open_all_nutrition_products(self, xpath: str = '//a[@class="sectionPeek_allCta sectionPeek_allCta-show"]'): #this can go in the MyProtein class which inherits from Webscraper
        '''
        Clicks 'View All' button so that all Bestseller products are showing.

        Parameters:
        -----------
        xpath: str
            Xpath of the 'View All' button on the NUtrition webpage
        '''
        
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, 1300)")
        time.sleep(1)
        nutrition_view_all = self.click_element(xpath)


    def find_product_links(self) -> list:
        '''
        Gets links to all products and stores the links to these in a list (product_link_list)

        Parameters:
        ----------
        xpath: str
            Xpath to each product
        
        xpath_container: str
            Xpath to the container of all products
        '''
        product_link_list = []

        products = self.find_element_in_container('//ul[@class="productListProducts_products"]', 'li' )
        time.sleep(1)

        for product in products: #finds each 'a' tag within list, finds the associated href (URL) and stores in a list
            product_link = product.find_element(By.XPATH, './/a').get_attribute('href')
            product_link_list.append(product_link)

        return product_link_list

    def first_product_click(self):
        first_product = scrape.click_element('//a[@class="athenaProductBlock_linkImage"]')





# TODO: Your dictionary should include all details for each record, its unique ID, timestamp of when it was scraped and links to any images associated with each record.

def get_product_data():
    '''
    Finds xpath of product name, price, and rating.
    '''
    product_dict = {}

    time.sleep(1)
    product_name = driver.find_element(By.XPATH, '//h1[@class="productName_title"]').text
    product_dict["Product Name"] = product_name

    time.sleep(1)
    product_price = driver.find_element(By.XPATH, '//p[@class="productPrice_price  "]').text
    product_dict["Product Price"] = product_price

    time.sleep(1)
    product_rating = driver.find_element(By.XPATH, '//span[@class="athenaProductReviews_aggregateRatingValue"]').text
    product_dict["Product Rating"] = product_rating

    print(product_dict)



def get_product_image():
    '''
    Finds the href to the product image and returns it??

    '''
    time.sleep(1)
    product_image = driver.find_element(By.XPATH, '//img[@class="athenaProductImageCarousel_image"]').get_attribute('src')

    return product_image


#@staticmethod
def get_timestamp():
    '''
    Prints the timestamp of current time.
    '''
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)


def create_dict():
    
    link_list = driver.find_product_links()
    product_dataset = get_product_data()
    #print(product_dataset)







if __name__ == "__main__":
    driver = webdriver.Chrome() 
    URL = "https://www.myprotein.com/"
    driver.get(URL)
    driver.maximize_window()

    scrape = Webscraper()
    scrape.close_email_signup()
    scrape.accept_cookies()
    #scrape.nutrition_button_click()
    #scrape.open_all_nutrition_products()
    #scrape.find_product_links()





# TODO: Your dictionary should include all details for each record, its unique ID, timestamp of when it was scraped and links to any images associated with each record.

# def get_product_image(self):
#     '''
#     Finds the href to the product image and returns it??

#     '''
#     time.sleep(1)
#     product_image = driver.find_element(By.XPATH, '//img[@class="athenaProductImageCarousel_image"]').get_attribute('src')

#     return product_image


# def get_product_price(self):
#     '''
#     Finds price of product and returns it?
#     '''
#     time.sleep(1)
#     product_price = driver. find_element(By.XPATH, '//p[@class="productPrice_price  "]')
#     print(product_price.text)
    
#     return product_price


# def get_product_rating(self):
#     '''
#     Finds rating of product and returns it?
#     '''
#     time.sleep(1)
#     product_rating = driver.find_element(By.XPATH, '//span[@class="athenaProductReviews_aggregateRatingValue"]')
#     print(product_rating.text)

#     return product_rating


def dict_name(self):

    product_2 = self.get_product_rating()



def get_product_info(self):
    '''
    Finds xpath of product name, price, rating and image link?
    '''
    
    time.sleep(1)
    product_name = driver.find_element(By.XPATH, '//h1[@class="productName_title"]').text
    #product_name.text

    time.sleep(1)
    product_price = driver.find_element(By.XPATH, '//p[@class="productPrice_price  "]').text
    #product_price.text

def get_product_name(self):
    '''
    Finds xpath of product name and returns it?
    '''
    time.sleep(1)
    product_name = driver. find_element(By.XPATH, '//h1[@class="productName_title"]')
    print(product_name.text)


def get_product_price(self):
    '''
    Finds price of product and returns it?
    '''
    time.sleep(1)
    product_price = driver. find_element(By.XPATH, '//p[@class="productPrice_price  "]')
    print(product_price.text)
    
def get_product_rating(self):
    '''
    Finds rating of product and returns it?
    '''
    time.sleep(1)
    product_rating = driver.find_element(By.XPATH, '//span[@class="athenaProductReviews_aggregateRatingValue"]')
    print(product_rating.text)



get_product_image()
get_product_name()
get_product_price()
get_product_rating()