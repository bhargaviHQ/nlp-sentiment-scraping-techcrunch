## NLP Sentiment Analysis with Web Scraping of Articles from TechCrunch
This project involves scraping over 9000+ articles related to [Artificial Intelligence from TechCrunch](https://techcrunch.com/category/artificial-intelligence/), performing sentiment analysis, and providing an interactive dashboard where users can filter articles based on sentiment and company mentions. The data is stored in MongoDB Atlas, and the analysis is visualized with Streamlit.

### Libraries and Tools

- **Web Scraping:** BeautifulSoup ; parsing HTML content from the TechCrunch articles.
- **Sentiment Analysis:** VADER (from NLTK) for sentiment analysis
- **Language Detection:** langid library
- **Data Storage:** MongoDB Atlas (for storing scraped data)
- **Visualization:** Streamlit (for the interactive dashboard)

###  Overview

1. **Web Scraping:** 
   - The project starts by scraping articles related to Artificial Intelligence from the TechCrunch website.
   - [`web-scraper-01.py`](https://github.com/bhargaviHQ/nlp-sentiment-scraping-techcrunch/tree/main/web-scraper/web-scraper-01.py) handles the scraping of articles from the first page, while [`web-scraper-02.py`](https://github.com/bhargaviHQ/nlp-sentiment-scraping-techcrunch/tree/main/web-scraper/web-scraper-02.py) scrapes the remaining pages, up to a total of 333 pages.
   
2. **Sentiment Analysis:** 
   - Each article is analyzed for sentiment using VADER sentiment analysis from the NLTK library. Articles are classified as having positive, negative, or neutral sentiment.
   - The sentiment score is stored in MongoDB for further filtering and display. View file [`main.py`](https://github.com/bhargaviHQ/nlp-sentiment-scraping-techcrunch/blob/main/main.py)

3. **Language Detection:** 
   - The language of each article is detected using the `langid` library, ensuring that articles in different languages are handled appropriately.

4. **MongoDB Storage:** 
   - All the articles and their metadata, including sentiment analysis results, are stored in MongoDB Atlas.

5. **Interactive Dashboard:**
   - [`app.py`](https://github.com/bhargaviHQ/nlp-sentiment-scraping-techcrunch/blob/main/app.py) contains the Streamlit code that serves as the interactive dashboard.
   - Users can filter articles based on sentiment and top companies mentioned.
   - The dashboard also allows users to search for casual mentions of companies in other articles.

###  Setup and Installation

####  Install required dependencies:

```bash
git clone https://github.com/bhargaviHQ/nlp-sentiment-scraping-techcrunch.git
```
```bash
cd nlp-sentiment-scraping-techcrunch
pip install -r requirements.txt
```
#### Run the Streamlit app:

```bash
streamlit run app.py
```
 
### MongoDB Atlas Setup
Setup a [MongoDB Atlas account](https://www.mongodb.com/docs/guides/atlas/account/) and replace the connection string in main.py with your own MongoDB Atlas connection URL.

###  Features
User-friendly dashboard with filters for sentiment and company-related metrics.
- **Sentiment Filtering:** Filter articles based on sentiment (positive, negative, neutral).
- **Company Mentions:** Filter articles based on mentions of top companies in the AI field.
- **Casual Mentions:** View company mentions in relation to other companies or articles.

###  Screenshots
View [screenshots](https://github.com/bhargaviHQ/nlp-sentiment-scraping-techcrunch/tree/main/screenshots) of the application in action

![Project Flow](https://github.com/bhargaviHQ/nlp-sentiment-scraping-techcrunch/blob/main/screenshots/flow.jpg)

###  Project Structure
- app.py - Streamlit interactive dashboard code
- main.py - MongoDB Atlas connection and sentiment analysis code
- requirements.txt - List of required libraries
- web-scraper/web-scraper-01.py - Web scraper for scraping articles from the first page of TechCrunch
- web-scraper/web-scraper-02.py - Web scraper for scraping articles from subsequent pages (up to 333 pages)
- screenshots/ - Folder containing screenshots of the dashboard


### License

[MIT](https://choosealicense.com/licenses/mit/)
