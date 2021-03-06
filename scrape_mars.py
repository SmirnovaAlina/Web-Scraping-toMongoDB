from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


def scrape_info():
    united_mars = {}
    

    nasa_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    response = requests.get(nasa_url)
    soup = BeautifulSoup(response.text, 'lxml')
    
    news_title = str(soup.find_all('div', class_='content_title')[0].a.text).replace('\n', '')
    united_mars["news_title"] = news_title

    news_p = str(soup.find_all('div', class_="rollover_description_inner")[0].text).replace('\n','')
    united_mars["news_p"] = news_p

    browser = init_browser() 
    time.sleep(1)
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    time.sleep(2)
 
    browser.click_link_by_id('full_image')
    time.sleep(3)
    browser.click_link_by_partial_text('more info')
    time.sleep(3)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    main_image = soup.find('img', class_="main_image" )["src"]
    
    main_image_url = 'https://www.jpl.nasa.gov'
    featured_image_url = main_image_url + main_image

    united_mars["featured_image_url"] = featured_image_url
    time.sleep(1)

    browser.quit()

    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(twitter_url)
    soup = BeautifulSoup(response.text, 'lxml')
    mars_weather = soup.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")[1].text.split(' ', 1)[1].rsplit(' ', 1)[0]
    united_mars["mars_weather"] = mars_weather

    space_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(space_url)
    df = tables[0]
    df.columns = ['description', 'Value']
    df.set_index('description', inplace=True)
    data = df.to_html()
    united_mars["mars_facts"] = data

    
    browser = init_browser() 


    astrogeology_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(astrogeology_url)
    time.sleep(2)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    images = soup.find_all('img', class_="thumb")
    images[1].attrs['alt'].rsplit(' ', 1)[0]

    images_name = []
    images = soup.find_all('img', class_="thumb")
    for image in images:
        try: 
            images_name.append(image.attrs['alt'].rsplit(' ', 1)[0])
        except:
            continue
   

    hemisphere_image_urls=[]
    for image in images_name:
        browser.click_link_by_partial_text(image)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        image_url = soup.find_all("a", text="Sample")
        hemisphere_dict = {"title": image, "img_url": image_url[0].attrs["href"] }
        hemisphere_image_urls.append(hemisphere_dict.copy())
        browser.back()

    united_mars['hemisphere_image_urls'] = hemisphere_image_urls

    browser.quit()

    return united_mars


    
    
    

























