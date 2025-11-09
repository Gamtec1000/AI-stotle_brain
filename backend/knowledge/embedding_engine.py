# backend/knowledge/embedding_engine.py
"""
Free local embeddings using sentence-transformers
No API costs!
"""

from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import json
import os
from pathlib import Path
from typing import List, Dict
import numpy as np

class LocalEmbeddingEngine:
    """
    FREE embedding engine using local models
    """

    def __init__(self):
        """Initialize with free local model"""

        print("🔧 Loading local embedding model...")

        # Use best free model
        self.model = SentenceTransformer('all-mpnet-base-v2')

        print("✅ Model loaded!")

        # Initialize ChromaDB (local, free)
        db_path = os.getenv("CHROMA_DB_PATH", "../data/embeddings/chroma")
        os.makedirs(db_path, exist_ok=True)

        self.chroma_client = chromadb.PersistentClient(path=db_path)

        # Create collections
        self.experiments = self.chroma_client.get_or_create_collection(
            name="experiments",
            metadata={"description": "Carls Newton experiments"}
        )

        self.qa_pairs = self.chroma_client.get_or_create_collection(
            name="qa_pairs",
            metadata={"description": "Common questions and answers"}
        )

        self.concepts = self.chroma_client.get_or_create_collection(
            name="concepts",
            metadata={"description": "Science concepts"}
        )

    def create_embedding(self, text: str) -> List[float]:
        """
        Create embedding (FREE - runs locally)

        Args:
            text: Text to embed

        Returns:
            Embedding vector
        """
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()

    def embed_experiments(self, experiments_file: str):
        """
        Embed all experiments from JSON file
        """
        print(f"\n📚 Embedding experiments from {experiments_file}...")

        with open(experiments_file, 'r') as f:
            experiments = json.load(f)

        for exp in experiments:
            # Create rich text
            text = f"""
            Experiment: {exp['name']}
            Category: {exp['category']}

            Description:
            {exp['description']}

            Science Concepts:
            {', '.join(exp['science_concepts'])}

            Age Groups: {exp['age_min']}-{exp['age_max']} years

            Materials: {', '.join(exp['materials'])}

            Safety Notes: {' '.join(exp['safety_notes'])}

            Wow Factor: {exp['wow_factor']}/10
            """

            # Create embedding (FREE!)
            embedding = self.create_embedding(text)

            # Store in ChromaDB
            self.experiments.add(
                ids=[exp['id']],
                embeddings=[embedding],
                documents=[text],
                metadatas=[{
                    'name': exp['name'],
                    'category': exp['category'],
                    'age_min': exp['age_min'],
                    'age_max': exp['age_max'],
                    'wow_factor': exp['wow_factor']
                }]
            )

            print(f"   ✅ {exp['name']}")

        print(f"\n✅ Embedded {len(experiments)} experiments (Cost: $0)")

    def embed_qa_pairs(self, experiments_file: str):
        """Embed Q&A pairs"""

        print(f"\n💬 Embedding Q&A pairs...")

        with open(experiments_file, 'r') as f:
            experiments = json.load(f)

        qa_count = 0

        for exp in experiments:
            for qa in exp.get('common_questions', []):
                text = f"""
                Question: {qa['question']}
                Answer: {qa['answer']}
                Related to: {exp['name']} ({exp['category']})
                """

                embedding = self.create_embedding(text)

                self.qa_pairs.add(
                    ids=[f"{exp['id']}_qa_{qa_count}"],
                    embeddings=[embedding],
                    documents=[text],
                    metadatas=[{
                        'question': qa['question'],
                        'experiment': exp['name'],
                        'experiment_id': exp['id']
                    }]
                )

                qa_count += 1

        print(f"✅ Embedded {qa_count} Q&A pairs (Cost: $0)")

    def search(self,
              query: str,
              collection: str = "experiments",
              n_results: int = 3) -> Dict:
        """
        Search knowledge base (FREE!)

        Args:
            query: Search query
            collection: Which collection to search
            n_results: Number of results

        Returns:
            Search results
        """
        # Create query embedding (FREE!)
        query_embedding = self.create_embedding(query)

        # Search
        if collection == "experiments":
            results = self.experiments.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
        elif collection == "qa" or collection == "qa_pairs":
            results = self.qa_pairs.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
        else:
            results = self.concepts.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )

        return results

    def get_stats(self):
        """Get database statistics"""

        exp_count = self.experiments.count()
        qa_count = self.qa_pairs.count()
        concepts_count = self.concepts.count()

        return {
            "total_experiments": exp_count,
            "total_qa_pairs": qa_count,
            "total_concepts": concepts_count,
            "total_passages": exp_count + qa_count + concepts_count,
            "collections": ["experiments", "qa_pairs", "concepts"],
            "embedding_model": "all-mpnet-base-v2",
            "embedding_dimension": 768,
            "vector_db": "ChromaDB",
            "total_cost": "$0 (all local!)"
        }


# Test
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🆓 FREE LOCAL EMBEDDINGS ENGINE")
    print("="*60)

    engine = LocalEmbeddingEngine()

    # Test search
    print("\n🔍 Testing search...")

    results = engine.search("foam explosion chemistry")

    print(f"Found {len(results['documents'][0])} results")
    print(f"Top result: {results['metadatas'][0][0].get('name', 'N/A')}")

    print("\n📊 Database stats:")
    stats = engine.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")

    print("\n💰 Total embedding cost: $0")
    print("="*60)
