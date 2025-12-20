"""
Simple RAG Service for PF Resource Hub
Uses local TF-IDF search instead of embeddings (no API quota limits)
"""

import os
import re
from typing import List, Dict, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class SimpleRAGService:
    def __init__(self, docs_directory: str = None):
        """Initialize simple RAG service"""
        if docs_directory is None:
            # Default to knowledge_base folder in backend
            docs_directory = os.path.join(os.path.dirname(__file__), 'knowledge_base')
        self.docs_directory = docs_directory
        self.documents = []
        self.document_names = []
        self.vectorizer = None
        self.tfidf_matrix = None
        
        # Load documents
        self._load_documents()
    
    def _load_documents(self):
        """Load all .txt documents"""
        if not os.path.exists(self.docs_directory):
            print(f"⚠️  Directory not found: {self.docs_directory}")
            return
        
        print(f"📂 Loading documents from: {self.docs_directory}")
        
        for filename in os.listdir(self.docs_directory):
            if filename.endswith('.txt') and filename != 'requirements.txt':
                filepath = os.path.join(self.docs_directory, filename)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Split into chunks
                    chunks = self._split_into_chunks(content, chunk_size=1000, overlap=200)
                    
                    for i, chunk in enumerate(chunks):
                        self.documents.append(chunk)
                        self.document_names.append(f"{filename} (chunk {i+1})")
                    
                    print(f"  ✅ Loaded: {filename} ({len(chunks)} chunks)")
                
                except Exception as e:
                    print(f"  ❌ Error loading {filename}: {str(e)}")
        
        print(f"\n✅ Loaded {len(self.documents)} document chunks from {len(set(self.document_names))} files")
        
        # Create TF-IDF vectors
        if self.documents:
            self._create_index()
    
    def _split_into_chunks(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks"""
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += chunk_size - overlap
        
        return chunks
    
    def _create_index(self):
        """Create TF-IDF index"""
        print("\n🔍 Creating search index...")
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(self.documents)
        print("✅ Search index created")
    
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Search documents for relevant context
        
        Args:
            query: User's question
            top_k: Number of relevant chunks to return
        
        Returns:
            List of relevant document chunks with scores
        """
        if not self.documents or self.vectorizer is None:
            print("❌ No documents loaded")
            return []
        
        try:
            # Transform query
            query_vector = self.vectorizer.transform([query])
            
            # Calculate similarity
            similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
            
            # Get top k results
            top_indices = similarities.argsort()[-top_k:][::-1]
            
            results = []
            for idx in top_indices:
                if similarities[idx] > 0:  # Only include relevant results
                    # Extract source filename (remove chunk info)
                    source = self.document_names[idx].split(' (chunk ')[0]
                    
                    results.append({
                        'source': source,
                        'text': self.documents[idx],
                        'score': float(similarities[idx])
                    })
            
            return results
        
        except Exception as e:
            print(f"❌ Search error: {str(e)}")
            return []
    
    def get_context_for_query(self, query: str, top_k: int = 3) -> Tuple[str, List[str]]:
        """
        Get relevant context and sources for a query
        
        Returns:
            (context_text, list_of_sources)
        """
        results = self.search(query, top_k=top_k)
        
        if not results:
            return "", []
        
        # Combine relevant texts
        context_parts = []
        sources = []
        
        for result in results:
            context_parts.append(result['text'])
            if result['source'] not in sources:
                sources.append(result['source'])
        
        context_text = "\n\n---\n\n".join(context_parts)
        
        return context_text, sources


# Module-level instance
_rag_service = None

def init_rag():
    """Initialize RAG service"""
    global _rag_service
    if _rag_service is None:
        _rag_service = SimpleRAGService()
    return _rag_service

def search_docs(query: str, top_k: int = 3) -> Tuple[str, List[str]]:
    """
    Search documents and return context + sources
    
    Returns:
        (context_text, list_of_sources)
    """
    service = init_rag()
    return service.get_context_for_query(query, top_k=top_k)


# Test the service
if __name__ == "__main__":
    print("\n🧪 Testing Simple RAG Service...")
    
    # Initialize
    init_rag()
    
    # Test search
    query = "How do I reset a breaker?"
    print(f"\n💬 Query: {query}")
    
    context, sources = search_docs(query)
    
    print(f"\n📄 Sources: {', '.join(sources)}")
    print(f"\n📝 Context (first 500 chars):\n{context[:500]}...")
    
    print("\n✅ RAG service test complete!")
