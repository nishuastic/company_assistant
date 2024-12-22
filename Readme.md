# LinkedIn Generator and Value App

This project combines two functionalities into a single streamlined application:
1. **LinkedIn Generator**: Create professional and concise LinkedIn connection notes.
2. **Value App**: Analyze competitor websites to extract relevant insights, perform Q&A on the extracted content, and summarize the results using AI.

---

## Features

### LinkedIn Generator
- Generate personalized LinkedIn connection notes based on the recipient's details, purpose of connection, and sender's information.
- AI-powered generation ensures the message is concise, polite, and professional.

### Value App
- **Website Analysis**: Crawl competitor websites and analyze page titles to find relevant sections like pricing, blogs, and about pages.
- **Content Extraction**: Fetch and clean text content from relevant pages.
- **AI-Powered Q&A**: Create a searchable context using LangChain and FAISS to allow questions about the extracted content.
- **AI Summarization**: Generate concise summaries of the answers to user queries.

---

## Installation

### Prerequisites
- Python 3.8 or later
- Environment variable for OpenAI API key (`OPENAI_API_KEY`) must be set.

### Clone the Repository
```bash
git clone https://github.com/your-repository-name.git
cd your-repository-name
```

### Running
1. Start the Backend Server. The backend is built using FastAPI. Start the server with:
```bash
uvicorn app.main:app --reload
```
By default, it runs at http://localhost:8000.

2. Start the Streamlit UI. The frontend is built using Streamlit. Start the UI with:
```bash
streamlit run app/streamlit_ui.py
```
The UI will open in your default browser, typically at http://localhost:8501