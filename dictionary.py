# TODO: Your dictionary should include all details for each record, its unique ID, timestamp of when it was scraped and links to any images associated with each record.

# def get_product_image(self):
#     '''
#     Finds the href to the product image and returns it??

#     '''
#     time.sleep(1)
#     product_image = driver.find_element(By.XPATH, '//img[@class="athenaProductImageCarousel_image"]').get_attribute('src')

#     return product_image


# def get_product_price(self):
#     '''
#     Finds price of product and returns it?
#     '''
#     time.sleep(1)
#     product_price = driver. find_element(By.XPATH, '//p[@class="productPrice_price  "]')
#     print(product_price.text)
    
#     return product_price


# def get_product_rating(self):
#     '''
#     Finds rating of product and returns it?
#     '''
#     time.sleep(1)
#     product_rating = driver.find_element(By.XPATH, '//span[@class="athenaProductReviews_aggregateRatingValue"]')
#     print(product_rating.text)

#     return product_rating



def get_product_info(self):
    '''
    Finds xpath of product name, price, rating and image link?
    '''
    
    time.sleep(1)
    product_name = driver.find_element(By.XPATH, '//h1[@class="productName_title"]').text
    #product_name.text

    time.sleep(1)
    product_price = driver.find_element(By.XPATH, '//p[@class="productPrice_price  "]').text
    #product_price.text

    time.sleep(1)
    product_rating = driver.find_element(By.XPATH, '//span[@class="athenaProductReviews_aggregateRatingValue"]').text
    #product_rating.text

    time.sleep(1)
    product_image = driver.find_element(By.XPATH, '//img[@class="athenaProductImageCarousel_image"]').get_attribute('src')


@staticmethod
def get_timestamp():
    '''
    Prints the timestamp of current time.
    '''
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)



# for link in product_link_list:
#     append?
#     product_dict = {"Product Name" : product_name, "Product Price" : product_price, "Product Rating" : product_rating, "Product Image Link" : product_image, "Time of Data Retrieval" : time_stamp}