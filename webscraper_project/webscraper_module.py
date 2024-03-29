#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


class Webscraper:
    '''
    Class includes various methods to navigate through a website.
    '''

    def __init__(self, url: str = "https://www.myprotein.com/"):    #in future can put URL straight to nutrition page to save time
        #self.driver = webdriver.Chrome()

        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--no-sandbox')               # bypass some security features to allow the scraper to run inside the container
        self.options.add_argument('--disable-dev-shm-usage')    # disables memory sharing between host system and container
        self.options.add_argument('--disable-gpu')              # GPU can cause issues on Windows
        self.options.add_argument('--headless')
        self.options.add_argument('--window-size=1920,1080')
        self.options.add_argument('--disable-extensions')
        self.options.add_argument('--disable-infobars')
        self.options.add_argument('--disable-notifications')
        self.options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36') #sets my user agent
        
        self.driver = webdriver.Chrome(options = self.options) #set options first before initialising driver
  
        self.driver.get(url)
        self.driver.maximize_window()
        time.sleep(1)
    

    def _click_element(self, xpath: str):
        '''
        Finds a specific element on the webpage and clicks it.

        Parameters
        ---------
        xpath: str
            The xpath of the element to be clicked.
        '''
        time.sleep(2)

        element = self.driver.find_element(By.XPATH, xpath)
        element.click()

        return element


    def _find_element_in_container(self, xpath_container: str, tag_elements: str) -> list:
        '''
        Finds elements within a specifed container and stores them in a list.

        Parameters
        ----------
        xpath_container: str
            The xpath of the container.
        
        tag_elements: str
            The tag for the elements within the container.

        Returns
        -------
        elements_in_container: list
            A list of elements within the specified container.
        '''
        container = self.driver.find_element(By.XPATH, xpath_container)
        elements_in_container = container.find_elements(By.XPATH, f'./{tag_elements}')
        
        return elements_in_container


    def _scroll_website(self, scroll_height: int):
        '''
        Scrolls to a specified point on the website. 

        Parameters
        ----------
        scroll_height: int
            The desired height to scroll the webpage to.
        '''
        self.driver.execute_script(f"window.scrollTo(0, {scroll_height})")


    def _close_email_signup(self, xpath: str = '//button[@class="emailReengagement_close_button"]'):
        '''
        Open MyProtein and close email newletter sign up pop-up.

        Parameters
        -------
        xpath: str
            The xpath of the 'X' button to close the pop-up.

        '''       
        try:
            email_signup_button = self._click_element(xpath)
            print('Email sign-up closed...\n\n')
            time.sleep(1)
        except:
            pass
            
        return email_signup_button


    def _accept_cookies(self, xpath: str = '//button[@id="onetrust-accept-btn-handler"]'):       #old xpath is '//button[@class="cookie_modal_button"]'
        '''
        Accepts the cookies on the webpage.
        
        Parameters
        ----------
        xpath: str
            The xpath of the "Accept Cookies" button.
        '''
        try:
            accept_cookies_button = self._click_element(xpath)
            print('Cookies accepted...\n\n')
            time.sleep(1)
        except Exception as e: 
            print(e)

        return accept_cookies_button


    def _click_next_page(self, xpath: str = '//button[@aria-label="Next page"]'):
    #'//button[@class="responsivePaginationNavigationButton paginationNavigationButtonNext"]'):
        '''
        Clicks the 'Next' button to navigate to the next webpage.

        Parameters
        ----------
        xpath: str
            The xpath of the "Next" button.
        '''
        try:
            next_page_button = self._click_element(xpath)
        except:
            pass

        return next_page_button