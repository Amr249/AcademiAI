# Import necessary libraries
import openai
import streamlit as st
import os
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
import base64
import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import re

# Load environment variables from the .env file
load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

# Cache the function to avoid redundant processing of the same PDF file
@st.cache_data
def setup_documents(pdf_file_path, chunk_size, chunk_overlap):
    """
    Load and split a PDF file into smaller chunks for processing.
    Args:
        pdf_file_path (str): Path to the PDF file.
        chunk_size (int): Size of each text chunk.
        chunk_overlap (int): Overlap between chunks.
    Returns:
        List[Document]: List of text chunks as LangChain documents.
    """
    loader = PyPDFLoader(pdf_file_path)  # Load the PDF file
    docs_raw = loader.load()  # Extract raw text from the PDF
    docs_raw_text = [doc.page_content for doc in docs_raw]  # Extract text content from each page
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = text_splitter.create_documents(docs_raw_text)  # Split text into chunks
    return docs

def show_pdf_with_expander(file_path):
    """
    Display a PDF file in an expandable section using base64 encoding.
    Args:
        file_path (str): Path to the PDF file.
    """
    with st.expander("Click to view the PDF"):
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode("utf-8")  # Encode PDF to base64
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="850" height="1000" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)  # Display PDF in an iframe

def fetch_blog_content(url):
    """
    Fetch and extract text content from a blog URL.
    Args:
        url (str): URL of the blog.
    Returns:
        str: Extracted text content.
    """
    try:
        response = requests.get(url)  # Send a GET request to the blog URL
        soup = BeautifulSoup(response.content, "html.parser")  # Parse the HTML content
        paragraphs = soup.find_all("p")  # Find all paragraph tags
        content = "\n".join([p.get_text() for p in paragraphs if p.get_text()])  # Extract text from paragraphs
        return content
    except Exception as e:
        st.error(f"Error fetching blog content: {e}")  # Display error message if fetching fails
        return None

def fetch_youtube_transcript(video_url):
    """
    Fetch the transcript of a YouTube video using its URL.
    Args:
        video_url (str): URL of the YouTube video.
    Returns:
        tuple: (formatted_transcript, video_id) or (None, None) if an error occurs.
    """
    # Extract video ID using regex
    video_id_match = re.search(r"(?:youtube\.com\/(?:[^\/]+\/.+\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]+)", video_url)
    if not video_id_match:
        st.error("Invalid YouTube URL.")  # Display error if the URL is invalid
        return None, None

    video_id = video_id_match.group(1)  # Extract the video ID
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)  # Fetch the transcript
        formatter = TextFormatter()
        formatted_transcript = formatter.format_transcript(transcript)  # Format the transcript as plain text
        return formatted_transcript, video_id
    except Exception as e:
        st.error(f"Error fetching transcript: {e}")  # Display error if fetching fails
        return None, None

def custom_summary(docs, llm, custom_prompt, chain_type, num_summaries):
    """
    Generate summaries using a custom prompt and selected chain type.
    Args:
        docs (List[Document]): List of text chunks to summarize.
        llm: Language model to use for summarization.
        custom_prompt (str): Custom prompt for summarization.
        chain_type (str): Type of summarization chain (map_reduce, stuff, refine).
        num_summaries (int): Number of summaries to generate.
    Returns:
        List[str]: List of generated summaries.
    """
    custom_prompt = custom_prompt + """:\n {text}"""  # Append the custom prompt
    COMBINE_PROMPT = PromptTemplate(template=custom_prompt, input_variables=["text"])
    MAP_PROMPT = PromptTemplate(template="Summarize:\n{text}", input_variables=["text"])
    if chain_type == "map_reduce":
        chain = load_summarize_chain(llm, chain_type=chain_type, map_prompt=MAP_PROMPT, combine_prompt=COMBINE_PROMPT)
    else:
        chain = load_summarize_chain(llm, chain_type=chain_type)

    summaries = []
    for i in range(num_summaries):
        summary_output = chain({"input_documents": docs}, return_only_outputs=True)["output_text"]  # Generate summary
        summaries.append(summary_output)
    return summaries

# Custom CSS for styling the Streamlit app
custom_css = """
<style>
#offer-div { margin-top: 30px; }
#text-offer-div { text-align: center; }
#row3-div { display: flex; justify-content: space-around; width: 100%; overflow: auto; padding: 10px; margin-bottom: 70px; }
#chat-div, #summarize-div, #Audio-div { width: 30%; text-align: center; padding: 10px; background-color: #f2f2f2; border-radius: 50px; border-style: solid; border-color: #7f7f7f; border-width: 2px; border-radius: 10px; }
#row3-div h4 { color: black; }
#transform-div { margin-top: 20px; position: relative; }
#transform-div h1 { text-align: center; }
#transform-div h6 { color: #afafaf; text-align: center; padding: 10px 50px; }
</style>
"""

