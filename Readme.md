# LinkedIn Generator and Value App

This project combines two functionalities into a single streamlined application:
1. **LinkedIn Generator**: Create professional and concise LinkedIn connection notes.
2. **Competitor Analysis (Value App)**: Analyzes competitors' websites to extract relevant pages and generate insights about pricing, sales channels, value propositions, and more.

---

## Architecture Overview

### 1. **Core Components**
- **Streamlit UI**: Provides an interactive interface for user input and result display.
- **FastAPI Backend**: Handles API requests for both Value App and LinkedIn Note Generator.
- **OpenAI Integration**: Uses GPT models for text analysis, title relevance checks, summarization, and generating LinkedIn notes.
- **LangChain**: Processes and indexes website data for contextual question-answering capabilities.

### 2. **Agent Workflow**

#### Competitor Analysis (Value App)
1. **Input**: The user provides a competitor's website URL.
2. **Homepage Crawling**:
   - The system crawls the homepage, extracting URLs and titles of pages.
   - Each URL is validated to ensure it belongs to the same domain.
3. **Title Analysis**:
   - Page titles are sent to the OpenAI GPT model.
   - The model identifies relevant titles based on their potential utility (e.g., pricing, product launches, value propositions).
4. **Content Extraction**:
   - Relevant pages are fetched, and their content is extracted and cleaned using BeautifulSoup.
   - Extracted content is saved in a local cache to avoid redundant processing.
5. **LangChain Indexing**:
   - The cleaned content is split into manageable chunks using `CharacterTextSplitter`.
   - A FAISS vector store is created with OpenAI embeddings to enable efficient similarity-based searches.
6. **Question Answering**:
   - The user can ask questions related to the analyzed content via a chatbot.
   - Relevant chunks are retrieved using LangChain's similarity search.
   - OpenAI GPT generates a summarized response based on the retrieved content.

#### LinkedIn Note Generator
1. **Input**: The user provides recipient details (name, headline, about section, purpose) and sender name.
2. **Prompt Construction**:
   - A detailed prompt is generated for OpenAI GPT, incorporating the user's inputs.
3. **Response Generation**:
   - OpenAI GPT generates a concise, professional connection note tailored to the provided context.
4. **Output**: The note is displayed in the Streamlit UI for the user.

---

## Decision-Making Process

### **Competitor Analysis**
1. **Relevance Filtering**:
   - GPT's natural language understanding evaluates page titles for their relevance.
   - The decision to include a page is based on whether the title aligns with key business insights.
2. **Dynamic Summarization**:
   - When answering user queries, the agent retrieves the most relevant chunks of content.
   - GPT generates a focused summary based on the question, ensuring concise and useful responses.

### **LinkedIn Note Generation**
- **Personalization**:
  - The agent identifies key details from the recipient's profile (headline, about section).
  - These details are used selectively to align with the connection's purpose.
- **Tone Analysis**:
  - GPT ensures the note maintains a polite, professional, and concise tone.
- **Efficiency**:
  - Redundant or irrelevant information is excluded, focusing solely on the connection's purpose.

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
git clone https://github.com/nishuastic/company_assistant.git
cd company_assistant
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