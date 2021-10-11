#!/usr/bin/env python
# coding: utf-8

import bs4
from bs4 import BeautifulSoup as soup
import pandas as pd
import pprint

# Needed for dynamic web pages
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from splinter import Browser
import os

def scrape():
    # Instantiate an Options object and add the --headless argument
    # This runs the browser in the background
    opts = Options()
    opts.add_argument(" --headless")

    # Set the location of the webdriver
    chrome_driver='C:\\Users\\srobi\\Projects\\chromedriver.exe'

    # Instantiate a webdriver
    driver = webdriver.Chrome(options=opts,executable_path=chrome_driver)

    # To scrape a url rather than a local file use this
    my_url = 'https://redplanetscience.com/'
    driver.get(my_url)

    # Put the page source into a variable and create a BS object from it, parse HTML
    page_html = driver.page_source
    page_soup = soup(page_html, "html.parser")

    # Close the browser
    driver.quit()

    # Tests to see if html has been parsed properly
    print('\nTesting html parsing...')
    print(page_soup.title.get_text())
    print(page_soup.h1.text) # shows header information
    print(page_soup.p.text) # shows paragraph information
    print(page_soup.body.span.text)
    print('Testing completed.\n')

    # Grabs each element
    titles = page_soup.findAll("div",{"class":"content_title"})
    print(f'There are {len(titles)} titles total.') # find total number of containers
    news_title = titles[0].text # look at the first container
    print(f'Here is the first title: \n{news_title}\n')

    paragraphs = page_soup.findAll("div",{"class":"article_teaser_body"})
    print(f'There are {len(paragraphs)} paragraphs total.') # find total number of containers
    news_p = paragraphs[0].text # look at the first container
    print(f'Here is the first paragraph: \n{news_p}\n')

    # Instantiate an Options object and add the --headless argument
    # This runs the browser in the background
    opts = Options()
    opts.add_argument(" --headless")

    # Set the location of the webdriver
    chrome_driver='C:\\Users\\srobi\\Projects\\chromedriver.exe'

    # Instantiate a webdriver
    driver = webdriver.Chrome(options=opts,executable_path=chrome_driver)

    # To scrape a url rather than a local file use this
    mars_image_url = 'https://spaceimages-mars.com/'
    driver.get(mars_image_url)

    # Put the page source into a variable and create a BS object from it, parse HTML
    page_html = driver.page_source
    page_soup = soup(page_html, "html.parser")

    # Load and print the title and the text of the <div>
    print('Testing that html has been parsed...')
    print(page_soup.title.get_text())
    print('Testing completed.')

    # Close the browser
    driver.quit()

    # Display featured url
    images = page_soup.findAll('img')[1]
    featured_image_url = mars_image_url + images['src']
    print(featured_image_url)

    # Pandas scraping
    url = 'https://galaxyfacts-mars.com/'

    tables = pd.read_html(url,header=0)
    df = tables[0]
    print('Dataframe created from table.')

    # Convert to HTML table
    html_table = df.to_html(index=False,col_space=30,justify='left',border=1)
    html_table = html_table.replace('\n','')
    print('Dataframe converted to HTML table called html_table.')

    # Extract table header and column values
    table_headers = df.columns.tolist()
    # col1_list = df['Mars - Earth Comparison'].tolist()
    # col2_list = df['Mars'].tolist()
    # col3_list = df['Earth'].tolist()
    # table_dict = df.set_index('Mars - Earth Comparison').T.to_dict('list')
    table_rows = df.values.tolist()

    # url for the image (Chrome version)
    mars_hemispheres_url = 'https://marshemispheres.com/'

    # Set up browser for Splinter
    executable_path = {'executable_path':'../chromedriver'}
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") # start with window maximized
    options.add_argument("--disable-notifications") # notifications turned off
    browser = Browser('chrome', **executable_path, headless=False, options = options)

    browser.visit(mars_hemispheres_url)

    submit = browser.find_by_css('a[class="itemLink product-item"]')
    original_submit_count = len(submit)
    print(f'There are {original_submit_count} items in the submit variable.')

    # Need to set up a loop to retrieve only even numbers
    # Can achieve this by adding 1 and divide by 2, mod needs to == 0
    hemisphere_image_urls = []

    for x in range(original_submit_count):
        if (x+1) % 2 == 0:
            # Splinter clicks on the submit element to open the page in Chrome
            submit = browser.find_by_css('a[class="itemLink product-item"]')
            submit[x].click()

            # Grab the current url using Splinter
            # This will be used as input for Beautiful Soup to parse the HTML
            current_url = browser.url
            print(current_url)
            
            # Instantiate a webdriver
            driver = webdriver.Chrome(options=opts,executable_path=chrome_driver)
            driver.get(current_url)

            # Put the page source into a variable and create a BS object from it, parse HTML
            page_html = driver.page_source
            page_soup = soup(page_html, "html.parser")

            # Load and print the title as a test
            print(page_soup.title.get_text())

            # Close the browser
            driver.quit()

            # Find title of image
            hemisphere_titles = page_soup.find_all("h2", {"class":"title"})
            title = hemisphere_titles[0].text
            print(title)

            # Find image_url
            hemisphere_images = page_soup.find_all("img", {"class":"wide-image"})
            image_url = mars_hemispheres_url + hemisphere_images[0]['src']
            print(image_url)
            
            # Append title and image_url to dictionary
            dictionary = {'title':title,'img_url':image_url}
            hemisphere_image_urls.append(dictionary)
            
            # Add a break line
            print()
            
            # Splinter clicks on the browser Back button
            browser.back()

    pprint.pprint(hemisphere_image_urls)
    print()

    # Create dictionary of all scraped data
    final_dictionary = {
        "news_title":news_title,
        "news_paragraph":news_p,
        "featured_image":featured_image_url,
        "mars_facts":html_table,
        "table_headers":table_headers,
        # "col1_list":col1_list,
        # "col2_list":col2_list,
        # "col3_list":col3_list,
        # "table_dict":table_dict,
        "table_rows":table_rows,
        "mars_hemispheres":hemisphere_image_urls
    }
    pprint.pprint(final_dictionary)

    # Return results
    return final_dictionary