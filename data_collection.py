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


    def close_email_signup(self):
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

        email_close_button = driver.find_element(By.XPATH, value = '//button[@class="emailReengagement_close_button"]')
        email_close_button.click()

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
        

driver = webdriver.Chrome() 
URL = "https://www.myprotein.com/"
driver.get(URL)

scrape = Webscraper()
scrape.close_email_signup()
scrape.accept_cookies()