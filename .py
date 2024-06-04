from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient
import requests
import time
import uuid
from datetime import datetime

# Twitter credentials and ProxyMesh credentials
TWITTER_USERNAME = 'your_twitter_username'
TWITTER_PASSWORD = 'your_twitter_password'
PROXYMESH_URL = 'http://your_proxymesh_url:port'

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['twitter_trends']
collection = db['trends']

# Function to get a new IP address from ProxyMesh
def get_new_proxy():
    return {'http': PROXYMESH_URL, 'https': PROXYMESH_URL}

# Function to fetch top trending topics
def fetch_trending_topics():
    # Set up Selenium with ProxyMesh
    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=%s' % PROXYMESH_URL)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Open Twitter login page
    driver.get('https://twitter.com/login')
    time.sleep(5)
    
    # Log in to Twitter
    username = driver.find_element(By.NAME, 'session[username_or_email]')
    password = driver.find_element(By.NAME, 'session[password]')
    username.send_keys(TWITTER_USERNAME)
    password.send_keys(TWITTER_PASSWORD)
    password.send_keys(Keys.RETURN)
    time.sleep(5)
    
    # Navigate to the "What's Happening" section
    driver.get('https://twitter.com/explore/tabs/trending')
    time.sleep(5)
    
    # Fetch the trending topics
    trends = driver.find_elements(By.XPATH, '//div[@aria-label="Timeline: Trending now"]//span')
    trending_topics = [trend.text for trend in trends[:5]]
    
    # Close the driver
    driver.quit()
    
    # Get current IP address
    current_ip = requests.get('http://api.ipify.org').text
    
    # Create a unique ID and store the result in MongoDB
    unique_id = str(uuid.uuid4())
    end_time = datetime.now()
    trend_data = {
        '_id': unique_id,
        'trend1': trending_topics[0],
        'trend2': trending_topics[1],
        'trend3': trending_topics[2],
        'trend4': trending_topics[3],
        'trend5': trending_topics[4],
        'end_time': end_time,
        'ip_address': current_ip
    }
    collection.insert_one(trend_data)
    
    return trend_data

if __name__ == '__main__':
    fetch_trending_topics()
