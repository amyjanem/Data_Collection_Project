# Data_Collection_Project

An implementation of an industry grade data collection pipeline that runs scalably in the cloud. It uses Python code to automatically control your browser, extract information from a website, and store it on the cloud in a data warehouses and data lake. The system conforms to industry best practices such as being containerised in Docker and running automated tests.

## Milestone 1 & 2

- Milestone 1 & 2 simply involved setting up a GitHub repositary, and deciding on a website to collect from. I chose a website in the Health and Nutrition category as this is something I am passionate about. Thus the website I use in this project is MyProtein.com - a website selling all kinds of nutrition, supplements, workout clothing and more.


## Milestone 3

- In Milestone 3, the task was to set up Selenium to use as a webdriver. As I use a Chrome browser, Chromedriver was installed (this is different for Safari, Firefox etc). Chromedriver was then moved to the Python Path using: 

```python
echo $PATH
```
- Selenium was then installed and ready to use after entering the following into the command terminal:
```python
pip install
```

- A scraper class was then created (WebScraper), along with methods to navigate the website such as to "Accept Cookies", close any email newsletter sign up pop-up's, and click any buttons. These were made to be as general as possible to ensure reusability in future projects. A couple of examples of these can be seen below:

```python   
      
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

- Another class called MyProteinScraper was created, as shown below, which inherits from the WebScraper class. The code within this class is specific to the MyProtein website, whereas the code in the WebScraper class is more generalised and can be used to scrape other websites with only minor edits to the code.
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
- This milestone involved scraping data from each product link that was obtained in the previous milestone. The information to be retrieved included the following: product name, price, rating, image link, and the time the data was scraped. Each product was also assigned a unique ID. 

- The product image was obtained using the following code:
```python    
    def _get_product_image(self) -> str:
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
```

- The exact time of data scraping was obtaining using the static method below:
```python       
    @staticmethod
    def _get_timestamp() -> str:
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
```  

- Using the above methods, the data for an individual product was scraped using the below:
```python            
    def _get_product_data(self) -> str:
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
        
        
    def create_product_dict(self, product_name, product_price, product_rating) -> dict:     
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
```

- As seen above, the unique product ID was generated using 'str(uuid.uuid4())'

- In order to scrape multiple products on the webpage, a method was created to iterate through the list of links we obtained in the previous milestone (using the find_product_links() method), and obtain the relevant data as well as download the associated jpg image. The product dictionary is saved in a json format to a folder with it's unique product ID as the name. The images are saved in a separate images folder with the filenames in the <date>_<time>_<order of image>.jpg format.

```python    
    @staticmethod
    def _get_date_and_timestamp() -> str:
        '''
        Determines the current date and time and prints it in 'DayMonthYear_HourMinuteSecond' format.

        Returns
        -------
        full_datestamp: str
            The current time
        '''
        now = datetime.now()
        full_datestamp = now.strftime("%d%m%Y_%H%M%S")

        return full_datestamp
    
    
    @staticmethod
    def create_product_folder(filename):
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


    def write_json(self, data, filename):
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
    def create_image_folder(filename):
        '''
        Creates 'images' folder if it doesn't already exist.
        
        Parameters
        ----------
        filename: str
            The unique product ID.
        '''
        if not os.path.exists(f'raw_data/{filename}/images'):
            os.makedirs(f'raw_data/{filename}/images')


    def download_image(self, image_src, filename):
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


    def scrape_one_page(self, product_links) -> list:
        '''
        The webscraper for one webpage, which iterates through URL links to find and save relevant product and image data from each.
        
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
        
        for link in range(len(product_links)): 
        #for link in range(0,2):                        #for testing due to harddrive space - will download all images otherwise

            product_link = product_links[link]
            self.driver.get(product_link)
            time.sleep(1)

            product_data = self._get_product_data()
            product_dict = self.create_product_dict(product_data[0], product_data[1], product_data[2])

            filename = list(product_dict.values())[0]   #indexes the product ID value and uses it for folder name   

            self.create_product_folder(filename)
            self.write_json(product_data, filename)     #writes the dictionary to a json file within the folder created above
            print('Product folders created, and product data saved... \n\n')

            product_data_list_all.append(product_data)

            self.create_image_folder(filename)
            image = self._get_product_image()
            self.download_image(image, filename)
            print('Product image downloaded and saved...\n\n')
        
        return product_data_list_all


    def scrape_all_pages(self, pages_num):
        '''
        The webscraper for a specified number of pages, navigates to new pages and scrapes it using the above scrape_one_page method before moving on to the next one.
        
        Parameters
        ----------
        pages_num: int
            The desired number of pages to be scraped.
        '''    
        total_pages = self.driver.find_element(By.XPATH, '//li/a[@class="responsivePaginationButton responsivePageSelector   responsivePaginationButton--last"]').text      #the total amount of pages that can be scraped

        #for page in range(1, int(total_pages) + 1):     #test all pages
        for page in range(1, pages_num + 1):             #scrape specified amount of pages
            links = self._find_product_links()
            print('Product links found...\n\n')
            time.sleep(2)

            self.scrape_one_page(links)
            print('Page scraped... \n\n')
            time.sleep(2)

            self.driver.get(f'https://www.myprotein.com/nutrition/bestsellers-en-gb.list?pageNumber={page}')
            time.sleep(2)

            try:
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Next page"]')))   
                time.sleep(2)
                self._click_next_page()
                print('Next page clicked...\n\n')
                time.sleep(2)
            except:
                print('Quitting page now...\n\n')
                self.driver.quit()
```

## Milestone 5

This milestone was all about optimising code, and setting up testing for the code using unit tests to ensure each part worked as desired.

- The code was first refactored and optimised by doing the following:
    - Methods were made sure to be appropriately named, and clear
    - Repeated code was closely scrutinised and optimised
    - Methods were ensured to have one concern where possible, for simplification and ease of testing
    - Methods were made private where necessary (more on this below)
    - Docstrings were ensured to be consistent throughout all methods
    - Nested loops were broken up where necessary
    
 

- The following methods were kept as public, whereas the remainder of the methods were made private:
    - create_product_dict, create_product_folder, write_json, create_image_folder, download_image, scrape_one_page, and scrape_all_pages

- The if __name__ = '__main__' block was also updated to the below:
```python 
    if __name__ == "__main__":          
    
    scrape = MyProteinScraper()

    scrape._close_email_signup()        
    scrape._accept_cookies()            
    scrape._nutrition_button_click()
    scrape._open_all_nutrition_products()
    scrape.scrape_all_pages(2)
```

- A file was then created to insert all of the unit tests into. The unit tests tested all of the public methods and this can be seen below:
```python
import unittest
import os
import shutil
import sys
sys.path.append(r"C:\Users\amyma\AiCore Projects\Data_Collection_Project")
from myprotein_scraper import MyProteinScraper


class TestMyProteinScraper_1(unittest.TestCase):
    

    def setUp(self):
        self.scrape = MyProteinScraper()             
        self.scrape._close_email_signup()            
        self.scrape._accept_cookies()
        self.scrape._nutrition_button_click()
        self.scrape._open_all_nutrition_products()
        print('setUp method called...\n\n')          

def test_create_product_dict(self):                 
        self.scrape._first_product_click()
        test_dict = self.scrape.create_product_dict('test_name', 'test_price', 'test_rating')
        self.assertIsInstance(test_dict, dict)
        print('create_product_dict returns a dictionary')

    def test_scrape_one_page(self):                 
        link_list = self.scrape._find_product_links()
        link_length = len(link_list)

        test_function_list = self.scrape.scrape_one_page(link_list)
        test_function_list_length = len(test_function_list)

        self.assertEqual(link_length, test_function_list_length)


    def test_scrape_all_pages(self):        #testing that the correct number of folders were created (and essentially that they were indeed created)
        products_per_page = len(self.scrape._find_product_links())
        test_pages_num = 1
        self.scrape.scrape_all_pages(test_pages_num)

        lst = os.listdir('raw_data')
        expected_number_files = len(lst)
        print(expected_number_files)
        actual_number_files = products_per_page * test_pages_num

        self.assertEqual(expected_number_files, actual_number_files)

        test_file = lst[1]          #random file to be read
        with open(f'raw_data/{test_file}/data.json', 'r') as file:
            data_text = file.read() 

        #testing that the images were downloaded correctly
        with open("raw_data/{test_file}/images/*.jpg" ,'wb'):
            pass

    def tearDown(self):
        self.scrape.driver.quit()


class TestMyProteinScraper_2(unittest.TestCase):


    def setUp(self):
        self.scrape = MyProteinScraper()

    def test_create_image_folder(self):            #pass
        random_directory = os.makedirs('random_name') 
        self.scrape.create_image_folder(random_directory)

        self.assertTrue(os.path.exists('raw_data/{random_directory}/images'), 'Image folder path does not exist')

    def test_create_product_folder(self):          #pass           
        self.scrape.create_product_folder('random_name')

        self.assertTrue(os.path.exists('raw_data/random_name'), 'Product folder path does not exist')
        #os.rmdir('raw_data/random_name')

    def test_write_json(self):                     #pass                      
        os.makedirs('raw_data/test_filename')

        self.scrape.write_json({'Price' : '£10.50'}, 'test_filename')
        self.assertTrue(os.path.exists('raw_data/test_filename/data.json'), 'Directory path is incorrect/does not exist')

        os.remove(f'raw_data/test_filename/data.json')
        os.rmdir(f'raw_data/test_filename')


    def test_download_image(self):                   #pass
        test_image_src = "http://t2.gstatic.com/licensed-image?q=tbn:ANd9GcQOO0X7mMnoYz-e9Zdc6Pe6Wz7Ow1DcvhEiaex5aSv6QJDoCtcooqA7UUbjrphvjlIc"
        test_image_filename = 'test_image_filename'
        
        os.makedirs('raw_data/test_image_filename/images')
        self.scrape.download_image(test_image_src, test_image_filename)

        self.assertTrue(os.path.exists(f'raw_data/{test_image_filename}/images/{self.scrape._get_date_and_timestamp()}.jpg'))  


    def tearDown(self):    
        shutil.rmtree('raw_data')   


if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)
```


## Milestone 6

-     This milestone involved containerising the scraper, ie. taking steps to running the system on the cloud and packaging it together in a self-contained unit.

-     First the code was analysed to be refactored for the final time. It was made sure to check whether the code could have been laid out better. This included looking at methods and variables to see if they were named appropriately, looking for any repitition and correcting it, ensuring methods had only one concern where possible and if not breaking it up into multiple methods, making methods private or protected where necessary, removing nested loops, and ensuring docstrings were consistent.
      
 -    It was then checked that all unit tests were passing and if not, correcting them appropriately.
      
 -    Some options were then added to the scraper, which can be seen below, such as to be run in headless mode as this will be needed in order to be run in a Docker container:
      
```python
   def __init__(self, url: str = "https://www.myprotein.com/"):    

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
```      
      
 - A Dockerfile was then created in order to build the image of the scraper. This used a base image of Python, set the working directory, and copied the relevant files from where the image was being built into the container.

```python
FROM python:3.9.7

WORKDIR data_collection_project 

COPY . .

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

#install chromedriver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN apt-get install -yqq unzip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

#install requirements (this can be done using a requirements.txt file too)
RUN pip3 --version
RUN python -m pip install selenium 
RUN python -m pip install requests
RUN python -m pip install --upgrade pip

CMD ["python", "webscraper_project/myprotein_scraper.py"]
```      
-     The image was then built using 'docker build -t my_protein_image:1.0 .', and then run using 'docker run my_protein_image'
      
-     DockerHub was then logged into and the image was pushed to DockerHub using 'docker push'.
      
      
## Milestone 7
      
-     This milestone invloved setting up a CI/CD pipeline to build and deploy the image to DockerHub.
      
-     CI/CD means continuous integration and continuous delivery/continuous deployment.

-     This was startedby setting up the relevant GitHub secrets (namely DOCKERHUB_USERNAME and DOCKERHUB_USERNAME) that contain the credentials required to push to my Dockerhub account.
     
-     A Github action was then created to trigger on a push to the main branch of my repository, and subsquently build the image and push it to my DockerHub account. The action was set up as shown below:
```python
name: Docker Image CI

on:
  push:
    branches:
      - "main"

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
      -
        name: Checkout
        uses: actions/checkout@v3
      -
        name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      -
        name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      -
        name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          file: ./Dockerfile
          push: true
          tags: ${{ secrets.DOCKERHUB_USERNAME }}/clockbox:latest
```      
      
## Conclusion

- Overall this was a very interesting project that covered many important topics and I feel that I really learnt so much working through it. 
