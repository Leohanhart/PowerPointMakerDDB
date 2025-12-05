"""
Tests for WorkflowService.
"""
import pytest
import os
from pathlib import Path
from dotenv import load_dotenv

from powerpoint_maker_ddb.service.workflow_service import WorkflowService
from powerpoint_maker_ddb.service.pdf_service import PDFService

load_dotenv()


class TestWorkflowService:
    """Test cases for WorkflowService."""
    
    @pytest.fixture
    def workflow_service(self):
        """Create a WorkflowService instance for testing."""
        return WorkflowService()
    
    @pytest.fixture
    def pdf_service(self):
        """Create a PDFService instance for testing."""
        return PDFService()
    
    def test_initialization(self, workflow_service):
        """Test WorkflowService initialization."""
        assert workflow_service is not None
        assert workflow_service.pdf_service is not None
        assert workflow_service.output_folder is not None
    
    def test_summarize_information_empty_chunks(self, workflow_service):
        """Test summarization with empty chunks."""
        summary = workflow_service.summarize_information("test topic", [])
        assert "No relevant information" in summary
    
    def test_generate_powerpoint(self, workflow_service, tmp_path):
        """Test PowerPoint generation."""
        # Set output folder to temporary directory
        workflow_service.output_folder = tmp_path
        
        test_summaries = {
            "Topic 1": "This is a test summary for topic 1.",
            "Topic 2": "This is a test summary for topic 2."
        }
        
        pptx_path = workflow_service.generate_powerpoint(test_summaries, output_filename="test.pptx")
        
        assert pptx_path.exists()
        assert pptx_path.suffix == ".pptx"
        assert pptx_path.stat().st_size > 0
    
    def test_generate_powerpoint_auto_filename(self, workflow_service, tmp_path):
        """Test PowerPoint generation with auto-generated filename."""
        workflow_service.output_folder = tmp_path
        
        test_summaries = {
            "Topic 1": "Test summary"
        }
        
        pptx_path = workflow_service.generate_powerpoint(test_summaries)
        
        assert pptx_path.exists()
        assert pptx_path.name.startswith("topic_summaries_")
        assert pptx_path.suffix == ".pptx"
