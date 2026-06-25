# AI Web Scraper with LLM Integration

An automated web scraping pipeline that extracts dynamic content from any website and uses **Llama 3** (via Ollama) to intelligently parse it based on natural-language instructions — no manual CSS selectors or regex required.

## How It Works

1. **Scrape** — Enter any URL. The app launches a remote, CAPTCHA-solving browser session (via Bright Data's Browser API) using Selenium to fully render the page, including dynamic/JavaScript-loaded content.
2. **Clean** — BeautifulSoup strips out scripts, styles, and noise, leaving just the readable text content of the page.
3. **Chunk** — The cleaned content is split into ~6,000-character chunks to fit within the LLM's context window.
4. **Parse** — Describe what you want extracted in plain English (e.g. *"Get all product names and prices"*). Each chunk is sent to a locally-running **Llama 3** model through LangChain, which returns only the matching information — no extra commentary.

## Tech Stack

- **Frontend**: Streamlit
- **Scraping**: Selenium + Bright Data Browser API (handles CAPTCHAs, anti-bot detection, and dynamic rendering)
- **Parsing**: BeautifulSoup4 (HTML cleaning), LangChain + Ollama (Llama 3) for LLM-based extraction
- **Language**: Python

## Demo

<img width="1893" height="946" alt="image" src="https://github.com/user-attachments/assets/6513e6c2-0dd4-4fd2-a764-5cbd08873b16" />


## Setup

### Prerequisites
- Python 3.9+
- [Ollama](https://ollama.com) installed locally, with the Llama 3 model pulled:
  ```bash
  ollama pull llama3
  ```
- A [Bright Data](https://brightdata.com) account with a **Browser API** zone (used for CAPTCHA-solving and rendering dynamic pages)

### Installation

```bash
git clone https://github.com/yato-hash/ai_webScrapper.git
cd ai_webScrapper
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
SBR_WEBDRIVER=https://brd-customer-<CUSTOMER_ID>-zone-<ZONE_NAME>:<PASSWORD>@brd.superproxy.io:9515
```

Get this connection string from your Bright Data dashboard under **Web Access APIs → Browser API → [your zone] → Overview**.

### Run

```bash
streamlit run main.py
```

The app will open in your browser at `localhost:8501`.

## Usage

1. Paste a URL and click **"Scrape Site"**
2. Expand **"View DOM Content"** to inspect the raw cleaned text (optional)
3. Type a description of what you want extracted, e.g.:
   - *"List all article headlines"*
   - *"Extract email addresses mentioned on the page"*
   - *"Get the price and availability of each product"*
4. Click **"Parse Content"** — the matching data will be displayed below

## Project Structure

```
.
├── main.py      # Streamlit UI and app flow
├── scrape.py    # Selenium scraping + HTML cleaning logic
├── parse.py     # LangChain + Ollama (Llama 3) parsing logic
└── requirements.txt
```

## Future Improvements

- Add a local-Selenium fallback mode that doesn't require a Bright Data account, for simpler/non-protected sites
- Export parsed results as CSV/JSON
- Support multiple LLM backends (OpenAI, Gemini) as alternatives to Llama 3
- Cache scraped pages to avoid redundant requests during iterative prompt testing

## License

MIT
