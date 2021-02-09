# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo

def init_browser():
    executable_path = {'executable_path': 'C:/webdrivers/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    #latest news article
    url = 'https://mars.nasa.gov/news/'

    browser.visit(url)

    html = browser.html

    latest_soup = BeautifulSoup(html, 'html.parser')

    news_title = latest_soup.find_all('div', class_='content_title')[1].text
    news_p = latest_soup.find_all('div', class_='article_teaser_body')[0].text

    #featured image
    fimage_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'

    browser.visit(fimage_url)

    image_html = browser.html

    image_soup = BeautifulSoup(image_html, 'html.parser')

    feat_image = image_soup.find('div', class_='floating_text_area')

    image_element = feat_image.a['href']

    featured_image_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{image_element}'

    #mars fact table
    table_url = 'https://space-facts.com/mars/'
    url_display = pd.read_html(table_url)[0]
    table_html = url_display.to_html(classes='table table-striped')

    #hemispheres

    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(hemi_url)

    hemi_h = browser.html

    hemi_soup = BeautifulSoup(hemi_h, 'html.parser')

    hemi_results = hemi_soup.find('div', class_='collapsible results')

    hemi_results_sub = hemi_results.find_all('div', class_='item')

    hemi_links = []

    for x in hemi_results_sub:
        hemi_desc = x.find('div', class_='description')
        hemi_title = hemi_desc.h3.text
        
        h_link = hemi_desc.a['href']
        browser.visit(f'https://astrogeology.usgs.gov/{h_link}')
        
        fh_html = browser.html
        fh_soup = BeautifulSoup(fh_html, 'html.parser')
        
        fh_link = fh_soup.find('div', class_='downloads')
        fh_url = fh_link.find('li').a['href']
        
        #adding to dictionary
        hemi_dict = {}
        hemi_dict['Title'] = hemi_title
        hemi_dict['Link'] = fh_url
        
        hemi_links.append(hemi_dict)

    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "fact_table": str(table_html),
        "hemisphere_images": hemi_links
    }

    return mars_dict