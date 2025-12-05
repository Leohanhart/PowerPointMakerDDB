"""
Main entry point for the PowerPoint Maker application.
"""
import os
from dotenv import load_dotenv
from service.pdf_service import PDFService

# Load environment variables from .env file
load_dotenv()


def main():
    """Main function to run the application."""
    # Check if OpenAI API key is set
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file based on example.env and add your API key.")
        return
    
    print("PowerPoint Maker DDB - Starting application...")
    print("OpenAI API key loaded successfully.\n")
    
    # Initialize PDF service
    pdf_service = PDFService()
    
    # Process PDFs and create embeddings
    result = pdf_service.process_pdfs()
    
    if result["status"] == "success":
        print(f"\n✓ Successfully processed {result['processed_files']} file(s)")
        print(f"✓ Created {result['total_chunks']} chunks with embeddings")
    elif result["status"] == "no_files":
        print("\n⚠ No PDF files found. Please add PDF files to src/pdf/ folder.")


if __name__ == "__main__":
    main()

