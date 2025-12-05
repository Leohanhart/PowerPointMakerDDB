"""
Example script demonstrating how to use the WorkflowService.

This script shows how to:
1. Load embeddings
2. Automatically discover topics from PDF content
3. Search topics from vectors
4. Get and summarize information per topic
5. Generate a PDF with summaries
"""
import os
from dotenv import load_dotenv
from powerpoint_maker_ddb.service.workflow_service import WorkflowService

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
    
    # Run the complete workflow with automatic topic discovery
    # This will:
    # 1. Load embeddings
    # 2. Automatically discover topics from the PDF content
    # 3. Search for each discovered topic in the vector database
    # 4. Summarize information for each topic
    # 5. Generate a PDF with all summaries
    result = workflow.run_workflow(
        topics=None,  # None = auto-discover topics from PDF content
        top_k=5,  # Number of top results to retrieve per topic
        output_filename=None,  # Will auto-generate filename with timestamp
        num_topics=5  # Number of topics to discover
    )
    
    print(f"\n✓ Workflow completed!")
    print(f"  PDF saved to: {result['pdf_path']}")
    print(f"  Topics discovered: {result['topics']}")
    print(f"  Topics processed: {result['topics_processed']}")
    
    # Alternative: You can also provide your own topics
    # result = workflow.run_workflow(
    #     topics=["machine learning", "data analysis", "artificial intelligence"],
    #     top_k=5,
    #     output_filename=None
    # )


if __name__ == "__main__":
    main()

