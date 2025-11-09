# backend/knowledge/faiss_knowledge.py
"""
AI-stotle Knowledge Base using FAISS
Free, fast, and local vector search for scientific knowledge
"""

import faiss
import numpy as np
import pickle
import os
from typing import List, Dict, Tuple
from sentence_transformers import SentenceTransformer
from pathlib import Path

class AristotleKnowledge:
    """
    Knowledge base for AI-stotle using FAISS vector search
    Stores and retrieves scientific knowledge for Carls Newton shows
    """
    
    def __init__(self, index_path: str = None, embedding_model: str = None):
        """
        Initialize knowledge base
        
        Args:
            index_path: Path to save/load FAISS index
            embedding_model: Sentence transformer model name
        """
        self.index_path = index_path or os.getenv(
            "FAISS_INDEX_PATH", 
            "../data/embeddings/faiss_index"
        )
        
        model_name = embedding_model or os.getenv(
            "EMBEDDING_MODEL",
            "sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Load embedding model (384 dimensions, fast and efficient)
        print(f"📚 Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.dimension = 384  # all-MiniLM-L6-v2 dimension
        
        # Initialize FAISS index
        self.index = None
        self.documents = []
        self.metadata = []
        
        # Try to load existing index
        self._load_index()
    
    def add_knowledge(self, 
                     texts: List[str], 
                     metadata: List[Dict] = None):
        """
        Add knowledge to the database
        
        Args:
            texts: List of text passages to add
            metadata: Optional metadata for each passage (experiment name, topic, etc.)
        """
        if not texts:
            return
        
        print(f"🔄 Adding {len(texts)} passages to knowledge base...")
        
        # Generate embeddings
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        
        # Create or expand index
        if self.index is None:
            self.index = faiss.IndexFlatL2(self.dimension)
        
        # Add to FAISS
        self.index.add(embeddings.astype('float32'))
        
        # Store documents and metadata
        self.documents.extend(texts)
        if metadata:
            self.metadata.extend(metadata)
        else:
            self.metadata.extend([{}] * len(texts))
        
        print(f"✅ Knowledge base now contains {self.index.ntotal} passages")
    
    def search(self, 
               query: str, 
               top_k: int = 3,
               filter_topic: str = None) -> List[Dict]:
        """
        Search knowledge base for relevant passages
        
        Args:
            query: Question or search query
            top_k: Number of results to return
            filter_topic: Optional topic filter
            
        Returns:
            List of relevant passages with scores
        """
        if self.index is None or self.index.ntotal == 0:
            return []
        
        # Encode query
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        
        # Search FAISS
        distances, indices = self.index.search(
            query_embedding.astype('float32'), 
            min(top_k * 2, self.index.ntotal)  # Get extra results for filtering
        )
        
        # Format results
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.documents):
                doc_metadata = self.metadata[idx]
                
                # Apply topic filter if specified
                if filter_topic and doc_metadata.get('topic') != filter_topic:
                    continue
                
                results.append({
                    'text': self.documents[idx],
                    'score': float(dist),
                    'metadata': doc_metadata
                })
                
                if len(results) >= top_k:
                    break
        
        return results
    
    def save_index(self):
        """Save FAISS index and documents to disk"""
        if self.index is None:
            print("⚠️ No index to save")
            return
        
        # Create directory if needed
        Path(self.index_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Save FAISS index
        faiss.write_index(self.index, f"{self.index_path}.index")
        
        # Save documents and metadata
        with open(f"{self.index_path}.pkl", 'wb') as f:
            pickle.dump({
                'documents': self.documents,
                'metadata': self.metadata
            }, f)
        
        print(f"💾 Saved knowledge base to {self.index_path}")
    
    def _load_index(self):
        """Load existing FAISS index from disk"""
        index_file = f"{self.index_path}.index"
        pkl_file = f"{self.index_path}.pkl"
        
        if os.path.exists(index_file) and os.path.exists(pkl_file):
            try:
                # Load FAISS index
                self.index = faiss.read_index(index_file)
                
                # Load documents and metadata
                with open(pkl_file, 'rb') as f:
                    data = pickle.load(f)
                    self.documents = data['documents']
                    self.metadata = data['metadata']
                
                print(f"📖 Loaded knowledge base with {self.index.ntotal} passages")
            except Exception as e:
                print(f"⚠️ Error loading index: {e}")
                print("Creating new index...")
    
    def get_stats(self) -> Dict:
        """Get knowledge base statistics"""
        if self.index is None:
            return {
                'total_passages': 0,
                'topics': []
            }
        
        topics = set(m.get('topic', 'unknown') for m in self.metadata)
        
        return {
            'total_passages': self.index.ntotal,
            'topics': sorted(list(topics)),
            'embedding_dimension': self.dimension,
            'model': self.model
        }


# Sample knowledge for Carls Newton shows
SAMPLE_KNOWLEDGE = [
    {
        'text': """Elephant toothpaste is a dramatic chemical reaction that produces massive amounts of foam. 
        When hydrogen peroxide decomposes with the help of a catalyst (like yeast or potassium iodide), 
        it rapidly breaks down into water and oxygen gas. The soap traps the oxygen bubbles, creating 
        thick foam that shoots up like toothpaste for an elephant! The reaction is exothermic, 
        meaning it releases heat energy.""",
        'metadata': {
            'topic': 'chemistry',
            'experiment': 'elephant_toothpaste',
            'difficulty': 'medium',
            'age_range': '8-14'
        }
    },
    {
        'text': """A catalyst is a special substance that speeds up a chemical reaction without being 
        used up itself. Think of it like a helpful friend who makes things happen faster but doesn't 
        get tired! In elephant toothpaste, yeast acts as a catalyst to break down hydrogen peroxide 
        much faster than it would naturally. The catalyst provides an easier pathway for the reaction.""",
        'metadata': {
            'topic': 'chemistry',
            'experiment': 'elephant_toothpaste',
            'difficulty': 'easy',
            'age_range': '7-12'
        }
    },
    {
        'text': """Chemical reactions happen when atoms and molecules rearrange themselves to form 
        new substances. The starting materials are called reactants, and what you end up with are 
        called products. During a reaction, chemical bonds break and new ones form. Some reactions 
        release energy (exothermic) while others absorb energy (endothermic). Signs of a chemical 
        reaction include color changes, temperature changes, gas production, or precipitate formation.""",
        'metadata': {
            'topic': 'chemistry',
            'experiment': 'general',
            'difficulty': 'medium',
            'age_range': '10-14'
        }
    },
    {
        'text': """Dry ice is frozen carbon dioxide at -78.5°C (-109°F). When it warms up, it sublimates - 
        meaning it goes directly from solid to gas without becoming liquid! This creates spooky fog effects. 
        The 'fog' you see is actually tiny water droplets condensed from the air by the cold CO2 gas. 
        Dry ice is heavier than air, so the fog sinks down, making it perfect for Halloween effects 
        and science demonstrations.""",
        'metadata': {
            'topic': 'physics',
            'experiment': 'dry_ice',
            'difficulty': 'medium',
            'age_range': '8-14'
        }
    },
    {
        'text': """Static electricity occurs when electric charges build up on the surface of objects. 
        When you rub a balloon on your hair, electrons transfer from your hair to the balloon. 
        The balloon becomes negatively charged and your hair becomes positively charged. Opposite 
        charges attract, so your hair stands up toward the balloon! Lightning is a dramatic example 
        of static electricity in nature.""",
        'metadata': {
            'topic': 'physics',
            'experiment': 'static_electricity',
            'difficulty': 'easy',
            'age_range': '6-12'
        }
    },
    {
        'text': """Slime is a non-Newtonian fluid, meaning it doesn't follow normal liquid rules. 
        When you mix glue (polyvinyl alcohol) with borax or contact lens solution (containing borate ions), 
        the molecules form long, flexible chains called polymers. These chains slide past each other 
        when you move slowly, but tangle up when you move fast. That's why slime can flow like liquid 
        but also bounce like a solid!""",
        'metadata': {
            'topic': 'chemistry',
            'experiment': 'slime',
            'difficulty': 'easy',
            'age_range': '6-12'
        }
    },
    {
        'text': """Becoming a scientist means asking questions about the world and finding answers through 
        experiments. Scientists observe, wonder, test ideas, and learn from mistakes. You don't need 
        fancy equipment - curiosity and careful observation are your best tools! Every great scientist 
        started as a curious kid who loved to explore. The scientific method is: Question, Hypothesis, 
        Experiment, Analyze, Conclude. Remember: failure is just learning what doesn't work!""",
        'metadata': {
            'topic': 'general',
            'experiment': 'inspiration',
            'difficulty': 'easy',
            'age_range': '6-14'
        }
    }
]


# Test script
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🏛️ AI-STOTLE KNOWLEDGE BASE TEST")
    print("="*60)
    
    # Initialize knowledge base
    kb = AristotleKnowledge()
    
    # Add sample knowledge
    print("\n📚 Adding sample knowledge...")
    texts = [item['text'] for item in SAMPLE_KNOWLEDGE]
    metadata = [item['metadata'] for item in SAMPLE_KNOWLEDGE]
    kb.add_knowledge(texts, metadata)
    
    # Save to disk
    kb.save_index()
    
    # Test queries
    test_queries = [
        "Why does elephant toothpaste foam so much?",
        "What is a catalyst?",
        "How does dry ice create fog?",
        "Can kids be scientists?",
        "What makes slime stretchy?"
    ]
    
    print("\n" + "="*60)
    print("🔍 TESTING SEMANTIC SEARCH")
    print("="*60)
    
    for query in test_queries:
        print(f"\n❓ Query: {query}")
        print("-" * 60)
        
        results = kb.search(query, top_k=2)
        
        for i, result in enumerate(results, 1):
            print(f"\n{i}. [Score: {result['score']:.3f}] {result['metadata'].get('topic', 'general')}")
            print(f"   {result['text'][:200]}...")
    
    # Show stats
    print("\n" + "="*60)
    stats = kb.get_stats()
    print(f"📊 Knowledge Base Stats:")
    print(f"   Total passages: {stats['total_passages']}")
    print(f"   Topics: {', '.join(stats['topics'])}")
    print(f"   Embedding dimension: {stats['embedding_dimension']}")
    print("="*60)