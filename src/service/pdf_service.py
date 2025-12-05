"""
Service for processing PDF files, chunking text, and creating embeddings.
"""
import os
import pickle
from pathlib import Path
from typing import List, Dict, Any
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class PDFService:
    """Service to process PDFs, chunk text, and store embeddings."""
    
    def __init__(self, pdf_folder: str = "src/pdf", vector_file: str = "src/service/vectors.pkl"):
        """
        Initialize the PDF service.
        
        Args:
            pdf_folder: Path to folder containing PDF files
            vector_file: Path to local vector storage file
        """
        self.pdf_folder = Path(pdf_folder)
        self.vector_file = Path(vector_file)
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Ensure folders exist
        self.pdf_folder.mkdir(parents=True, exist_ok=True)
        self.vector_file.parent.mkdir(parents=True, exist_ok=True)
    
    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """
        Extract text from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text as string
        """
        try:
            import PyPDF2
            
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except ImportError:
            raise ImportError("PyPDF2 is required. Install it with: pip install PyPDF2")
        except Exception as e:
            raise Exception(f"Error reading PDF {pdf_path}: {str(e)}")
    
    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """
        Split text into chunks with overlap.
        
        Args:
            text: Text to chunk
            chunk_size: Maximum size of each chunk in characters
            overlap: Number of characters to overlap between chunks
            
        Returns:
            List of text chunks
        """
        if not text:
            return []
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence boundary if possible
            if end < len(text):
                # Look for sentence endings near the end
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                break_point = max(last_period, last_newline)
                
                if break_point > chunk_size * 0.7:  # Only break if we're at least 70% through
                    chunk = chunk[:break_point + 1]
                    end = start + break_point + 1
            
            chunks.append(chunk.strip())
            start = end - overlap  # Overlap for context
        
        return chunks
    
    def create_embeddings(self, chunks: List[str]) -> List[List[float]]:
        """
        Create embeddings for text chunks using OpenAI.
        
        Args:
            chunks: List of text chunks to embed
            
        Returns:
            List of embedding vectors
        """
        if not chunks:
            return []
        
        try:
            response = self.client.embeddings.create(
                model="text-embedding-3-small",  # or "text-embedding-ada-002"
                input=chunks
            )
            
            embeddings = [item.embedding for item in response.data]
            return embeddings
        except Exception as e:
            raise Exception(f"Error creating embeddings: {str(e)}")
    
    def process_pdfs(self) -> Dict[str, Any]:
        """
        Process all PDFs in the pdf folder, chunk them, create embeddings,
        and replace the vector storage file.
        
        Returns:
            Dictionary with processing results
        """
        # Find all PDF files
        pdf_files = list(self.pdf_folder.glob("*.pdf"))
        
        if not pdf_files:
            print(f"No PDF files found in {self.pdf_folder}")
            return {
                "processed_files": 0,
                "total_chunks": 0,
                "status": "no_files"
            }
        
        all_chunks = []
        all_embeddings = []
        all_metadata = []
        
        print(f"Processing {len(pdf_files)} PDF file(s)...")
        
        for pdf_path in pdf_files:
            print(f"Processing: {pdf_path.name}")
            
            # Extract text
            text = self.extract_text_from_pdf(pdf_path)
            
            # Chunk text
            chunks = self.chunk_text(text)
            print(f"  Created {len(chunks)} chunks")
            
            # Create embeddings
            embeddings = self.create_embeddings(chunks)
            print(f"  Created {len(embeddings)} embeddings")
            
            # Store metadata for each chunk
            for i, chunk in enumerate(chunks):
                all_chunks.append(chunk)
                all_embeddings.append(embeddings[i])
                all_metadata.append({
                    "source_file": pdf_path.name,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                })
        
        # Replace vector storage file
        vector_data = {
            "chunks": all_chunks,
            "embeddings": np.array(all_embeddings),
            "metadata": all_metadata
        }
        
        with open(self.vector_file, 'wb') as f:
            pickle.dump(vector_data, f)
        
        print(f"\nVector storage updated: {self.vector_file}")
        print(f"Total chunks stored: {len(all_chunks)}")
        
        return {
            "processed_files": len(pdf_files),
            "total_chunks": len(all_chunks),
            "vector_file": str(self.vector_file),
            "status": "success"
        }
    
    def load_vectors(self) -> Dict[str, Any]:
        """
        Load vectors from storage file.
        
        Returns:
            Dictionary with chunks, embeddings, and metadata
        """
        if not self.vector_file.exists():
            return {
                "chunks": [],
                "embeddings": np.array([]),
                "metadata": []
            }
        
        with open(self.vector_file, 'rb') as f:
            return pickle.load(f)

