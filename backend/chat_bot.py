import openai
import json
from typing import List, Dict
import os
from dotenv import load_dotenv
from .vector_store import VectorStore, get_summary_by_title

load_dotenv()


class SmartLibrarian:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.vector_store = VectorStore()

        # Load books into vector store
        try:
            self.vector_store.load_books_from_file('./data/book_summaries.txt')
        except FileNotFoundError:
            print("Warning: book_summaries.txt not found. Please ensure the file exists in the data directory.")

        # Define inappropriate words (you can expand this list)
        self.inappropriate_words = [
            'fuck', 'shit', 'damn', 'bitch', 'bastard', 'asshole',
            'motherfucker', 'cocksucker', 'cunt', 'piss'
        ]

    def contains_inappropriate_language(self, message: str) -> bool:
        """Check if message contains inappropriate language"""
        message_lower = message.lower()
        return any(word in message_lower for word in self.inappropriate_words)

    def get_book_recommendation(self, user_query: str) -> Dict:
        """Get book recommendation with RAG and tool calling"""

        # Check for inappropriate language
        if self.contains_inappropriate_language(user_query):
            return {
                "response": "I appreciate your interest in book recommendations, but I'd prefer to keep our conversation respectful. Could you please rephrase your request without offensive language? I'm here to help you find amazing books to read!",
                "inappropriate_content": True
            }

        # Search vector store for relevant books
        relevant_books = self.vector_store.search_books(user_query, n_results=3)

        if not relevant_books:
            return {
                "response": "I couldn't find any books matching your criteria in my current database. Could you try a different theme or provide more details about what you're looking for?",
                "inappropriate_content": False
            }

        # Prepare context for the LLM
        context = "Based on your interests, here are some relevant books from my database:\n\n"
        for book in relevant_books:
            context += f"**{book['title']}**: {book['summary'][:200]}...\n\n"

        # Define the tool for getting detailed summaries
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_summary_by_title",
                    "description": "Get a detailed summary for a specific book title",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "The exact title of the book"
                            }
                        },
                        "required": ["title"]
                    }
                }
            }
        ]

        # Create the system prompt
        system_prompt = f"""You are a knowledgeable and friendly librarian AI assistant. Your job is to recommend books based on user interests and provide engaging, conversational responses.

Context from book database:
{context}

Guidelines:
1. Recommend 1-2 books that best match the user's request
2. Be conversational and enthusiastic about books
3. After making your recommendation, use the get_summary_by_title tool to provide a detailed summary
4. Explain why you think the book(s) would be a good fit for the user
5. Keep your initial response concise but engaging

Available books in the database: {', '.join(self.vector_store.get_all_titles())}"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ]

        try:
            # Get initial recommendation
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=tools,
                tool_choice="auto",
                temperature=0.7
            )

            assistant_message = response.choices[0].message
            full_response = assistant_message.content or ""

            # Handle tool calls
            if assistant_message.tool_calls:
                messages.append({
                    "role": "assistant",
                    "content": assistant_message.content,
                    "tool_calls": assistant_message.tool_calls
                })

                for tool_call in assistant_message.tool_calls:
                    if tool_call.function.name == "get_summary_by_title":
                        function_args = json.loads(tool_call.function.arguments)
                        title = function_args["title"]

                        # Get detailed summary
                        detailed_summary = get_summary_by_title(title)

                        # Add tool response to messages
                        messages.append({
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": "get_summary_by_title",
                            "content": detailed_summary
                        })

                # Get final response with tool results
                final_response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    temperature=0.7
                )

                full_response = final_response.choices[0].message.content

            return {
                "response": full_response,
                "inappropriate_content": False,
                "recommended_books": [book['title'] for book in relevant_books[:2]]
            }

        except Exception as e:
            return {
                "response": f"I apologize, but I encountered an error while processing your request. Please try again later. Error: {str(e)}",
                "inappropriate_content": False
            }

    def chat(self, message: str) -> str:
        """Main chat interface"""
        result = self.get_book_recommendation(message)
        return result["response"]