import chromadb
from chromadb.utils import embedding_functions
import os
import json

class ARPVectorStore:
    def __init__(self):
        self.db_path = "chroma_db"
        # We use a standard sentence-transformer embedding function
        # This works locally without an API key
        self.emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        
        self.client = chromadb.PersistentClient(path=self.db_path)
        self.collection = self.client.get_or_create_collection(
            name="arp_insights",
            embedding_function=self.emb_fn
        )

    def add_insight(self, product_id, raw_text, analysis_json):
        """
        Add a processed insight to the vector database.
        """
        # Combine analysis results into a single string for embedding
        document_text = f"Product: {analysis_json.get('product_name')}\n"
        document_text += f"Analysis: {analysis_json.get('analysis')}\n"
        document_text += f"Key Insight: {analysis_json.get('key_insight')}"
        
        metadata = {
            "product_id": product_id,
            "symbol": analysis_json.get("symbol", "IREN"),
            "value_score": analysis_json.get("value_score", 0.0),
            "price": analysis_json.get("extracted_price", "N/A"),
            "timestamp": analysis_json.get("timestamp", "")
        }

        self.collection.add(
            documents=[document_text],
            metadatas=[metadata],
            ids=[product_id]
        )
        print(f"📦 [VectorStore] Indexed insight for {product_id}")

    def query(self, query_text, n_results=3):
        """
        Semantic search for relevant insights.
        """
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results
