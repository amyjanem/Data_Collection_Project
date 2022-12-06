import unittest
from webscraper_project.webscraper_module import Webscraper
from webscraper_project.myprotein_scraper import MyProteinScraper

class TestMyProteinScraper(unittest.TestCase):
    def setUp(self):
        self.scrape = MyProteinScraper(Webscraper)

    def test_create_product_dict(self):
        expected_type = type(dict)
        actual_type = type(self.scrape.create_product_dict())
        self.assertEqual(expected_type, actual_type)

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)

        
