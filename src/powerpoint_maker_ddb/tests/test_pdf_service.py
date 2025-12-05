"""
Tests for PDFService.
"""
import pytest
import os
from pathlib import Path
from dotenv import load_dotenv

from powerpoint_maker_ddb.service.pdf_service import PDFService

load_dotenv()


class TestPDFService:
    """Test cases for PDFService."""
    
    @pytest.fixture
    def pdf_service(self):
        """Create a PDFService instance for testing."""
        return PDFService()
    
    def test_initialization(self, pdf_service):
        """Test PDFService initialization."""
        assert pdf_service is not None
        assert pdf_service.pdf_folder is not None
        assert pdf_service.vector_file is not None
    
    def test_chunk_text(self, pdf_service):
        """Test text chunking functionality."""
        text = "This is a test. " * 100  # Create a long text
        chunks = pdf_service.chunk_text(text, chunk_size=50, overlap=10)
        
        assert len(chunks) > 0
        assert all(isinstance(chunk, str) for chunk in chunks)
    
    def test_chunk_text_empty(self, pdf_service):
        """Test chunking empty text."""
        chunks = pdf_service.chunk_text("")
        assert chunks == []
    
    def test_load_vectors_empty(self, pdf_service):
        """Test loading vectors when file doesn't exist."""
        # Use a non-existent file path
        pdf_service.vector_file = Path("non_existent_vectors.pkl")
        vector_data = pdf_service.load_vectors()
        
        assert vector_data["chunks"] == []
        assert len(vector_data["embeddings"]) == 0
        assert vector_data["metadata"] == []
    
    def test_search_vectors_empty(self, pdf_service):
        """Test searching with empty vectors."""
        empty_vector_data = {
            "chunks": [],
            "embeddings": [],
            "metadata": []
        }
        results = pdf_service.search_vectors("test query", vector_data=empty_vector_data)
        assert results == []

