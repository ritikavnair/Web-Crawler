import requests
import re
import io
import time
import collections
import os
from bs4 import BeautifulSoup


# Seed URL, Keyword, Maximum depth can be changed by updating their value here :
SEED_URL="https://en.wikipedia.org/wiki/Tropical_cyclone"
KEYWORD= "rain"
MAX_DEPTH = 6

# Global Constants
PREFIX_URL ="https://en.wikipedia.org"
POLITE_WAIT_TIME = 1
FILE_NUMBER = 1
MAX_CRAWL_PAGES = 1000


def links_to_follow(href):
    """Retains links that start with '/wiki/'.
    Ignores administrative links (links that contain ':')
    """
    return href and href.startswith("/wiki/")  and ":" not in href


def download_page(url, soup):
    """Downloads the raw html content of a given page extracted by the Beautiful soup parser.
    Stores the content in text file, with the url of the page at the top of the file.
    """ 
    global FILE_NUMBER
    with io.open(str(FILE_NUMBER)+".txt", "w", encoding="utf-8") as textfile:
        textfile.write(str(url+ "\n\n"))
        textfile.write(soup.prettify())
    FILE_NUMBER = FILE_NUMBER + 1


def append_url_to_file(url):
    """Adds the given url to the end of the textfile CrawledPageList.txt
    containing names of already crawled urls.
    """
    with io.open("CrawledPageList.txt", "a", encoding="utf-8") as textfile:
        textfile.write(url + "\n")

def fetch_page_content(url):
    """Fetches the html page coressponding to given url and downloads it into a text file.
    Returns the relevant body content of html page.
    """
    try:        
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")

        #Checking if the page is a redirected page.
        redirectedSpan = soup.find_all("span", {"class" : "mw-redirectedfrom"})
        if redirectedSpan:
            print("Skipping redirected page . . .")
            return None

        #download the document
        download_page(url,soup)
        append_url_to_file(url)

        # Fetch relevant content
        return soup.find("div", id="bodyContent")

    except Exception as e:
        print("Error occured while fetching page. .")
        
    

def keyword_matched(link,keyword):
    """Return true if the link contains a href or anchor text 
    that matches the given keyword. Otherwise return false.
    """
    href = link.get("href")
    anchor = link.text

    href_start_matcher = re.compile(r'.*(_|/){0}.*'.format(keyword), re.I)
    href_end_matcher = re.compile(r'.*{0}(_|/).*'.format(keyword), re.I)
    anchor_start_matcher = re.compile(r'.*(^|\s){0}.*'.format(keyword), re.I)
    anchor_end_matcher = re.compile(r'.*{0}($|\s).*'.format(keyword), re.I)

    href_matched =  href_start_matcher.match(href) or href_end_matcher.match(href)
    anchor_matched = anchor_start_matcher.match(anchor) or anchor_end_matcher.match(anchor)
    if href_matched or anchor_matched:
        return True

def filter_links_by_key(links,keyword):
    """Returns a filtered list of links that is filtered based on the given keyword."""
    matched_links = []
    for link in links:
        if keyword_matched(link,keyword):
            matched_links.append(link)               
    return matched_links


def fetch_page_links(page_content, keyword):
    """Returns a list of links extracted from the given page content.
    If a keyword other than empty string is provided, the links are filtered based on the keyword.
    """
    links = page_content.find_all("a", href = links_to_follow)
    if keyword == "":
        return links
    else:
        return filter_links_by_key(links,keyword)
        

def crawl_action(links_to_crawl, depth , keyword):
    """ Performs crawling of webpages by a breadth first approach.
    Using a deque as a FIFO structure gives importance to earlier hyperlinks within the same depth.
    """
    print ("Starting Crawl . . .")

    crawled_pages = []
    while depth <= MAX_DEPTH:
        next_level_links = []
        while (len(crawled_pages) < MAX_CRAWL_PAGES and len(links_to_crawl) > 0 ):

            # Politeness policy of time delay between requests.
            time.sleep(POLITE_WAIT_TIME)

            try:
                
                # Fetch the webpage content
                url = links_to_crawl.popleft()
                page_content = fetch_page_content(url)

                if page_content:
                        
                    # Filter the links in the page and add to 'next_level_links' to be crawled next.
                    for link in fetch_page_links(page_content, keyword):
                        # treat the link to add domain in the start
                        link = str(PREFIX_URL + link.get("href")) 
                        if ((link not in crawled_pages) and (link not in links_to_crawl) and (link not in next_level_links)):
                            next_level_links.append(link)

                    # Finished crawling this page        
                    crawled_pages.append(url)
                    print("Depth : " + str(depth) + "; Crawled Page: "+url)
            except:
                print("Error occured while crawling . . .")
                continue

        # Add the new links to the end of the deque.
        links_to_crawl.extend(next_level_links)
        
        # Move to next depth    
        depth = depth + 1
    return depth
        
        

def Crawler(start_page,keyword):

    # Calculating program execution time
    start_time = time.time()

    # Initializations.
    links_to_crawl = collections.deque()
    links_to_crawl.append(start_page)
    current_depth = 1 #Depth of first URL = 1.

    # Preparing a new text file that maintains a list of all crawled urls.
    textfile = io.open("CrawledPageList.txt", "w", encoding="utf-8") 
    textfile.close()
  
    # Starts the crawl. 
    current_depth = crawl_action(links_to_crawl, current_depth, keyword)
    print("\nEnding Crawl . . .")
    print("Total time taken for execution = %s seconds." %(time.time() - start_time))

def main():
    print("Press 1 for Task 1 : Unfocused Crawling.")
    print("Press 2 for Task 2 : Focused Crawling.")
    user_choice = input("Enter your option: ")

    if user_choice == "1":
        print ("\nYou chose Unfocused Crawling")
        Crawler(SEED_URL, "")
        
    elif user_choice == "2":
        print ("\nYou chose Focused Crawling")
        Crawler(SEED_URL, KEYWORD)
    else:
        print("\nInvalid input. Aborting . .")

# Entry point to the program:
main()
