"""
Main entry point for the PowerPoint Maker application.
"""
import os
from dotenv import load_dotenv
from powerpoint_maker_ddb.service.pdf_service import PDFService
from powerpoint_maker_ddb.service.workflow_service import WorkflowService

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
    
    print("=" * 80)
    print("PowerPoint Maker DDB - Starting application...")
    print("=" * 80)
    print("OpenAI API key loaded successfully.\n")
    
    # Step 1: Initialize PDF service and process PDFs
    print("Step 1: Processing PDFs and creating embeddings...")
    pdf_service = PDFService()
    result = pdf_service.process_pdfs()
    
    if result["status"] == "no_files":
        print("\n⚠ No PDF files found. Please add PDF files to src/pdf/ folder.")
        return
    
    if result["status"] == "success":
        print(f"\n✓ Successfully processed {result['processed_files']} file(s)")
        print(f"✓ Created {result['total_chunks']} chunks with embeddings\n")
    else:
        print("⚠ Error processing PDFs. Please check the error messages above.")
        return
    
    # Step 2: Run workflow to generate PowerPoint
    print("\n" + "=" * 80)
    print("Step 2: Running workflow to generate PowerPoint presentation...")
    print("=" * 80)
    
    try:
        # Initialize workflow service
        workflow = WorkflowService()
        
        # Run complete workflow: discover topics, summarize, and generate PowerPoint
        workflow_result = workflow.run_workflow(
            topics=None,  # Auto-discover topics from PDF content
            top_k=5,  # Number of top results per topic
            output_filename=None,  # Auto-generate filename with timestamp
            num_topics=5  # Number of topics to discover
        )
        
        if workflow_result["status"] == "success":
            print("\n" + "=" * 80)
            print("✓ APPLICATION COMPLETED SUCCESSFULLY!")
            print("=" * 80)
            print(f"  PowerPoint saved to: {workflow_result['pptx_path']}")
            print(f"  Topics discovered: {workflow_result['topics']}")
            print(f"  Topics processed: {workflow_result['topics_processed']}")
            print("=" * 80)
        else:
            print("\n⚠ Workflow completed with errors. Please check the messages above.")
            
    except Exception as e:
        print(f"\n✗ Error running workflow: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

