"""
Workflow service that loads embeddings, searches topics, and generates PDF summaries.
"""
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

from service.pdf_service import PDFService

# Load environment variables
load_dotenv()


class WorkflowService:
    """Service to orchestrate embedding search and PDF generation workflow."""
    
    def __init__(self, vector_file: str = "src/service/vectors.pkl", output_folder: str = "src/pdf"):
        """
        Initialize the workflow service.
        
        Args:
            vector_file: Path to vector storage file
            output_folder: Folder to save output PDFs
        """
        self.pdf_service = PDFService(vector_file=vector_file)
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(parents=True, exist_ok=True)
    
    def load_embeddings(self) -> Dict[str, Any]:
        """
        Load embeddings from storage.
        
        Returns:
            Dictionary with chunks, embeddings, and metadata
        """
        print("Loading embeddings...")
        vector_data = self.pdf_service.load_vectors()
        
        if len(vector_data["chunks"]) == 0:
            raise ValueError("No embeddings found. Please process PDFs first using PDFService.process_pdfs()")
        
        print(f"✓ Loaded {len(vector_data['chunks'])} chunks with embeddings")
        return vector_data
    
    def search_topics(self, topics: List[str], top_k: int = 5, vector_data: Optional[Dict[str, Any]] = None) -> Dict[str, List[Dict[str, Any]]]:
        """
        Search for each topic in the vector database.
        
        Args:
            topics: List of topic strings to search for
            top_k: Number of top results per topic
            vector_data: Optional pre-loaded vector data
            
        Returns:
            Dictionary mapping each topic to its search results
        """
        if vector_data is None:
            vector_data = self.load_embeddings()
        
        print(f"\nSearching for {len(topics)} topic(s)...")
        topic_results = {}
        
        for topic in topics:
            print(f"  Searching: '{topic}'")
            results = self.pdf_service.search_vectors(topic, top_k=top_k, vector_data=vector_data)
            topic_results[topic] = results
            print(f"    Found {len(results)} relevant chunks")
        
        return topic_results
    
    def summarize_information(self, topic: str, chunks: List[str], max_length: int = 500) -> str:
        """
        Summarize information from relevant chunks for a topic.
        
        Args:
            topic: The topic being summarized
            chunks: List of relevant text chunks
            max_length: Maximum length of summary in characters
            
        Returns:
            Summarized text
        """
        if not chunks:
            return f"No relevant information found for topic: {topic}"
        
        # Combine chunks with context
        combined_text = "\n\n".join([f"[Chunk {i+1}]\n{chunk}" for i, chunk in enumerate(chunks)])
        
        # Create prompt for summarization
        prompt = f"""Please provide a concise summary of the following information related to the topic: "{topic}"

Information:
{combined_text}

Please summarize the key points about "{topic}" in a clear and structured way. Keep the summary under {max_length} characters."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes information clearly and concisely."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            summary = response.choices[0].message.content.strip()
            return summary
        except Exception as e:
            raise Exception(f"Error summarizing information: {str(e)}")
    
    def generate_pdf(self, topic_summaries: Dict[str, str], output_filename: Optional[str] = None) -> Path:
        """
        Generate a PDF with summarized information for each topic.
        
        Args:
            topic_summaries: Dictionary mapping topics to their summaries
            output_filename: Optional custom output filename
            
        Returns:
            Path to the generated PDF file
        """
        try:
            from reportlab.lib.pagesizes import letter, A4
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
            from reportlab.lib.enums import TA_LEFT, TA_CENTER
        except ImportError:
            raise ImportError("reportlab is required. Install it with: pip install reportlab")
        
        # Generate output filename
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"topic_summaries_{timestamp}.pdf"
        
        if not output_filename.endswith('.pdf'):
            output_filename += '.pdf'
        
        output_path = self.output_folder / output_filename
        
        # Create PDF document
        doc = SimpleDocTemplate(str(output_path), pagesize=A4)
        story = []
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor='#1a1a1a',
            spaceAfter=30,
            alignment=TA_CENTER
        )
        topic_style = ParagraphStyle(
            'CustomTopic',
            parent=styles['Heading2'],
            fontSize=18,
            textColor='#2c3e50',
            spaceAfter=12,
            spaceBefore=20
        )
        summary_style = ParagraphStyle(
            'CustomSummary',
            parent=styles['Normal'],
            fontSize=11,
            textColor='#34495e',
            spaceAfter=12,
            leading=16,
            alignment=TA_LEFT
        )
        
        # Add title
        story.append(Paragraph("Topic Summaries Report", title_style))
        story.append(Spacer(1, 0.3*inch))
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        story.append(Spacer(1, 0.5*inch))
        
        # Add summaries for each topic
        for i, (topic, summary) in enumerate(topic_summaries.items(), 1):
            # Add topic heading
            story.append(Paragraph(f"{i}. {topic}", topic_style))
            story.append(Spacer(1, 0.1*inch))
            
            # Add summary (escape HTML special characters)
            summary_escaped = summary.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            story.append(Paragraph(summary_escaped, summary_style))
            
            # Add spacing between topics (except for last one)
            if i < len(topic_summaries):
                story.append(Spacer(1, 0.3*inch))
        
        # Build PDF
        doc.build(story)
        
        print(f"\n✓ PDF generated: {output_path}")
        return output_path
    
    def run_workflow(self, topics: List[str], top_k: int = 5, output_filename: Optional[str] = None) -> Dict[str, Any]:
        """
        Run the complete workflow: load embeddings, search topics, summarize, and generate PDF.
        
        Args:
            topics: List of topics to search and summarize
            top_k: Number of top results to retrieve per topic
            output_filename: Optional custom output filename
            
        Returns:
            Dictionary with workflow results
        """
        print("=" * 60)
        print("Starting Workflow Service")
        print("=" * 60)
        
        # Step 1: Load embeddings
        vector_data = self.load_embeddings()
        
        # Step 2: Search topics
        topic_results = self.search_topics(topics, top_k=top_k, vector_data=vector_data)
        
        # Step 3: Loop through topics and summarize
        print(f"\nSummarizing information for {len(topics)} topic(s)...")
        topic_summaries = {}
        
        for topic in topics:
            print(f"  Summarizing: '{topic}'")
            # Get chunks from search results
            chunks = [result["chunk"] for result in topic_results[topic]]
            
            # Summarize
            summary = self.summarize_information(topic, chunks)
            topic_summaries[topic] = summary
            print(f"    ✓ Summary created ({len(summary)} characters)")
        
        # Step 4: Generate PDF
        print(f"\nGenerating PDF with summaries...")
        pdf_path = self.generate_pdf(topic_summaries, output_filename)
        
        print("\n" + "=" * 60)
        print("Workflow completed successfully!")
        print("=" * 60)
        
        return {
            "status": "success",
            "topics_processed": len(topics),
            "pdf_path": str(pdf_path),
            "summaries": topic_summaries
        }

