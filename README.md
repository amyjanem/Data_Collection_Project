# Data_Collection_Project


> The purpose of this project was to use a website to collect and build a dataset from. This was be done using a webscraper.
> Include here a brief description of the project, what technologies are used etc.

## Milestone 1 & 2

- Milestone 1 & 2 simply involved setting up a GitHub repositary, and deciding on a website to collect from. I chose a website in the Health and Nutrition category as this is something I am passionate about. Thus the website I use in this project is MyProtein - a website selling all kinds of nutrition, supplements, workout clothing and more.


## Milestone 3

- In Milestone 3, the task was to set up Selenium to use as a webdriver. As I use a Chrome browser, Chromedriver was installed (this is different for Safari, Firefox etc). Chromedriver was then moved to the Python Path using: 

```python
echo $PATH
```
- Selenium was then installed and ready to use after entering the following into the command terminal:
```python
pip install
```


Does what you have built in this milestone connect to the previous one? If so explain how. What technologies are used? Why have you used them? Have you run any commands in the terminal? If so insert them using backticks (To get syntax highlighting for code snippets add the language after the first backticks).

- Example below:

```bash
/bin/kafka-topics.sh --list --zookeeper 127.0.0.1:2181
```

- The above command is used to check whether the topic has been created successfully, once confirmed the API script is edited to send data to the created kafka topic. The docker container has an attached volume which allows editing of files to persist on the container. The result of this is below:

```python
"""Insert your code here"""
```

- A scraper class was then created (WebScraper), along with methods to navigate the website such as to "Accept Cookies", 'X' any email newsletter sign up pop-up's, and click any buttons. These were made to be as general as possible to ensure reusability in future projects.

```python
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


    def close_email_signup(self, xpath: str = '//button[@class="emailReengagement_close_button"]'):
        '''
        Open MyProtein and close email newletter sign up pop-up

        Returns
        -------
        driver: webdriver.Chrome
            This driver is already in the MyProtein webpage
        '''       

        time.sleep(1) 
        self.click_element(xpath)        # TODO: ensure code still runs if pop-up doesn't appear - insert try and except clause. Try click_element(xpath), except pass

    
    def accept_cookies(self, xpath: str = '//button[@class="cookie_modal_button"]'):
        '''
        Accepts the cookies on the webpage
        
        Parameters
        ----------
        xpath: str
            The xpath of the "Accept Cookies" button
        '''

        time.sleep(1) 
        self.click_element(xpath)   # TODO: ensure code still runs if pop-up doesn't appear, use try/except clause
```

- Next, a method was created to retrieve links to products on the page and store them in a list. This was done by navigating to a page in the webiste, clicking a "View All" button so that all the products were visible, and then using a for loop to iterate through each item and retrieve their 'href' links to store within a list. This is shown in the code below:

 ```python 
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
        driver.execute_script("window.scrollTo(0, 1300)")
        time.sleep(1)
        nutrition_view_all = self.click_element(xpath)
        
    def find_product_links(self) -> list:
        '''
        Gets links to all products and stores the links to these in a list (product_link_list)
        '''
        product_link_list = []

        products = self.find_element_in_container('//ul[@class="productListProducts_products"]', 'li' )
        time.sleep(1)

        for product in products: 
            try:
                product_link = product.find_element(By.XPATH, './/div/div/a[@class="athenaProductBlock_linkImage"]').get_attribute('href')
                product_link_list.append(product_link)
            except:
                pass

        return product_link_list

 ```
- In find_product_links, the for-loop is within a try/except clause to avoid errors if an a-tag did not match the xpath specified.

- Lastly, the class is initialised within a if _ _ name _ _ == "__main__" block, so that it only runs if this file is run directly rather than on any import.
```python
if __name__ == "__main__":
    driver = webdriver.Chrome() 
    URL = "https://www.myprotein.com/"
    driver.get(URL)
    driver.maximize_window()

    scrape = Webscraper()
    scrape.close_email_signup()
    scrape.accept_cookies()
    scrape.nutrition_button_click()
    scrape.open_all_nutrition_products()
    scrape.find_product_links()
```

## Milestone 4
- This milestone involved scraping data from each product link that we obtained in the previous milestone. The information to be retrieved included the following: product name, price, rating, image link, and the time the data was scraped. Each product was also assigned a unique ID. 

- The product image was obtained using the following code:
```python
def get_product_image(self):
    '''
    Finds the href to the product image.

    '''
    time.sleep(1)
    product_image = self.driver.find_element(By.XPATH, '//img[@class="athenaProductImageCarousel_image"]').get_attribute('src')

    return product_image
```        
- The exact time of data scraping was obtaining using the following code:
```python
@staticmethod
def get_timestamp():
    '''
    Prints the timestamp of current time.
    '''
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")

    return current_time
```    
- Using the above code, the data for an individual product was scraped using the below:
```python
def get_product_data(self) -> dict:
    '''
    Finds xpath of product name, price, and rating of product and creates a dictionary of all the data.

    Parameters:
    -----------
    product_link: str
        the xpath of the url link to an individual product
    '''       
    product_dict = {}

    product_name = self.driver.find_element(By.XPATH, '//h1[@class="productName_title"]').text 

    product_price = self.driver.find_element(By.XPATH, '//p[@class="productPrice_price  "]').text

    try:
        product_rating = self.driver.find_element(By.XPATH, '//span[@class="athenaProductReviews_aggregateRatingValue"]').text
    except:
        product_rating = 'None'
        pass

    product_dict.update({
        "Product ID" : str(uuid.uuid4()),
        "Product Name" : product_name,
        "Price" : product_price,
        "Rating" : product_rating,
        "Time Scraped" : self.get_timestamp(),
        "Image Link" : self.get_product_image()            
        })

    return product_dict
```
- As seen above, the unique product ID was generated using 'str(uuid.uuid4())'
- 


## Milestone n

- Continue this process for every milestone, making sure to display clear understanding of each task and the concepts behind them as well as understanding of the technologies used.

- Also don't forget to include code snippets and screenshots of the system you are building, it gives proof as well as it being an easy way to evidence your experience!

## Conclusions

- Maybe write a conclusion to the project, what you understood about it and also how you would improve it or take it further.

- Read through your documentation, do you understand everything you've written? Is everything clear and cohesive?
