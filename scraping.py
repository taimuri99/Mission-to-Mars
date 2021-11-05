# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # using mars_news function
    news_title, news_paragraph = mars_news(browser)
    hemisphere_image_urls = hemisphere_images(browser)
    # Run all scraping functions and store results in dictionary
    # create the HTML template, we'll create paths to the dictionary's values, which lets us present our data on our template
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemisphere_image_urls
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # * above code is searching for elements with a specific combination of tag (div) and attribute (list_text).
    # 
    # * As an example, ul.item_list would be found in HTML as <ul class="item_list">.
    # 
    # * Secondly, we're also telling our browser to wait one second before searching for components.
    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')

        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None

    
    return news_title, news_p

# ### Featured Images

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    # the [1] tells it to choose the second button as the first one is navbar
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        img_url_rel
    except AttributeError:
        return None
    # * An img tag is nested within this HTML, so we've included it.
    # * .get('src') pulls the link to the image.
    # 
    # * What we've done here is tell BeautifulSoup to look inside the <img /> tag for an image with a class of fancybox-image. Basically we're saying, "This is where the image we want lives—use the link that's inside these tags."

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    return img_url

def mars_facts():
    try:
      # use 'read_html" to scrape the facts table into a dataframe
      # df = pd.read_htmldf = pd.read_html('https://galaxyfacts-mars.com')[0] With this line, we're creating a new DataFrame from the HTML table. The Pandas function read_html() specifically searches for and returns a list of tables found in the HTML. By specifying an index of 0, we're telling Pandas to pull only the first table it encounters, or the first item in the list. Then, it turns the table into a DataFrame.
      df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
      return None

    # Assign columns and set index of dataframe
    # df.columns=['description', 'Mars', 'Earth'] Here, we assign columns to the new DataFrame for additional clarity.
    df.columns=['description', 'Mars', 'Earth']
    # df.set_index('description', inplace=True) By using the .set_index() function, we're turning the Description column into the DataFrame's index. inplace=True means that the updated index will remain in place, without having to reassign the DataFrame to a new variable.
    df.set_index('description', inplace=True)
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()

def hemisphere_images(browser):
    # # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

    # ### Hemispheres

    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.

    for n in range(4,12,2):
        hemispheres = {}
        browser.find_by_css('a[href]')[n].click()
        html = browser.html
        img_soup = soup(html, 'html.parser')
        title = img_soup.find('h2', class_='title').get_text()
        partial_link = img_soup.find_all('a', target= '_blank')[2].get('href')
        img_url = f'https:/marshemispheres.com/{partial_link}'
        
        hemispheres['img_url'] = img_url
        hemispheres['title'] = title
        
        hemisphere_image_urls.append(hemispheres)
        browser.back()
        

    # 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())