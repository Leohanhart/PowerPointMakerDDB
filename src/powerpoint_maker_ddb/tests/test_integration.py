"""
Integration tests for the complete workflow.
"""
import pytest
import os
from pathlib import Path
from dotenv import load_dotenv

from powerpoint_maker_ddb.service.pdf_service import PDFService
from powerpoint_maker_ddb.service.workflow_service import WorkflowService

load_dotenv()


@pytest.mark.integration
class TestIntegration:
    """Integration tests that require actual API calls."""
    
    @pytest.fixture
    def pdf_service(self):
        """Create a PDFService instance."""
        return PDFService()
    
    @pytest.fixture
    def workflow_service(self):
        """Create a WorkflowService instance."""
        return WorkflowService()
    
    @pytest.mark.skipif(
        not os.getenv("OPENAI_API_KEY"),
        reason="OPENAI_API_KEY not set"
    )
    def test_create_embeddings(self, pdf_service):
        """Test creating embeddings with OpenAI API."""
        test_chunks = ["This is a test chunk.", "Another test chunk."]
        embeddings = pdf_service.create_embeddings(test_chunks)
        
        assert len(embeddings) == 2
        assert all(isinstance(emb, list) for emb in embeddings)
        assert all(len(emb) > 0 for emb in embeddings)
    
    @pytest.mark.skipif(
        not os.getenv("OPENAI_API_KEY"),
        reason="OPENAI_API_KEY not set"
    )
    def test_search_vectors_with_embeddings(self, pdf_service):
        """Test vector search with actual embeddings."""
        # Create some test chunks and embeddings
        test_chunks = [
            "Machine learning is a subset of artificial intelligence.",
            "Data analysis involves examining data sets.",
            "Python is a programming language."
        ]
        
        embeddings = pdf_service.create_embeddings(test_chunks)
        
        vector_data = {
            "chunks": test_chunks,
            "embeddings": embeddings,
            "metadata": [{"source_file": "test.pdf", "chunk_index": i} for i in range(len(test_chunks))]
        }
        
        # Search for something related to machine learning
        results = pdf_service.search_vectors("artificial intelligence", top_k=2, vector_data=vector_data)
        
        assert len(results) > 0
        assert all("similarity" in result for result in results)
        assert all("chunk" in result for result in results)
        assert all("metadata" in result for result in results)
    
    @pytest.mark.skipif(
        not os.getenv("OPENAI_API_KEY"),
        reason="OPENAI_API_KEY not set"
    )
    def test_summarize_information(self, workflow_service):
        """Test information summarization with OpenAI API."""
        test_chunks = [
            "Machine learning algorithms can learn from data.",
            "Neural networks are a type of machine learning model.",
            "Deep learning uses multiple layers of neural networks."
        ]
        
        summary = workflow_service.summarize_information("machine learning", test_chunks)
        
        assert summary is not None
        assert len(summary) > 0
        assert isinstance(summary, str)
