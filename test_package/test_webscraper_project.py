import unittest
from webscraper_project.webscraper_module import Webscraper
from webscraper_project.myprotein_scraper import MyProteinScraper

class TestMyProteinScraper(unittest.TestCase):
    
    def setUp(self):
        self.scrape = MyProteinScraper(Webscraper)
        self.scrape._close_email_signup()           #put these in __init__ method of myprotein scraper so that I don't need to repeat?
        self.scrape._accept_cookies()
        self.scrape._nutrition_button_click()
        self.scrape._open_all_nutrition_products()

    def test_create_product_folder(self):
        


    # def test_create_product_dict(self):
    #     test_dict = self.scrape._create_product_dict()
    #     actual_type = type(test_dict)
        
    #     self.assertIsInstance(dict, actual_type)

    #     #assert type(test_dict) is dict

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)

        
