import unittest
from webscraper_project.webscraper_module import Webscraper
from webscraper_project.myprotein_scraper import MyProteinScraper

class TestMyProteinScraper(unittest.TestCase):
    def setUp(self):
        self.scrape = MyProteinScraper(Webscraper)

    def test_create_product_dict(self):
        #expected_type = type(dict)
        test_dict = self.scrape._create_product_dict()
        #print(type(test_dict))
        actual_type = type(test_dict)
        #assert type(test_dict) is dict
        self.assertIsInstance(type(test_dict), dict)

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)

        
