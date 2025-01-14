
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd
import os 
## Install the required libraries
url = 'https://techcrunch.com/category/artificial-intelligence/'

ua = UserAgent()
userAgent = ua.random
headers = {'User-Agent': userAgent}
page = requests.get(url, headers = headers)
soup = BeautifulSoup(page.content, "html.parser")
print(url)
blog_box = soup.find_all('div', class_= "loop-card loop-card--post-type-post loop-card--default loop-card--horizontal loop-card--wide loop-card--force-storyline-aspect-ratio")

links = []
titles = []
time_uploaded = []
authors = []
tags = []
reading_times = []

for box in blog_box: 
    if box.find('h3', class_ = "loop-card__title") is not None:
        link = box.find('h3', class_ = "loop-card__title").a  #.replace('\n\t\t','').replace('\n','').strip()
        link = link['href']
        #links.append('https://techcrunch.com/category/artificial-intelligence/'+ link)
        if not link.startswith('http'):
            links.append('https://techcrunch.com/category/artificial-intelligence/' + link)
        else:
            links.append(link)

    else:
        links.append('None')

    #titles
    if box.find('h3', class_ = "loop-card__title") is not None:
        title = box.find('h3', class_ = "loop-card__title").text.replace('\n','').strip()
        titles.append(title)
    else:
        titles.append('None')

    #time_uploaded
    if box.find('time', attrs={"datetime": True}) is not None:
        time_upload = box.find('time', attrs={"datetime": True})   #.replace('\n\t\t','').replace('\n','').strip()
        time_upload = time_upload['datetime']
        time_uploaded.append(time_upload)
    else:
        time_uploaded.append('None') 

    #author
    if box.find('a', class_ ="loop-card__author") is not None:
        author = box.find('a', class_ ="loop-card__author").text.replace('\n','').strip()
        authors.append(author)
    else:
        authors.append('None')

    #tags
    if box.find('a', class_ ="loop-card__cat") is not None:
        tag = box.find('a', class_ ="loop-card__cat").text.replace('\n','').strip()
        tags.append(tag)
    else:
        tags.append('None')

df = pd.DataFrame({
    'Link': links,
    'Title': titles,
    'Time Uploaded': time_uploaded,
    'Author': authors,
    'Tags': tags
})

df_cleaned = df[df['Link'] != 'None']

article = []
article_link = []
def get_full_content(url): 
    ua = UserAgent()
    userAgent = ua.random
    headers = {'User-Agent': userAgent}
    page = requests.get(url, headers = headers)
    soup = BeautifulSoup(page.content, "html.parser")
    print(url)
    content = soup.find('div', class_= "entry-content wp-block-post-content is-layout-constrained wp-block-post-content-is-layout-constrained")
    paragraphs = content.find_all('p')
    contents = []
    # Iterate over each <p> tag and remove any <a> tags within them
    for paragraph in paragraphs:
        for a in paragraph.find_all('a'):
            a.decompose()  # Removes <a> tag and its content

    # Print the cleaned text from each <p> tag
    for paragraph in paragraphs:
        contents.append(paragraph.get_text())

    string = ' '.join(contents)
    article.append(string)
    article_link.append(url)

for i in df_cleaned.Link:
    get_full_content(i)


article_df = pd.DataFrame({
    'Article Content': article,
    'Link': article_link
})


merged_df = pd.merge(df_cleaned, article_df, on='Link', how='inner')
merged_df

file_exists = os.path.isfile('merged_articles.csv')
merged_df.to_csv('merged_articles.csv', mode='a', header=not file_exists, index=False)
file_exists = True

#### Fetch rest of the pages

ua = UserAgent()
userAgent = ua.random
headers = {'User-Agent': userAgent}

for page_num in range(2, 330):
    url = f'https://techcrunch.com/category/artificial-intelligence/page/{page_num}/'
    print(f'Scraping page {page_num}: {url}')

    page = requests.get(url, headers = headers)
    soup = BeautifulSoup(page.content, "html.parser")
    print(url)
    blog_box = soup.find_all('div', class_= "loop-card loop-card--post-type-post loop-card--default loop-card--horizontal loop-card--wide loop-card--force-storyline-aspect-ratio")

    links = []
    titles = []
    time_uploaded = []
    authors = []
    tags = []
    reading_times = []

    for box in blog_box: 
        if box.find('h3', class_ = "loop-card__title") is not None:
            link = box.find('h3', class_ = "loop-card__title").a  #.replace('\n\t\t','').replace('\n','').strip()
            link = link['href']
            #links.append('https://techcrunch.com/category/artificial-intelligence/'+ link)
            if not link.startswith('http'):
                links.append(url + link)
            else:
                links.append(link)

        else:
            links.append('None')

        #titles
        if box.find('h3', class_ = "loop-card__title") is not None:
            title = box.find('h3', class_ = "loop-card__title").text.replace('\n','').strip()
            titles.append(title)
        else:
            titles.append('None')

        #time_uploaded
        if box.find('time', attrs={"datetime": True}) is not None:
            time_upload = box.find('time', attrs={"datetime": True})   #.replace('\n\t\t','').replace('\n','').strip()
            time_upload = time_upload['datetime']
            time_uploaded.append(time_upload)
        else:
            time_uploaded.append('None') 

        #author
        if box.find('a', class_ ="loop-card__author") is not None:
            author = box.find('a', class_ ="loop-card__author").text.replace('\n','').strip()
            authors.append(author)
        else:
            authors.append('None')

        #tags
        if box.find('a', class_ ="loop-card__cat") is not None:
            tag = box.find('a', class_ ="loop-card__cat").text.replace('\n','').strip()
            tags.append(tag)
        else:
            tags.append('None')

    df = pd.DataFrame({
        'Link': links,
        'Title': titles,
        'Time Uploaded': time_uploaded,
        'Author': authors,
        'Tags': tags
    })

    df_cleaned = df[df['Link'] != 'None']

    article = []
    article_link = []
    def get_full_content(url): 
        ua = UserAgent()
        userAgent = ua.random
        headers = {'User-Agent': userAgent}
        page = requests.get(url, headers = headers)
        soup = BeautifulSoup(page.content, "html.parser")
        print(url)
        content = soup.find('div', class_= "entry-content wp-block-post-content is-layout-constrained wp-block-post-content-is-layout-constrained")
        paragraphs = content.find_all('p')
        contents = []
        # Iterate over each <p> tag and remove any <a> tags within them
        for paragraph in paragraphs:
            for a in paragraph.find_all('a'):
                a.decompose()  # Removes <a> tag and its content

        # Print the cleaned text from each <p> tag
        for paragraph in paragraphs:
            contents.append(paragraph.get_text())

        string = ' '.join(contents)
        article.append(string)
        article_link.append(url)

    for i in df_cleaned.Link:
        get_full_content(i)


    article_df = pd.DataFrame({
        'Article Content': article,
        'Link': article_link
    })


    merged_df = pd.merge(df_cleaned, article_df, on='Link', how='inner')
    file_exists = os.path.isfile('merged_articles.csv')
    merged_df.to_csv('merged_articles.csv', mode='a', header=not file_exists, index=False)
    file_exists = True