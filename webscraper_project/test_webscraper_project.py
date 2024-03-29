import unittest
import os
import shutil
import sys
sys.path.append(r"C:\Users\amyma\AiCore Projects\Data_Collection_Project")
from myprotein_scraper import MyProteinScraper


class TestMyProteinScraper_1(unittest.TestCase):
    

    def setUp(self):
        self.scrape = MyProteinScraper()             #already inherited Webscraper so don't need to put in as argument
        self.scrape._close_email_signup()            
        self.scrape._accept_cookies()
        self.scrape._nutrition_button_click()
        self.scrape._open_all_nutrition_products()
        print('setUp method called...\n\n')          #for testing

    def test_create_product_dict(self):            #pass
        self.scrape._first_product_click()
        test_dict = self.scrape.create_product_dict('test_name', 'test_price', 'test_rating')
        self.assertIsInstance(test_dict, dict)
        print('create_product_dict returns a dictionary')

    def test_scrape_one_page(self):                 #pass
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

        #testing that the files created have the correct information?
        test_file = lst[1]          #random file to be read
        with open(f'raw_data/{test_file}/data.json', 'r') as file:
            data_text = file.read() #??

        #testing that the images were downloaded correctly
        with open("raw_data/{test_file}/images/*.jpg" ,'wb'): #?
            pass


#TODO:
#To test the files you can have the expected file already created read it in.
#Then read in the file that was downloaded in your test and compare then.
#You could just do a json.loads for both and compare them in the assertion.

#For the images you can just read the images in byte form to test them against each other.
#You can read images in bytes by passing the b flag into your file open statement along with the filemode. Like with open("<filename here>" ,'wb') and compare them that way.


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

        
