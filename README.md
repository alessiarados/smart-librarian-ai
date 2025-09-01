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
## macOS/Linux:
source venv/bin/activate

3. Install Dependencies
bashpip install -r requirements.txt

4. Environment Configuration
bash# Copy the environment template
cp .env.example .env

## Edit .env file and add your OpenAI API key
## Windows:

notepad .env
## macOS/Linux:

nano .env

Add your API key to the .env file:

OPENAI_API_KEY=your_openai_api_key_here

CHROMA_OPENAI_API_KEY=your_openai_api_key_here

CHROMA_DB_PATH=./chroma_db

API_HOST=localhost

API_PORT=8000

## Running the Application
Method 1: Full Application (Recommended) 

Start both backend and frontend:

bash# Terminal 1 - Start the backend API

python -m backend.api

## Terminal 2 - Start the frontend (keep backend running)

streamlit run frontend/app.py

Method 2: API Only

For API-only usage:

bashpython -m backend.api

Access API documentation at: http://localhost:8000/docs

## Usage 
## Web Interface

Open your browser to http://localhost:8501

Ask for book recommendations using natural language:

"I want a book about freedom and social control"

"What do you recommend if I love fantasy stories?"

"Books about friendship and magic"

"What is 1984 about?"



## API Endpoints

GET / - Health check

POST /chat - Get book recommendations

GET /books - List all available books

GET /search?query=<text> - Search books by query


## Book Database

The system includes 12 classic books:

- 1984 (George Orwell)
- The Hobbit (J.R.R. Tolkien)
- To Kill a Mockingbird (Harper Lee)
- The Lord of the Rings (J.R.R. Tolkien)
- Pride and Prejudice (Jane Austen)
- The Catcher in the Rye (J.D. Salinger)
- Brave New World (Aldous Huxley)
- The Great Gatsby (F. Scott Fitzgerald)
- Harry Potter and the Philosopher's Stone (J.K. Rowling)
- Dune (Frank Herbert)
- All Quiet on the Western Front (Erich Maria Remarque)
- The Chronicles of Narnia (C.S. Lewis)

## How It Works

User Query: User asks for book recommendations

Semantic Search: Query is converted to embeddings and searched in ChromaDB

AI Processing: GPT-4o-mini analyzes results and generates recommendations

Tool Calling: AI automatically calls get_summary_by_title() for detailed information

Response: User receives conversational recommendations with full summaries
