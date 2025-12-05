"""
Example script demonstrating how to use the WorkflowService.

This script shows how to:
1. Load embeddings
2. Search topics from vectors
3. Get and summarize information per topic
4. Generate a PDF with summaries
"""
import os
from dotenv import load_dotenv
from service.workflow_service import WorkflowService

# Load environment variables
load_dotenv()


def main():
    """Example usage of the WorkflowService."""
    # Check if OpenAI API key is set
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file based on example.env and add your API key.")
        return
    
    # Initialize the workflow service
    workflow = WorkflowService()
    
    # Define topics to search for
    topics = [
        "machine learning",
        "data analysis",
        "artificial intelligence"
    ]
    
    # Run the complete workflow
    # This will:
    # 1. Load embeddings
    # 2. Search for each topic in the vector database
    # 3. Summarize information for each topic
    # 4. Generate a PDF with all summaries
    result = workflow.run_workflow(
        topics=topics,
        top_k=5,  # Number of top results to retrieve per topic
        output_filename=None  # Will auto-generate filename with timestamp
    )
    
    print(f"\n✓ Workflow completed!")
    print(f"  PDF saved to: {result['pdf_path']}")
    print(f"  Topics processed: {result['topics_processed']}")


if __name__ == "__main__":
    main()

