


from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser


import pandas as pd



def scrape():
    local_nasa_file= "News_NASA_Mars_Exploration_Program.html"

    nasa_html=open(local_nasa_file, "r").read()
    news_soup = bs(nasa_html, "html.parser")
    recent_title=news_soup.find("div",class_="content_title").text
    recent_para=news_soup.find("div", class_="article_teaser_body").text
    mars_url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    # Retrieve page with the requests module
    response = requests.get(mars_url)
    # Create BeautifulSoup object; parse with 'html parser'
    soup = bs(response.text, 'html.parser')
    featured=soup.find("a",class_="button fancybox")
    featured_image_url='https://www.jpl.nasa.gov' + featured["data-fancybox-href"]
    mars_twitter='https://twitter.com/marswxreport?lang=en'
    response_twitter=requests.get(mars_twitter)
    soup_twitter=bs(response_twitter.text, 'html.parser')
    recent_tweet=soup_twitter.find("div", class_="js-tweet-text-container")
    mars_weather=recent_tweet.p.text
    space_facts='https://space-facts.com/mars/'
    mars_table=pd.read_html(space_facts)
    clean_table=pd.DataFrame(columns=list(mars_table[0][0]))
    clean_table.loc[0]=list(mars_table[0][1])
    table_html=clean_table.to_html()
    table_html=table_html.replace('\n', '')
    table_html=table_html.replace("'", '')
    ##rendered_table=bs(table_html)


    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    base_url='https://astrogeology.usgs.gov'
    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    hemisphere_image_urls=[]
    for x in range(0,4):
        html = browser.html
        soup = bs(html, 'html.parser')
        mars_links = soup.find_all('div', class_='item')
        #find the 1st, 2nd, 3rd, and 4th href link and travel to their pages
        link_tag=mars_links[x].find('a', href=True)
        link=link_tag['href']
        #save the title of the current image
        title=mars_links[x].find('h3').text
        #travel to the image's page
        browser.visit(base_url+link)
        ## parse the new page html
        html = browser.html
        soup = bs(html, 'html.parser')
        #locate the image url
        image=soup.find("img", class_="wide-image")
        #append it to the base url
        image_url=base_url+ image['src']
        #save both title and url to a list of dictionaries
        hemisphere_image_urls.append({'title':title, 'image_url':image_url})
        #travel to the previous page to go find the next image
        browser.back()

    mars_dict = {
        "recent_title": recent_title,
        "recent_para": recent_para,
        "featured_image_url": featured_image_url ,
        "mars_weather" : mars_weather ,
        "table_html" : table_html,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    return mars_dict
