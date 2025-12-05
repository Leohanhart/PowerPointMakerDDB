"""
Test script to test all functions and workflows.

This script tests:
1. PDFService - PDF processing and embedding creation
2. WorkflowService - Topic discovery, search, summarization, and PowerPoint generation
3. All workflow steps individually
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import services
from powerpoint_maker_ddb.service.pdf_service import PDFService
from powerpoint_maker_ddb.service.workflow_service import WorkflowService


def test_pdf_service():
    """Test PDFService functionality."""
    print("\n" + "=" * 60)
    print("TEST 1: PDF Service")
    print("=" * 60)
    
    try:
        # Initialize PDF service
        pdf_service = PDFService()
        print("✓ PDFService initialized")
        
        # Check if PDFs exist
        pdf_files = list(pdf_service.pdf_folder.glob("*.pdf"))
        print(f"✓ Found {len(pdf_files)} PDF file(s) in {pdf_service.pdf_folder}")
        
        if len(pdf_files) == 0:
            print("⚠ Warning: No PDF files found. Please add PDFs to src/pdf/ folder")
            return False
        
        # Process PDFs
        print("\nProcessing PDFs and creating embeddings...")
        result = pdf_service.process_pdfs()
        
        if result["status"] == "success":
            print(f"✓ Successfully processed {result['processed_files']} file(s)")
            print(f"✓ Created {result['total_chunks']} chunks with embeddings")
            return True
        else:
            print(f"⚠ Status: {result['status']}")
            return False
            
    except Exception as e:
        print(f"✗ Error in PDFService: {str(e)}")
        return False


def test_load_vectors():
    """Test loading vectors."""
    print("\n" + "=" * 60)
    print("TEST 2: Load Vectors")
    print("=" * 60)
    
    try:
        pdf_service = PDFService()
        vector_data = pdf_service.load_vectors()
        
        if len(vector_data["chunks"]) == 0:
            print("⚠ No vectors found. Run test_pdf_service() first.")
            return False
        
        print(f"✓ Loaded {len(vector_data['chunks'])} chunks")
        print(f"✓ Embeddings shape: {vector_data['embeddings'].shape}")
        print(f"✓ Metadata entries: {len(vector_data['metadata'])}")
        
        # Show sample chunk
        if len(vector_data["chunks"]) > 0:
            sample_chunk = vector_data["chunks"][0][:100] + "..."
            print(f"✓ Sample chunk: {sample_chunk}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error loading vectors: {str(e)}")
        return False


def test_vector_search():
    """Test vector search functionality."""
    print("\n" + "=" * 60)
    print("TEST 3: Vector Search")
    print("=" * 60)
    
    try:
        pdf_service = PDFService()
        vector_data = pdf_service.load_vectors()
        
        if len(vector_data["chunks"]) == 0:
            print("⚠ No vectors found. Run test_pdf_service() first.")
            return False
        
        # Test search
        test_query = "machine learning"
        print(f"Searching for: '{test_query}'")
        results = pdf_service.search_vectors(test_query, top_k=3, vector_data=vector_data)
        
        if len(results) == 0:
            print("⚠ No results found. Try a different query.")
            return False
        
        print(f"✓ Found {len(results)} results:")
        for i, result in enumerate(results, 1):
            print(f"  {i}. Similarity: {result['similarity']:.4f}")
            print(f"     Source: {result['metadata'].get('source_file', 'Unknown')}")
            chunk_preview = result['chunk'][:80] + "..." if len(result['chunk']) > 80 else result['chunk']
            print(f"     Preview: {chunk_preview}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error in vector search: {str(e)}")
        return False


def test_topic_discovery():
    """Test automatic topic discovery."""
    print("\n" + "=" * 60)
    print("TEST 4: Topic Discovery")
    print("=" * 60)
    
    try:
        workflow = WorkflowService()
        vector_data = workflow.load_embeddings()
        
        print("Discovering topics from PDF content...")
        topics = workflow.discover_topics(vector_data=vector_data, num_topics=5)
        
        if len(topics) == 0:
            print("⚠ No topics discovered.")
            return False
        
        print(f"✓ Discovered {len(topics)} topics:")
        for i, topic in enumerate(topics, 1):
            print(f"  {i}. {topic}")
        
        return topics
        
    except Exception as e:
        print(f"✗ Error in topic discovery: {str(e)}")
        return None


def test_topic_search():
    """Test searching for specific topics."""
    print("\n" + "=" * 60)
    print("TEST 5: Topic Search")
    print("=" * 60)
    
    try:
        workflow = WorkflowService()
        vector_data = workflow.load_embeddings()
        
        # Use discovered topics or test topics
        test_topics = ["data", "analysis", "method"]
        print(f"Searching for topics: {test_topics}")
        
        topic_results = workflow.search_topics(test_topics, top_k=3, vector_data=vector_data)
        
        for topic, results in topic_results.items():
            print(f"\n✓ Topic: '{topic}' - Found {len(results)} results")
            if len(results) > 0:
                print(f"  Top result similarity: {results[0]['similarity']:.4f}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error in topic search: {str(e)}")
        return False


def test_summarization():
    """Test information summarization."""
    print("\n" + "=" * 60)
    print("TEST 6: Information Summarization")
    print("=" * 60)
    
    try:
        workflow = WorkflowService()
        vector_data = workflow.load_embeddings()
        
        # Get some chunks for testing
        if len(vector_data["chunks"]) == 0:
            print("⚠ No chunks available for summarization.")
            return False
        
        # Search for a topic and get chunks
        test_topic = "data"
        print(f"Summarizing information about: '{test_topic}'")
        
        results = workflow.pdf_service.search_vectors(test_topic, top_k=3, vector_data=vector_data)
        chunks = [result["chunk"] for result in results]
        
        if len(chunks) == 0:
            print("⚠ No relevant chunks found.")
            return False
        
        print(f"Summarizing {len(chunks)} chunks...")
        summary = workflow.summarize_information(test_topic, chunks)
        
        print(f"✓ Summary created ({len(summary)} characters):")
        print(f"\n{summary}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error in summarization: {str(e)}")
        return False


def test_powerpoint_generation():
    """Test PowerPoint generation."""
    print("\n" + "=" * 60)
    print("TEST 7: PowerPoint Generation")
    print("=" * 60)
    
    try:
        workflow = WorkflowService()
        
        # Create test summaries
        test_summaries = {
            "Test Topic 1": "This is a test summary for topic 1. It contains some sample information to demonstrate the PowerPoint generation functionality.",
            "Test Topic 2": "This is a test summary for topic 2. It shows how multiple topics can be included in a single PowerPoint presentation.",
            "Test Topic 3": "This is a test summary for topic 3. The PowerPoint generator formats each topic with proper headings and spacing."
        }
        
        print("Generating test PowerPoint...")
        pptx_path = workflow.generate_powerpoint(test_summaries, output_filename="test_output.pptx")
        
        if pptx_path.exists():
            print(f"✓ PowerPoint generated successfully: {pptx_path}")
            print(f"✓ File size: {pptx_path.stat().st_size} bytes")
            return True
        else:
            print("✗ PowerPoint file was not created.")
            return False
            
    except Exception as e:
        print(f"✗ Error in PowerPoint generation: {str(e)}")
        return False


def test_full_workflow():
    """Test the complete workflow."""
    print("\n" + "=" * 60)
    print("TEST 8: Full Workflow (Auto-discover topics)")
    print("=" * 60)
    
    try:
        workflow = WorkflowService()
        
        print("Running complete workflow with automatic topic discovery...")
        result = workflow.run_workflow(
            topics=None,  # Auto-discover
            top_k=5,
            output_filename="full_workflow_test.pptx",
            num_topics=5
        )
        
        if result["status"] == "success":
            print(f"\n✓ Workflow completed successfully!")
            print(f"  Topics discovered: {result['topics']}")
            print(f"  PowerPoint saved to: {result['pptx_path']}")
            return True
        else:
            print(f"✗ Workflow failed with status: {result.get('status', 'unknown')}")
            return False
            
    except Exception as e:
        print(f"✗ Error in full workflow: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_custom_topics_workflow():
    """Test workflow with custom topics."""
    print("\n" + "=" * 60)
    print("TEST 9: Full Workflow (Custom topics)")
    print("=" * 60)
    
    try:
        workflow = WorkflowService()
        
        custom_topics = ["data", "analysis", "method", "result", "conclusion"]
        print(f"Running workflow with custom topics: {custom_topics}")
        
        result = workflow.run_workflow(
            topics=custom_topics,
            top_k=5,
            output_filename="custom_topics_test.pptx"
        )
        
        if result["status"] == "success":
            print(f"\n✓ Workflow completed successfully!")
            print(f"  Topics processed: {result['topics']}")
            print(f"  PowerPoint saved to: {result['pptx_path']}")
            return True
        else:
            print(f"✗ Workflow failed with status: {result.get('status', 'unknown')}")
            return False
            
    except Exception as e:
        print(f"✗ Error in custom topics workflow: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests in sequence."""
    print("\n" + "=" * 80)
    print("WORKFLOW TEST SUITE")
    print("=" * 80)
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("\n✗ ERROR: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file based on example.env and add your API key.")
        return
    
    results = {}
    
    # Test 1: PDF Service
    results["PDF Service"] = test_pdf_service()
    
    # Test 2: Load Vectors
    results["Load Vectors"] = test_load_vectors()
    
    # Test 3: Vector Search
    results["Vector Search"] = test_vector_search()
    
    # Test 4: Topic Discovery
    discovered_topics = test_topic_discovery()
    results["Topic Discovery"] = discovered_topics is not None
    
    # Test 5: Topic Search
    results["Topic Search"] = test_topic_search()
    
    # Test 6: Summarization
    results["Summarization"] = test_summarization()
    
    # Test 7: PowerPoint Generation
    results["PowerPoint Generation"] = test_powerpoint_generation()
    
    # Test 8: Full Workflow (Auto)
    results["Full Workflow (Auto)"] = test_full_workflow()
    
    # Test 9: Full Workflow (Custom)
    results["Full Workflow (Custom)"] = test_custom_topics_workflow()
    
    # Print summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("=" * 80)


def run_specific_test(test_number: int):
    """Run a specific test by number."""
    tests = {
        1: ("PDF Service", test_pdf_service),
        2: ("Load Vectors", test_load_vectors),
        3: ("Vector Search", test_vector_search),
        4: ("Topic Discovery", test_topic_discovery),
        5: ("Topic Search", test_topic_search),
        6: ("Summarization", test_summarization),
        7: ("PowerPoint Generation", test_powerpoint_generation),
        8: ("Full Workflow (Auto)", test_full_workflow),
        9: ("Full Workflow (Custom)", test_custom_topics_workflow),
    }
    
    if test_number not in tests:
        print(f"Invalid test number. Choose 1-9")
        return
    
    name, test_func = tests[test_number]
    print(f"\nRunning test {test_number}: {name}")
    test_func()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            test_num = int(sys.argv[1])
            run_specific_test(test_num)
        except ValueError:
            print("Usage: python test_workflow.py [test_number]")
            print("  test_number: 1-9 (optional, runs all tests if not specified)")
    else:
        run_all_tests()

