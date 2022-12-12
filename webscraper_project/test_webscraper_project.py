import unittest
import os
import sys
sys.path.append(r"C:\Users\amyma\AiCore Projects\Data_Collection_Project")
from myprotein_scraper import MyProteinScraper
from webscraper_module import Webscraper
from selenium import webdriver


class TestMyProteinScraper(unittest.TestCase):
    

    def setUp(self):
        self.scrape = MyProteinScraper()             #already inherited Webscraper so don't need to put in as argument
        self.scrape._close_email_signup()            #TODO: navigate straight to nutrition page, no need to go through whole scroll, click next etc etc
        self.scrape._accept_cookies()
        self.scrape._nutrition_button_click()
        self.scrape._open_all_nutrition_products()
        print('setUp method called...')              #for testing

    def test_create_product_dict(self):
        self.scrape._first_product_click()
        test_dict = self.scrape.create_product_dict('test_name', 'test_price', 'test_rating')
        self.assertIsInstance(test_dict, dict)
        print('create_product_dict returns a dictionary')

    # def test_create_product_folder(self):           
    #     random_directory = os.makedirs('random_name') #specify path
    #     self.scrape.create_product_folder(random_directory)
    #     self.assertTrue(os.path.exists('raw_data/random_name'), 'Product folder path does not exist')

    # def test_write_json(self):                      
    #     test_filename = 'test_filename'
    #     test_data = {'Price' : '£10.50'}
    #     self.scrape.write_json(test_data, test_filename)
    #     self.assertTrue(os.path.isdir(f'raw_data/{test_filename}/data.json'), 'Directory is invalid')

    # def test_create_image_folder(self):
    #     random_directory = os.makedirs('random_name') #specify path (/webscraper_project?)
    #     self.scrape.create_image_folder(random_directory)
    #     self.assertTrue(os.path.exists('raw_data/{random_directory}/images'), 'Image folder path does not exist')



    #def test_download_image(self):

    #def test_scrape_one_page(self):


    def tearDown(self):
        self.scrape.driver.quit()


if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)

        
