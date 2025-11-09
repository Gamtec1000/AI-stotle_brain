# backend/knowledge/embedding_engine.py
"""
AI-stotle Knowledge Base using ChromaDB
Free, fast, and local vector search for scientific knowledge
"""

import chromadb
from chromadb.config import Settings
import os
from typing import List, Dict, Optional
from sentence_transformers import SentenceTransformer
from pathlib import Path

class LocalEmbeddingEngine:
    """
    Knowledge base for AI-stotle using ChromaDB
    Stores and retrieves scientific knowledge for Carls Newton shows
    """

    def __init__(self, persist_directory: str = None):
        """
        Initialize knowledge base with ChromaDB

        Args:
            persist_directory: Path to persist ChromaDB data
        """
        self.persist_directory = persist_directory or os.getenv(
            "CHROMA_PERSIST_DIR",
            "../data/embeddings"
        )

        # Ensure directory exists
        Path(self.persist_directory).mkdir(parents=True, exist_ok=True)

        # Initialize ChromaDB client
        print(f"📚 Initializing ChromaDB at {self.persist_directory}")
        self.client = chromadb.PersistentClient(path=self.persist_directory)

        # Load embedding model (384 dimensions, fast and efficient)
        model_name = os.getenv(
            "EMBEDDING_MODEL",
            "sentence-transformers/all-MiniLM-L6-v2"
        )
        print(f"🔤 Loading embedding model: {model_name}")
        self.embedding_model = SentenceTransformer(model_name)

        # Get or create collections
        self.experiments_collection = self._get_or_create_collection("experiments")
        self.qa_collection = self._get_or_create_collection("qa")

        print("✅ Knowledge base initialized")

    def _get_or_create_collection(self, name: str):
        """Get or create a ChromaDB collection"""
        try:
            return self.client.get_collection(name=name)
        except:
            return self.client.create_collection(
                name=name,
                metadata={"hnsw:space": "cosine"}
            )

    def add_experiments(self,
                       experiments: List[Dict]):
        """
        Add experiments to the knowledge base

        Args:
            experiments: List of experiment dictionaries with:
                - name: Experiment name
                - description: Detailed description
                - category: Science category
                - age_min/age_max: Age range
                - wow_factor: How exciting (1-10)
                - safety_notes: Safety considerations
        """
        if not experiments:
            return

        print(f"🔬 Adding {len(experiments)} experiments...")

        documents = []
        metadatas = []
        ids = []

        for i, exp in enumerate(experiments):
            # Create searchable document
            doc = f"{exp['name']}: {exp['description']}"
            documents.append(doc)

            # Store metadata
            metadatas.append({
                "name": exp['name'],
                "category": exp['category'],
                "age_min": exp.get('age_min', 5),
                "age_max": exp.get('age_max', 12),
                "wow_factor": exp.get('wow_factor', 5),
                "safety_notes": exp.get('safety_notes', '')
            })

            # Generate ID
            ids.append(f"exp_{i}")

        # Add to collection
        self.experiments_collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

        print(f"✅ Added {len(experiments)} experiments")

    def add_qa_pairs(self, qa_pairs: List[Dict]):
        """
        Add Q&A pairs to the knowledge base

        Args:
            qa_pairs: List of Q&A dictionaries with:
                - question: The question
                - answer: The answer
                - topic: Science topic
                - difficulty: easy/medium/hard
        """
        if not qa_pairs:
            return

        print(f"💬 Adding {len(qa_pairs)} Q&A pairs...")

        documents = []
        metadatas = []
        ids = []

        for i, qa in enumerate(qa_pairs):
            # Create searchable document (question + answer)
            doc = f"Q: {qa['question']}\nA: {qa['answer']}"
            documents.append(doc)

            # Store metadata
            metadatas.append({
                "question": qa['question'],
                "answer": qa['answer'],
                "topic": qa.get('topic', 'general'),
                "difficulty": qa.get('difficulty', 'medium')
            })

            # Generate ID
            ids.append(f"qa_{i}")

        # Add to collection
        self.qa_collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

        print(f"✅ Added {len(qa_pairs)} Q&A pairs")

    def search(self,
               query: str,
               collection: str = "experiments",
               n_results: int = 3) -> Dict:
        """
        Search knowledge base for relevant content

        Args:
            query: Search query
            collection: "experiments" or "qa"
            n_results: Number of results to return

        Returns:
            Dictionary with documents, metadatas, distances
        """
        # Select collection
        coll = self.experiments_collection if collection == "experiments" else self.qa_collection

        # Search
        results = coll.query(
            query_texts=[query],
            n_results=n_results
        )

        return {
            "documents": results['documents'],
            "metadatas": results['metadatas'],
            "distances": results['distances']
        }

    def get_stats(self) -> Dict:
        """Get knowledge base statistics"""
        exp_count = self.experiments_collection.count()
        qa_count = self.qa_collection.count()

        return {
            "total_experiments": exp_count,
            "total_qa_pairs": qa_count,
            "total_passages": exp_count + qa_count,
            "collections": ["experiments", "qa"],
            "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
            "embedding_dimension": 384,
            "vector_db": "ChromaDB"
        }

    def clear_collection(self, collection: str):
        """Clear a collection (for testing/rebuilding)"""
        print(f"🗑️ Clearing {collection} collection...")
        self.client.delete_collection(name=collection)

        if collection == "experiments":
            self.experiments_collection = self._get_or_create_collection("experiments")
        else:
            self.qa_collection = self._get_or_create_collection("qa")

        print(f"✅ Cleared {collection}")