def main():
    """
    Main function to run the Streamlit app.
    """
    st.set_page_config(layout="wide")  # Set the page layout to wide
    st.markdown(custom_css, unsafe_allow_html=True)  # Apply custom CSS

    # Main section of the app
    st.markdown('''
        <div id="transform-div">
            <h1>Custom Summarization App 📑</h1>
            <h6>Effortlessly interact with multiple PDFs at once using AI. Upload your research papers, textbooks, or lecture notes, and ask questions to get instant, context-aware answers. This tool simplifies your study and research by extracting key insights from multiple documents, saving you time and helping you focus on what matters most. Start streamlining your academic workflow today!</h6>
        </div>
    ''', unsafe_allow_html=True)

    # How it works section
    st.markdown('''
        <div id="offer-div">
            <div id="text-offer-div">
                <h1>How it works ?</h1>
            </div>
            <div id="row3-div">
                <div id="chat-div">
                    <img src="https://cdn-icons-png.freepik.com/256/5732/5732163.png?semt=ais_hybrid" width="50" height="50">
                    <h4>Choose What would you like to summarize.</h4>
                </div>
                <div id="summarize-div"> 
                    <img src="https://cdn-icons-png.freepik.com/256/16090/16090500.png?semt=ais_hybrid" width="50" height="50">
                    <h4>Based on your choice Upload a File, Enter the Blog link or the YouTube Video Link</h4>
                </div>
                <div id="Audio-div">
                    <img src="https://cdn-icons-png.flaticon.com/512/10817/10817257.png" width="50" height="50">
                    <h4>Enter the summary prompt and Customize as you wish</h4>
                </div>
            </div>     
        </div>
    ''', unsafe_allow_html=True)

    # Sidebar options
    llm = st.sidebar.selectbox("LLM", ["ChatGPT", "GPT4", "Other (open source in the future)"])  # Select LLM
    chain_type = st.sidebar.selectbox("Chain Type", ["map_reduce", "stuff", "refine"])  # Select chain type
    chunk_size = st.sidebar.slider("Chunk Size", min_value=20, max_value=10000, step=10, value=2000)  # Set chunk size
    chunk_overlap = st.sidebar.slider("Chunk Overlap", min_value=5, max_value=5000, step=10, value=200)  # Set chunk overlap

    # Select summarization type
    summarization_type = st.radio("What would you like to summarize?", ["PDF Document", "Blog", "YouTube Video"])

    # Handle PDF Document summarization
    if summarization_type == "PDF Document":
        pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])  # Upload PDF file
        if pdf_file:
            temp_file_path = "temp_uploaded_file.pdf"
            with open(temp_file_path, "wb") as f:
                f.write(pdf_file.read())  # Save the uploaded file temporarily
            user_prompt = st.text_input("Enter the custom summary prompt")  # Input custom prompt
            show_pdf_with_expander(temp_file_path)  # Display the PDF
            docs = setup_documents(temp_file_path, chunk_size, chunk_overlap)  # Process the PDF
            st.write("PDF loaded successfully")

    # Handle Blog summarization
    elif summarization_type == "Blog":
        blog_url = st.text_input("Enter a blog URL")  # Input blog URL
        blog_content = st.text_area("Or paste blog content manually")  # Input manual blog content
        if blog_url:
            st.write("Fetching blog content...")
            content = fetch_blog_content(blog_url)  # Fetch blog content
            if content:
                docs = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap).create_documents([content])  # Process blog content
                user_prompt = st.text_input("Enter the custom summary prompt")
                st.write("Blog content loaded successfully")
        elif blog_content:
            docs = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap).create_documents([blog_content])  # Process manual content
            user_prompt = st.text_input("Enter the custom summary prompt")
            st.write("Manual blog content loaded successfully")

    # Handle YouTube Video summarization
    elif summarization_type == "YouTube Video":
        video_url = st.text_input("Enter YouTube video URL")  # Input YouTube URL
        if video_url:
            st.write("Fetching YouTube transcript...")
            transcript, video_id = fetch_youtube_transcript(video_url)  # Fetch transcript
            if transcript:
                # Display the embedded YouTube video
                video_embed_code = f'<iframe width="1000" height="450" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
                st.markdown(video_embed_code, unsafe_allow_html=True)
                docs = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap).create_documents([transcript])  # Process transcript
                user_prompt = st.text_input("Enter the custom summary prompt")
                st.write("YouTube transcript loaded successfully")

    # Additional settings
    temperature = st.sidebar.number_input("Set the ChatGPT Temperature", min_value=0.0, max_value=1.0, step=0.1, value=0.5)  # Set temperature
    num_summaries = st.sidebar.number_input("Number of summaries", min_value=1, max_value=10, step=1, value=1)  # Set number of summaries

    # Summarize button
    if summarization_type and st.button("Summarize", use_container_width=True):
        if 'docs' in locals() and 'user_prompt' in locals():
            if llm == "ChatGPT":
                llm = ChatOpenAI(temperature=temperature)  # Use ChatGPT
            elif llm == "GPT4":
                llm = ChatOpenAI(model_name="gpt-4", temperature=temperature)  # Use GPT-4
            else:
                st.write("Using ChatGPT while open source models are not implemented!")
                llm = ChatOpenAI(temperature=temperature)

            # Generate summaries
            result = custom_summary(docs, llm, user_prompt, chain_type, num_summaries)
            st.write("Summary:")
            for summary in result:
                st.write(summary)  # Display summaries

# Run the app
if __name__ == "__main__":
    main()