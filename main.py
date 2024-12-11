import requests
from bs4 import BeautifulSoup
from datetime import datetime
import traceback
import os
import re

# Function to scrape news page information and return a news dictionary and a list of images
def get_news(new_url):
    # News information dictionary
    new_dict = {}
    print("News URL: " + new_url)
    try:
        res = requests.get(new_url)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'lxml')
        # Title
        new_title = soup.select('h1.article_title')[0].text.strip()
        new_dict['title'] = new_title
        # Time
        nt = datetime.strptime(soup.select('span.time')[0].text.strip(), '%Y-%m-%d %H:%M:%S')
        new_time = datetime.strftime(nt, '%Y-%m-%d %H:%M')
        new_dict['time'] = new_time
        print(nt)
        # Source - cannot use a.source as the source content may be in a span tag
        new_source = soup.select('span.source')[0].text
        new_dict['source'] = new_source
        # Author
        new_author = soup.select('div#js_article_content>p>strong')[0].text
        new_dict['author'] = new_author
        # Article body
        news_article = soup.select('div#js_content.article_content>p')
        tmp_str = ''
        for i in range(len(news_article) - 1):
            tmp_str += news_article[i].text + '\r\n'
        new_dict['article'] = tmp_str
        # Images
        news_pic = soup.select('div#js_article_content>p.pcenter> img')
        news_pic_list = []
        for pic in news_pic:
            news_pic_list.append(pic.get("src"))
        new_dict['picture'] = news_pic_list
    except Exception as e:
        print('Error while scraping, this news article will be skipped')
        print(e)
        traceback.print_exc()
        return None, None
    print('Time: %s Title: %s Author: %s Source: %s ' % (new_time, new_title, new_author, new_source))
    print('Total %d images found' % len(news_pic_list))
    return new_dict, news_pic_list

# Function to get all news links
def get_url_list(new_list_url, num_pages=1):
    # News links list
    news_url_list = []
    # Control the number of pages to scrape
    for i in range(1, num_pages + 1):
        url = new_list_url.format(page=i)
        tmp_url_list = get_url(url)
        # Merge URL lists
        if len(tmp_url_list):
            news_url_list[len(news_url_list):len(news_url_list)] = tmp_url_list
        else:
            print('-----------Finished scraping directory-----------')
            break
    return news_url_list

# Function to get all news links from a specified page
def get_url(new_list_url):
    url = new_list_url
    res = requests.get(url)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    # Get news links
    url_list = []
    news_url = soup.select('div#list>div>div>a')
    print(news_url)
    for url in news_url:
        url_list.append(url.get('href'))
    print('This page has %d news articles. Links: %s' % (len(url_list), new_list_url))
    return url_list

# Function to save news
def save_new(root_dir, news_dict, pic_list):
    # Create subdirectory
    try:
        # Filter out symbols that cannot appear in path names
        title = news_dict['title']
        title = re.sub(r'[\\/:*?"<>|!：？！；]', '_', title)
        file_dir = root_dir + os.sep + title
        is_dir_exist = os.path.exists(file_dir)
        if not is_dir_exist:
            os.makedirs(file_dir)
        # Output news text
        save_text(file_dir, news_dict)
        # Output images
        save_pic(file_dir, pic_list)
    except Exception as e:
        print('Error while saving')
        print(e)
        traceback.print_exc()
    print("Save complete, news file path: %s" % file_dir)

# Function to save text
def save_text(file_dir, news_dict):
    res = ('Title: ' + news_dict['title'] + '\r\n' +
           'Time: ' + news_dict['time'] + '\r\n' +
           'Author: ' + news_dict['author'] + '\r\n' +
           'Source: ' + news_dict['source'] + '\r\n' +
           'News Body: ' + news_dict['article'] + '\r\n ')
    # Filter out symbols that cannot appear in file names
    title = news_dict['title']
    title = re.sub(r'[\\/:*?"<>|!：？！；]', '_', title)
    # Output
    file_path = file_dir + os.sep + title + '.txt'
    with open(file_path, "wb") as f:
        f.write(res.encode("utf-8"))

# Function to save images
def save_pic(file_dir, pic_list):
    for i in range(len(pic_list)):
        # Image save path
        pic_path = file_dir + os.sep + '%d.jpg' % i
        try:
            req = requests.get(pic_list[i])
        except requests.exceptions.MissingSchema as e:
            print('Image URL error, attempting to complete URL')
            print(e)
            req = requests.get('http:' + pic_list[i])
        finally:
            img = req.content
            with open(pic_path, "wb") as f:
                f.write(img)

# Start execution
def start_spider(root_url, root_dir, num_pages=1):
    url_list = get_url_list(root_url, num_pages)
    print('----Link retrieval complete----')
    l = len(url_list)
    print('About to scrape %d news articles\r\n' % l)
    for i in range(len(url_list)):
        print('%d: ' % i)
        new, pic = get_news(url_list[i])
        if new:
            save_new(root_dir, new, pic)
    print('--------Scraping complete--------')

if __name__ == '__main__':
    # Entry point {page} is used for format formatting
    root_url = 'https://finance.china.com/tuijian/'
    root_dir = r'news'
    start_spider(root_url, root_dir)