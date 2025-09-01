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
