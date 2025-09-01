import chromadb
from chromadb.utils import embedding_functions
import os
from typing import List, Dict
import re
from dotenv import load_dotenv

load_dotenv()


class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=os.getenv('CHROMA_DB_PATH', './chroma_db'))

        # Use OpenAI embeddings
        openai_ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.getenv('OPENAI_API_KEY'),
            model_name="text-embedding-3-small"
        )

        # Set the environment variable that ChromaDB expects
        os.environ['CHROMA_OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name="book_summaries",
            embedding_function=openai_ef
        )

    def load_books_from_file(self, file_path: str):
        """Load book summaries from text file and add to vector store"""
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Parse the book summaries
        books = self.parse_book_summaries(content)

        # Clear existing data
        try:
            # Get all existing IDs and delete them
            existing_data = self.collection.get()
            if existing_data['ids']:
                self.collection.delete(ids=existing_data['ids'])
        except Exception as e:
            print(f"Note: Could not clear existing data: {e}")
            # This is fine for a fresh database

        # Add books to collection
        documents = []
        metadatas = []
        ids = []

        for i, book in enumerate(books):
            documents.append(book['summary'])
            metadatas.append({'title': book['title']})
            ids.append(f"book_{i}")

        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

        print(f"Loaded {len(books)} books into vector store")

    def parse_book_summaries(self, content: str) -> List[Dict]:
        """Parse book summaries from the text format"""
        books = []
        sections = content.split('## Title: ')[1:]  # Skip first empty element

        for section in sections:
            lines = section.strip().split('\n', 1)
            if len(lines) >= 2:
                title = lines[0].strip()
                summary = lines[1].strip()
                books.append({
                    'title': title,
                    'summary': summary
                })

        return books

    def search_books(self, query: str, n_results: int = 3) -> List[Dict]:
        """Search for books based on query"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )

        books = []
        if results['documents'][0]:  # Check if we have results
            for i in range(len(results['documents'][0])):
                books.append({
                    'title': results['metadatas'][0][i]['title'],
                    'summary': results['documents'][0][i],
                    'distance': results['distances'][0][i] if results['distances'] else 0
                })

        return books

    def get_all_titles(self) -> List[str]:
        """Get all book titles in the database"""
        results = self.collection.get()
        return [metadata['title'] for metadata in results['metadatas']]


# Book summaries dictionary for the tool
book_summaries_dict = {
    "1984": (
        "George Orwell's novel describes a dystopian society under total state control. "
        "People are constantly watched by 'Big Brother,' and free thought is considered a crime. "
        "Winston Smith, the main character, tries to resist this oppressive regime. "
        "It is a story about freedom, truth, and ideological manipulation. The novel explores "
        "themes of surveillance, propaganda, and the individual's struggle against totalitarian power."
    ),
    "The Hobbit": (
        "Bilbo Baggins, a comfortable hobbit with no adventures, is taken by surprise "
        "when he is invited on a quest to recover the dwarves' treasure guarded by the dragon Smaug. "
        "Along the way, he discovers courage and inner resources he never knew he had. "
        "The story is full of fantastic creatures, unexpected friendships, and tense moments. "
        "It's a tale of personal growth, adventure, and discovering one's true potential."
    ),
    "To Kill a Mockingbird": (
        "Harper Lee's masterpiece set in 1930s Alabama follows Scout Finch as she grows up "
        "in a racially divided town. Her father, lawyer Atticus Finch, defends a black man "
        "falsely accused of rape, teaching valuable lessons about moral courage. The novel "
        "explores themes of prejudice, justice, and the loss of innocence through a child's eyes."
    ),
    "The Lord of the Rings": (
        "J.R.R. Tolkien's epic fantasy follows Frodo Baggins on his quest to destroy the One Ring "
        "and defeat the Dark Lord Sauron. Accompanied by a fellowship of diverse companions, "
        "they journey through Middle-earth facing incredible dangers. This masterwork explores "
        "themes of friendship, sacrifice, good versus evil, and the corrupting nature of power."
    ),
    "Pride and Prejudice": (
        "Jane Austen's beloved novel follows Elizabeth Bennet as she navigates 19th-century "
        "English society, dealing with issues of marriage, money, and social class. Her relationship "
        "with the proud Mr. Darcy evolves from initial dislike to deep love. The story brilliantly "
        "examines themes of love, social expectations, and personal growth."
    ),
    "The Catcher in the Rye": (
        "J.D. Salinger's controversial novel follows Holden Caulfield, a troubled teenager who "
        "wanders through New York City after being expelled from prep school. Through his cynical "
        "observations, the novel explores themes of alienation, depression, and the difficulty "
        "of growing up in a world he perceives as fake and superficial."
    ),
    "Brave New World": (
        "Aldous Huxley's dystopian masterpiece depicts a futuristic society where humans are "
        "genetically engineered and conditioned for specific roles. The story follows Bernard Marx "
        "and John 'the Savage' as they challenge their controlled world. The novel examines themes "
        "of technology, social control, individual freedom, and what it means to be human."
    ),
    "The Great Gatsby": (
        "F. Scott Fitzgerald's Jazz Age classic tells the story of Jay Gatsby's obsessive pursuit "
        "of his lost love, Daisy Buchanan. Through narrator Nick Carraway's eyes, we witness the "
        "decadence and moral emptiness of the wealthy elite. The novel explores themes of the "
        "American Dream, wealth, love, and social class in 1920s America."
    ),
    "Harry Potter and the Philosopher's Stone": (
        "J.K. Rowling's magical tale begins when Harry Potter discovers he's a wizard on his 11th "
        "birthday and enters Hogwarts School of Witchcraft and Wizardry. Along with friends Ron "
        "and Hermione, he faces challenges and discovers his connection to the dark wizard Voldemort. "
        "The story combines magic, friendship, courage, and the eternal battle between good and evil."
    ),
    "Dune": (
        "Frank Herbert's science fiction epic set on the desert planet Arrakis follows Paul Atreides "
        "as he becomes embroiled in a struggle for control of spice melange, the most valuable "
        "substance in the universe. The novel explores complex themes of politics, religion, ecology, "
        "and human potential in an intricate interstellar society."
    ),
    "All Quiet on the Western Front": (
        "Erich Maria Remarque's powerful anti-war novel follows Paul Bäumer, a German soldier "
        "during World War I, as he experiences the brutal realities of trench warfare. The story "
        "depicts the physical and psychological trauma of war, the loss of innocence, and the "
        "profound disconnect between soldiers and civilian life."
    ),
    "The Chronicles of Narnia: The Lion, the Witch and the Wardrobe": (
        "C.S. Lewis's fantasy classic follows four children who discover the magical land of Narnia "
        "through a wardrobe. They become involved in the struggle between the noble lion Aslan and "
        "the evil White Witch. The story combines fantasy adventure with deeper themes of sacrifice, "
        "redemption, and the eternal battle between good and evil."
    )
}


def get_summary_by_title(title: str) -> str:
    """Tool function to get detailed summary by exact title"""
    if title in book_summaries_dict:
        return book_summaries_dict[title]
    else:
        return f"Sorry, I don't have a detailed summary for '{title}'. Please check the title spelling or try a different book."