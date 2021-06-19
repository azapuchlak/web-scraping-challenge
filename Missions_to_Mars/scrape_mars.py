#Import Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import requests

def scrape():
    # Set Executable Path & Initialize Chrome Browser
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)

    # Step 1 - Scraping
    ### NASA Mars News - Print Article Title & Description
   
    # Visit the NASA Mars News Site
    url_news = "https://redplanetscience.com/"
    browser.visit(url_news)
    
    #Put results into HTML
    html = browser.html
    
    #use BeautifulSoup to print the results
    soup = bs(html, 'html.parser')
    
    # print(soup.prettify()) - commenting out for sake of scrolling     
    
    # Scrape the latest news title
    news_title = browser.find_by_css('.content_title')[0].text
    print(news_title)
    
    # Scrape the Latest Paragraph Text
    news_paragraph = browser.find_by_css('.article_teaser_body')[0].text
    print(news_paragraph)

    
    ### JPL Mars Space Images -  Print Featured Image
    
    # Visit https://spaceimages-mars.com/
    url_pic = "https://spaceimages-mars.com/"
    browser.visit(url_pic)
    
    #Put results into html
    space_image = browser.html
    
    #Use BeautifulSoup to print the results
    soup_image = bs(space_image, 'html.parser')
    
    #print(soup_image.prettify()) - commenting out for sake of scrolling
    
    #Went through elements and saw the class of the featured image was headerimage fade-in
   
    #code below searches for the class and prints the image with
    featured_pic = soup_image.find(class_='headerimage fade-in')['src']
    print(featured_pic)
    
    #Assign the url string to a variable
    featured_image_url = url_pic + featured_pic
    print(featured_image_url)
  
   
    ### Mars Facts - Scrape Table
    
    # Visit & Scrape data from https://galaxyfacts-mars.com/
    url_facts = "https://galaxyfacts-mars.com/"
    browser.visit(url_facts)
    
    #Find/Scrape the table and convert it to a HTML string
    html = browser.html
    tables = pd.read_html(url_facts)
    html_table = tables[0].to_html(header=False, index=False)
    html_table
    
    #Display tables to confirm accuracy
    tables = pd.read_html(url_facts)
    tables
    
    #Turn scraped data into DF
    facts_df = tables[1]
    facts_df.columns = ['Fact', 'Data']
    facts_df

    
    ### Mars Hemispheres
   
    # Visit the NASA Mars News Site
    url_hemi = "https://marshemispheres.com/"
    browser.visit(url_hemi)
   
    #Put results into HTML
    html = browser.html
    
    #use BeautifulSoup to print the results
    soup = bs(html, 'html.parser')
    
    #print(soup.prettify())  - commenting out for sake of scrolling 
    image_div_items = soup.find_all('div',class_='item')
    
    # Create temporary blank dicts to store urls
    product_list = []
    url_list = []
    product_img_url_dict = []
    
    # Create for loop that finds image urls for each hemisphere
    for hemisphere in image_div_items:
        if hemisphere.h3:
            product = hemisphere.h3.text
            product_list.append(product)
        if hemisphere.img:
            image_src = hemisphere.find('img')['src']
            url_list.append(image_src)
        
    # Create for loop to add the lists into blank dicts
    for products, img_url in zip(product_list, url_list):
        product_url = {"Product": product, "image_url": url_hemi+img_url}
        product_img_url_dict.append(product_url)
    product_img_url_dict

# Put scraped items into a dictionary for MongoDB
    mars_data = {
        "news_title": news_title,
        "news_paragraph": first_paragraph,
        "featured_image": featured_image_url,
        "mars_fact_table": html_table,
        "hemisphere_title_1": image_title_url_dict[0]["title"],
        "hemisphere_image_1": image_title_url_dict[0]["image_url"],
        "hemisphere_title_2": image_title_url_dict[1]["title"],
        "hemisphere_image_2": image_title_url_dict[1]["image_url"],
        "hemisphere_title_3": image_title_url_dict[2]["title"],
        "hemisphere_image_3": image_title_url_dict[2]["image_url"],
        "hemisphere_title_4": image_title_url_dict[3]["title"],
        "hemisphere_image_4": image_title_url_dict[3]["image_url"]
    }

    browser.quit()

    return(mars_data)