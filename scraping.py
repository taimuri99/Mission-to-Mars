# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

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

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# ### Featured Images

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

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# * An img tag is nested within this HTML, so we've included it.
# * .get('src') pulls the link to the image.
# 
# * What we've done here is tell BeautifulSoup to look inside the <img /> tag for an image with a class of fancybox-image. Basically we're saying, "This is where the image we want lives—use the link that's inside these tags."

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

# * df = pd.read_htmldf = pd.read_html('https://galaxyfacts-mars.com')[0] With this line, we're creating a new DataFrame from the HTML table. The Pandas function read_html() specifically searches for and returns a list of tables found in the HTML. By specifying an index of 0, we're telling Pandas to pull only the first table it encounters, or the first item in the list. Then, it turns the table into a DataFrame.
# 
# * df.columns=['description', 'Mars', 'Earth'] Here, we assign columns to the new DataFrame for additional clarity.
# 
# * df.set_index('description', inplace=True) By using the .set_index() function, we're turning the Description column into the DataFrame's index. inplace=True means that the updated index will remain in place, without having to reassign the DataFrame to a new variable.
# 

df.to_html()

browser.quit()