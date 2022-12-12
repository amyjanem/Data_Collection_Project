import unittest
import os
import sys
sys.path.append(r"C:\Users\amyma\AiCore Projects\Data_Collection_Project")

from myprotein_scraper import MyProteinScraper
from webscraper_module import Webscraper


class TestMyProteinScraper(unittest.TestCase):
    

    def setUp(self):
        self.scrape = MyProteinScraper(Webscraper)
        self.scrape._close_email_signup()           #put these in __init__ method of myprotein scraper so that I don't need to repeat?
        self.scrape._accept_cookies()
        self.scrape._nutrition_button_click()
        self.scrape._open_all_nutrition_products()
        print('setUp method called...')             #for testing

    def test_create_product_dict(self):
        self.scrape._first_product_click()
        test_dict = self.scrape.create_product_dict()
        self.assertIsInstance(test_dict, dict)
        print('create_product_dict returns a dictionary')

    def test_create_product_folder(self):           #not being picked up as test, ie not being counted in 'Ran X test in ...'
        random_directory = os.makedirs('random_name') #specify path
        self.scrape.create_product_folder(random_directory)
        self.assertTrue(os.path.exists('raw_data/random_name'), 'Folder path does not exist')

    def test_write_json(self):                      #not being picked up as test. Is it better to test that data has been written to file as desired?
        test_filename = '123'
        test_data = 456 #change to dict
        self.scrape.write_json(test_data, test_filename)
        self.assertTrue(os.path.isdir(f'raw_data/{test_filename}/data.json'), 'Directory is invalid')


    #def test_create_image_folder(self):

    #def test_download_image(self):

    #def test_scrape_one_page(self):


    def tearDown(self):
        self.scrape.driver.quit()


if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)

        
