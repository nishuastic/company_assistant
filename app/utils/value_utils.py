import os
import requests
from dotenv import load_dotenv

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from openai import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.schema import Document

import pickle

load_dotenv()

CACHE_DIR = "cache"
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Function to crawl homepage and collect URLs with titles
def crawl_homepage(base_url):
    visited_urls = set()
    page_links = []

    def is_valid_url(url):
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme) and base_url in url

    try:
        print(f"Crawling homepage: {base_url}")
        response = requests.get(base_url, timeout=10)
        if response.status_code != 200:
            print(f"Failed to retrieve {base_url}: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        for a_tag in soup.find_all("a", href=True):
            link = urljoin(base_url, a_tag["href"])
            if link not in visited_urls and is_valid_url(link):
                visited_urls.add(link)
                title = a_tag.get_text(strip=True) or "No Title"
                page_links.append({"url": link, "title": title})

    except Exception as e:
        print(f"Error crawling {base_url}: {e}")

    return page_links


# Function to analyze titles using OpenAI
def analyze_titles_with_openai(titles):
    messages = [
        {
            "role": "system",
            "content": """You are an assistant that analyzes a list of page titles and identifies their relevance. 
            Our purpose is to find relevant pages of our competitors which might help us understand their pricing,
            sales channels, value propositions.""",
        },
        {
            "role": "user",
            "content": f"Here is a list of page titles: {', '.join(titles)}. Please check the titles and only return those which might be relevant to us. No text. Just a list of titles without indexing in the same formating that was given to you.",
        },
    ]

    try:
        print("Sending titles to OpenAI for analysis...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", messages=messages
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return None


# Function to fetch and filter relevant pages
def fetch_and_filter_relevant_pages(base_url, relevant_titles, all_pages):
    relevant_pages = [page for page in all_pages if page["title"] in relevant_titles]
    filtered_content = {}

    for page in relevant_pages:
        try:
            print(f"Fetching relevant page: {page['url']}")
            response = requests.get(page["url"], timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                text = soup.get_text(separator=" ", strip=True)
                filtered_content[page["url"]] = text
            else:
                print(f"Failed to fetch {page['url']}: {response.status_code}")
        except Exception as e:
            print(f"Error fetching {page['url']}: {e}")

    return filtered_content


# Function to save content to cache
def save_to_cache(base_url, data):
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    with open(os.path.join(CACHE_DIR, f"{urlparse(base_url).netloc}.pkl"), "wb") as f:
        pickle.dump(data, f)


# Function to load content from cache
def load_from_cache(base_url):
    cache_file = os.path.join(CACHE_DIR, f"{urlparse(base_url).netloc}.pkl")
    if os.path.exists(cache_file):
        with open(cache_file, "rb") as f:
            return pickle.load(f)
    return None


# Function to create a LangChain context
def create_langchain_context(filtered_content):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    # Convert filtered_content to the expected format
    documents = [
        {"page_content": content, "metadata": {"source": url}}
        for url, content in filtered_content.items()
    ]

    # Split the documents into smaller chunks
    split_documents = []
    for doc in documents:
        chunks = text_splitter.split_text(doc["page_content"])
        split_documents.extend(
            [{"page_content": chunk, "metadata": doc["metadata"]} for chunk in chunks]
        )

    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    vectorstore = FAISS.from_documents(
        [Document(**doc) for doc in split_documents], embeddings
    )

    return vectorstore


# Main processing logic
def process_value_app_logic(base_url):
    cached_data = load_from_cache(base_url)
    if cached_data:
        print("Cache found. Using cached data.")
        return cached_data

    # If cache not found, process data
    print("No cache found. Processing...")
    pages = crawl_homepage(base_url)
    titles = [page["title"] for page in pages]
    relevant_titles = analyze_titles_with_openai(titles)

    if not relevant_titles:
        print("No relevant titles found.")
        return {}

    filtered_content = fetch_and_filter_relevant_pages(base_url, relevant_titles, pages)
    save_to_cache(base_url, filtered_content)

    return filtered_content


# Function for querying the vectorstore
def query_vectorstore(vectorstore, query):
    results = vectorstore.similarity_search(query, k=3)
    combined_results = "\n".join([result.page_content for result in results])

    # Summarize the results using OpenAI
    try:
        prompt = f"""
        You are a helpful assistant. Summarize the following content in a concise manner that answers the user's question:
        User's Question: {query}
        Content: {combined_results}
        """
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=150,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error summarizing: {e}")
        return "Error generating response."
