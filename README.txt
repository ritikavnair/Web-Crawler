****************** WEB CRAWLER *****************

----------------------------------------------------------------------------------------------
----------------------------------- Setup ---------------------------------------------------
---------------------------------------------------------------------------------------------
This code requires the following software packages for it to run successfully:
1. Python 3.6.3
	Can be downloaded from "https://www.python.org/downloads/"
2. BeautifulSoup package
	Can be downloaded from "https://www.crummy.com/software/BeautifulSoup/"
	Can be installed using pip, by entering the following command 
	in Terminal or Command Line :

		 pip install beautifulsoup4

3. Requests package
	Can be installed using pip, by entering the following command 
	in Terminal or Command Line :

		pip install requests

--------------------------------------------------------------------------------------------
-------------------------------------- Run--------------------------------------------------
--------------------------------------------------------------------------------------------

1. Place the file 'WikiWebCrawler.py' in new folder.
2. Open Terminal (or Windows PowerShell for Windows) and make sure
   that the present working directory is the folder where you have placed 'WikiWebCrawler.py'.
3. Make sure python's path is set in the environment variables of your computer.
4. Run the code by entering the following command:

		python WikiWebCrawler.py

5. The program asks you which task you want to perform and 
   prompts you for an answer.

		Press 1 for Task 1 : Unfocused Crawling.
		Press 2 for Task 2 : Focused Crawling.
		Enter your option: 

   Enter either 1 or 2 depending on your choice.

   By default the seed URL is "https://en.wikipedia.org/wiki/Tropical_cyclone"
   and the keyword is "rain"
   and the depth is 6

   If you need to change these values, you can do so in the top section against the names:
   SEED_URL , KEYWORD , MAX_DEPTH 

6. At the end, the maximum depth the crawler could reach is printed on the console.
7. The raw html of all the pages crawled is saved in the present working directory.
   Also a textfile named 'CrawledPageList.txt' is generated which lists all the URLs crawled 
   by the crawler.



References:
-----------

https://learnpythonthehardway.org
http://docs.python-requests.org/en/master/user/quickstart/
http://www.tutorialspoint.com/python/
http://www.pythonforbeginners.com/python-on-the-web/web-scraping-with-beautifulsoup/
	

