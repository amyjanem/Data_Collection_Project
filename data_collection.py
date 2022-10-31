from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class Webscraper:

    def close_email_signup(self):

        '''
        Open MyProtein and close email newletter sign up pop-up

        Returns
        -------
        driver: webdriver.Chrome
            This driver is already in the MyProtein webpage
        '''       

        time.sleep(3) 

        accept_email_signup_button = driver.find_element(by=By.XPATH, value='//button[@class="emailReengagement_close_button"]')
        accept_email_signup_button.click()
        time.sleep(2)

        return driver 
    
    
    
    def accept_cookies(self) -> webdriver.Chrome:
        '''
        Accepts the cookies on the webpage
        
        Returns
        -------
        driver: webdriver.Chrome
            This driver is already in the MyProtein webpage
        '''

        time.sleep(2) 

        accept_cookies_button = driver.find_element(by=By.XPATH, value='//button[@class="cookie_modal_button"]')
        accept_cookies_button.click()
        
        time.sleep(2)



        return driver 
        

driver = webdriver.Chrome() 
URL = "https://www.myprotein.com/"
driver.get(URL)

scrape = Webscraper()
scrape.close_email_signup()
scrape.accept_cookies()

