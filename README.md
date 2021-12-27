# Mission-to-Mars
## Module 10: Mission to Mars - Web Scraping with HTML/CSS
For the challenge we were tasked to display the data, and alter the design of the web app to accommodate these images of Mars' Hemispheres which we scraped from a website using Jupyter and Python. The web page was made using flask, html and mongodb. 
## Deliverable 1
Using BeautifulSoup and Splinter, we scrape full-resolution images of Mars’s hemispheres and the titles of those images. The full-resolution images of the hemispheres and titles are added to the dictionary initialised using the following code:

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
  
The following dictionary is created:

<img width="635" alt="Screenshot 2021-12-27 at 15 13 35" src="https://user-images.githubusercontent.com/87828174/147504264-cde85295-1d3c-4edd-bb40-9c30dcb3802d.png">

## Deliverable 2
Using Python and HTML, we add the code created in Deliverable 1 to the scraping.py file. The scraping.py file retrieves the full-resolution image URL and title for each hemisphere image. The Mongo database is updated to contain the full-resolution image URL and title for each hemisphere image. The index.html file contains code that will display the webpage containing all the information we collected in this module as well as the full-resolution image and title for each hemisphere image. After scraping has been completed, the web app displays this information.

## Deliverable 3
Using CSS and two additional Bootstrap components, we make the web page stand out. The webpage is made mobile-responsive using code such as this:

        <div class="col-xs-12 col-sm-12 col-md-12">

Finally we use two additional Bootstrap components to customize the web page such as colours and fonts. Here is the webpage as seen on a laptop.

<img width="1173" alt="Screenshot 2021-12-27 at 15 24 00" src="https://user-images.githubusercontent.com/87828174/147505017-357b58de-0d31-43e2-afc0-22c39866f400.png">
<img width="1174" alt="Screenshot 2021-12-27 at 15 24 18" src="https://user-images.githubusercontent.com/87828174/147505022-da279a4c-b5ff-45bf-855f-7cff26b6785e.png">
<img width="1174" alt="Screenshot 2021-12-27 at 15 24 28" src="https://user-images.githubusercontent.com/87828174/147505033-183c86d6-9b8d-4602-bb1e-2c1b5e6624a3.png">
