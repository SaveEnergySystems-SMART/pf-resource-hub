"""
Simple RAG Service for PF Resource Hub - NO DEPENDENCIES VERSION
Just loads and searches text files using basic Python
"""

import os
import re
from typing import List, Dict, Tuple

class SimpleRAGService:
    def __init__(self, docs_directory: str = None):
        """Initialize simple RAG service"""
        if docs_directory is None:
            docs_directory = os.path.join(os.path.dirname(__file__), 'knowledge_base')
        self.docs_directory = docs_directory
        self.documents = []
        self.document_names = []
        
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
                        self.documents.append({
                            'text': chunk,
                            'source': filename,
                            'chunk_id': i
                        })
                    
                    print(f"  ✅ Loaded: {filename} ({len(chunks)} chunks)")
                
                except Exception as e:
                    print(f"  ❌ Error loading {filename}: {str(e)}")
        
        print(f"\n✅ Loaded {len(self.documents)} document chunks from {len(set([d['source'] for d in self.documents]))} files")
    
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
    
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Search documents using simple keyword matching
        """
        if not self.documents:
            print("❌ No documents loaded")
            return []
        
        try:
            # Convert query to lowercase and extract keywords
            query_lower = query.lower()
            query_words = set(re.findall(r'\w+', query_lower))
            
            # Score each document
            scored_docs = []
            for doc in self.documents:
                text_lower = doc['text'].lower()
                
                # Count matching words
                score = sum(1 for word in query_words if word in text_lower)
                
                if score > 0:
                    scored_docs.append({
                        'source': doc['source'],
                        'text': doc['text'],
                        'score': score
                    })
            
            # Sort by score and return top_k
            scored_docs.sort(key=lambda x: x['score'], reverse=True)
            return scored_docs[:top_k]
        
        except Exception as e:
            print(f"❌ Search error: {str(e)}")
            return []
    
    def get_context_for_query(self, query: str, top_k: int = 3) -> Tuple[str, List[str]]:
        """
        Get relevant context and sources for a query
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
