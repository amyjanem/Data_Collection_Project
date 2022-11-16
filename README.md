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

- A scraper class was then created (WebScraper), along with methods to navigate the website such as to "Accept Cookies", 'X' any email newsletter sign up pop-up's, and click any buttons. These were made to be as general as possible to ensure reusability in future projects.

```python
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
```

- The following code was then created within another class, MyProteinScraper, as shown below, which inherits from the WebScraper class. The code within this class is specific to the MyProtein website, whereas the code in the WebScraper class is more generalised and can be used to scrape other websites with only minor edits to the code.
```python
class MyProteinScraper(Webscraper):  
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
- In find_product_links above, the for-loop is within a try/except clause to avoid errors if an a-tag did not match the xpath specified.

- Lastly, the class is initialised within a if _ _ name _ _ == "__main__" block, so that it only runs if this file is run directly rather than on any import. It is set such that the cookies are accepted and the email newletter pop-up are automatically closed once the code is run.
```python
if __name__ == "__main__":

    scrape=MyProteinScraper()

    scrape.close_email_signup()
    scrape.accept_cookies()
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

- The exact time of data scraping was obtaining using the static method below:
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

- Using the above methods, the data for an individual product was scraped using the below:
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

- In order to scrape multiple products on the webpage, a method was created to iterate through the list of links we obtained in the previous milestone (using the find_product_links() method), and obtain the relevant data as well as download the associated jpg image. The product dictionary is saved in a json format to a folder with it's unique product ID as the name. The images are saved in a separate images folder with the filenames in the <date>_<time>_<order of image>.jpg format.

```python
    @staticmethod
    def get_date_and_timestamp():
        '''
        Prints the current date and time.
        '''
        now = datetime.now()
        full_datestamp = now.strftime("%d%m%Y_%H%M%S")

        return full_datestamp
    
    
    def scrape_pages(self, product_link_list) -> list:
        '''
        Iterates through URL links on webpage and scrape data from each, and stores the data in a list.
        Method also downloads the associated image and stores in a folder with the product ID as the filename.

        Parameters:
        ----------
        product_link_list:
            list of URL's ("href" tags) for each product shown on the webpage.
        '''
        product_data_list_all= []   #list of product dictionaries

        for link in range(len(product_link_list)): 

            product_link = product_link_list[link]
            self.driver.get(product_link)

            time.sleep(1)

            product_data = self.get_product_data()

            filename = list(product_data.values())[0]   #indexes the product ID value and uses it for folder name   

            self.create_product_folder(filename)

            self.write_json(product_data, filename)     #writes the dictionary to a json file within the folder created above

            image_src = self.get_product_image()        #finds and downloads the image before saving it
            image_filename = self.get_date_and_timestamp()
            self.download_image(image_src, image_filename)

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
            json.dump(data, file, indent = 4)   


    def download_image(self, image_src, filename):
        '''
        Creates images folder if it doesn't already exist, and then downloads and saves the relevant .jpg image within it.

        Parameters:
        ----------
        image_src:
            the URL of the image to be downloaded
        product_id:
            the unique product ID to be used as the filename for the image
        '''
        if not os.path.exists('images'):
            os.makedirs('images')

        image_src = requests.get(image_src).content

        with open(f'images/{filename}.jpg', 'wb') as file:     
            file.write(image_src)    
```


## Milestone n

- Continue this process for every milestone, making sure to display clear understanding of each task and the concepts behind them as well as understanding of the technologies used.

- Also don't forget to include code snippets and screenshots of the system you are building, it gives proof as well as it being an easy way to evidence your experience!

## Conclusions

- Maybe write a conclusion to the project, what you understood about it and also how you would improve it or take it further.

- Read through your documentation, do you understand everything you've written? Is everything clear and cohesive?
