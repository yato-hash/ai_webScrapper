import os
from dotenv import load_dotenv
from selenium.webdriver import Remote
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup

load_dotenv()
SBR_WEBDRIVER = os.getenv("SBR_WEBDRIVER")

def scrape_website(website):
    print("Launching Bright Data Chrome instance...")

    # Establish a remote Chrome session through Bright Data
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')

    with Remote(command_executor=sbr_connection, options=Options()) as driver:
        driver.get(website)
        print("Page loaded. Waiting for CAPTCHA solve...")

        # CAPTCHA handling
        result = driver.execute(
            'executeCdpCommand',
            {
                'cmd': 'Captcha.waitForSolve',
                'params': {'detectTimeout': 10000},
            },
        )

        print("Captcha solve status:", result['value']['status'])
        print("Scraping page content...")
        html = driver.page_source
        return html

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content,'html.parser')
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content,'html.parser')

    for script_or_style in soup(['script','style']):#removing script and style from the soup
        script_or_style.extract()

    cleaned_content = soup.get_text(separator='\n')
    cleaned_content = '\n'.join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()#remove empty whitestrips
    )
    return cleaned_content


def split_dom_content(dom_content,max_length=6000):
    return[
        dom_content[i:i+max_length] for i in range(0,len(dom_content),max_length)
    ]