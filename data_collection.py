from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


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


    def close_email_signup(self, xpath: str = '//button[@class="emailReengagement_close_button"]'):
        '''
        Open MyProtein and close email newletter sign up pop-up

        Returns
        -------
        driver: webdriver.Chrome
            This driver is already in the MyProtein webpage
        '''       

        time.sleep(2) 

        #delay  = 10
        #self.WebDriverWait(driver, delay).until(EC.presence_of_element_located(By.XPATH, value = '//button[@class="cookie_modal_button"]'))

        self.click_element(xpath)

        #self.click_element(xpath) # TODO: ensure code still runs if pop-up doesn't appear

    
    def accept_cookies(self, xpath: str = '//button[@class="cookie_modal_button"]'):
        '''
        Accepts the cookies on the webpage
        
        Parameters
        ----------
        xpath: str
            The xpath of the "Accept Cookies" button
        '''

        time.sleep(2) 

        self.click_element(xpath)   # TODO: ensure code still runs if pop-up doesn't appear
        

    def find_element_in_container(self, xpath_container: str, tag_elements: str) -> list:
        '''
        Finds elements within a specifed container and them in a list

        Parameters
        ----------
        xpath_container: str
            The xpath of the container
        
        tag_elements: str
            The tag for the elements within the container
        '''
        
        container = self.driver.find_element(By.XPATH, xpath_container)
        elements_in_container = container.find_elements(By.XPATH, f'/{tag_elements}')

        return elements_in_container
        
    def find_pages_links(self, xpath_container: str, tag_elements: str) -> list:
        page_link_list = []
        self.find_element_in_container('//ul[@class="responsiveFlyoutMenu_levelOne "]', 'li')

        for page in page

driver = webdriver.Chrome() 
URL = "https://www.myprotein.com/"
driver.get(URL)

scrape = Webscraper()
scrape.close_email_signup()
scrape.accept_cookies()