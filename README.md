# Smart Librarian AI

An AI-powered book recommendation system that uses Retrieval-Augmented Generation (RAG) with ChromaDB vector database and OpenAI GPT-4o-mini for intelligent book suggestions.

## Features

- **Semantic Search**: Uses ChromaDB with OpenAI embeddings for finding books by meaning, not just keywords
- **Intelligent Recommendations**: GPT-4o-mini provides conversational, context-aware book suggestions
- **Tool Integration**: Automatic detailed summary retrieval using OpenAI function calling
- **Content Filtering**: Built-in inappropriate language detection and filtering
- **Web Interface**: Clean Streamlit frontend for easy interaction
- **REST API**: FastAPI backend with comprehensive endpoints
- **Vector Database**: Persistent ChromaDB storage for fast semantic queries

## Technology Stack

- **AI Models**: OpenAI GPT-4o-mini, text-embedding-3-small
- **Vector Database**: ChromaDB for semantic search
- **Backend**: FastAPI with Pydantic models
- **Frontend**: Streamlit web application
- **Languages**: Python 3.9+
- **Dependencies**: OpenAI, ChromaDB, Streamlit, FastAPI, Uvicorn

## Prerequisites

- Python 3.9 or higher
- OpenAI API key (Get one here)
- Git (for cloning)

## Installation & Setup
1. Clone the Repository
bashgit clone https://github.com/alessiarados/smart-librarian-ai.git
cd smart-librarian-ai

2. Create Virtual Environment
bash# Create virtual environment
python -m venv venv

## Activate virtual environment
## Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

3. Install Dependencies
bashpip install -r requirements.txt

4. Environment Configuration
bash# Copy the environment template
cp .env.example .env

# Edit .env file and add your OpenAI API key
# Windows:

notepad .env
# macOS/Linux:

nano .env

Add your API key to the .env file:

OPENAI_API_KEY=your_openai_api_key_here

CHROMA_OPENAI_API_KEY=your_openai_api_key_here

CHROMA_DB_PATH=./chroma_db

API_HOST=localhost

API_PORT=8000
