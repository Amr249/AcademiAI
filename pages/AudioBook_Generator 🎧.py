import openai
import streamlit as st
from tempfile import NamedTemporaryFile
from gtts import gTTS
import pdfplumber
import os
from dotenv import load_dotenv, find_dotenv
import time
from PIL import Image
from io import BytesIO
import requests
import replicate
import time

# Load environment variables from the .env file
load_dotenv(find_dotenv())

# Retrieve the OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Extracting the text from a PDF file
def extract_text_from_pdf(uploaded_file):
    # Use BytesIO to treat the uploaded file as a file-like object
    pdf_content = BytesIO(uploaded_file.read())  # Reading file bytes into memory
    with pdfplumber.open(pdf_content) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Convert the PDFs text into speech
def text_to_speech(text, output_path):
    time.sleep(10)
    tts = gTTS(text=text, lang='en')
    tts.save(output_path)

# Function to generate cover art based on the podcast's topic
def generate_cover_art(cover_art_title):
    # Use DALL·E to generate an image based on the podcast title or description
    prompt = f""" Create an artistic podcast cover for a podcast titled '{cover_art_title}'.
            It should reflect the topics discussed in the research paper,
            include things realted to podcasts in the image like Microphone, speaker, Headphones and studio please,
            NOTE that you dont have to include them all just include what is better for the design, ALSO Include no
            Text in the cover image"""

    # Generate the image using OpenAI's DALL·E model
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"  # You can adjust the image size
    )
    
    # Get the URL of the generated image
    image_url = response['data'][0]['url']
    
    # Fetch and load the image
    image = Image.open(BytesIO(requests.get(image_url).content))
    return image

# CSS code
custom_css = """
<style>

#offer-div {
    margin-top: 30px;
}

#text-offer-div{
    text-align: center;
}

#row3-div {
    display: flex;
    justify-content: space-evenly;
    width: 100%;
    overflow: auto;
    padding: 10px;
    margin-bottom: 50px;
}

#chat-div, #summarize-div, #Audio-div {
    width: 30%;
    text-align: center;
    padding: 10px;
    background-color: #f2f2f2;
    border-radius: 50%;
    box-sizing: border-box;
    border-radius: 50px;
    border-style: solid;
    border-color: #7f7f7f;
    border-width: 2px;
    border-radius: 10px;
}

#row3-div h4{
    color: black;
}

rgin-top: 10px;
}


#transform-div{
        margin-top: 20px;
        position: relative;
}

#transform-div h1{
    text-align: center;
}

#transform-div h6{
    text-align: center;
    color: #afafaf;
    text-align: center;
    padding: 10px 50px;
}

</style>
"""

# Apply CSS
st.markdown(custom_css, unsafe_allow_html=True)
       
# --------------------------------------------- Main section ------------------------------------------- #
st.markdown('''
        <div id="transform-div">
            <h1>Paper to Audio-Book 🎧</h1>
            <h6>Transform your PDF documents into immersive audiobooks with ease. Upload any PDF, and we'll generate an audiobook complete with a custom cover image. Whether you're studying, multitasking, or simply relaxing, enjoy your content hands-free. Start turning your documents into engaging audio experiences today!</h6>
        </div>
    ''', unsafe_allow_html=True)

# --------------------------------------------- How it works? section ------------------------------------------- #
st.markdown('''
    <div id="offer-div">
        <div id="text-offer-div">
            <h1>How it works ?</h1>
        </div>
        <div id="row3-div">
            <div id="chat-div">
                <img src="https://www.iconpacks.net/icons/2/free-pdf-upload-icon-2619-thumb.png" width="50" height="50">
                <h4>Upload your documents</h4>
            </div>
            <div id="summarize-div"> 
                <img src="https://cdn-icons-png.flaticon.com/512/17079/17079094.png" width="50" height="50">
                <h4>Enter the document title to generate a Cover image for the Audio-Book</h4>
            </div>
            <div id="Audio-div">
                <img src="https://images.vexels.com/content/150845/preview/audio-headphones-icon-2df781.png" width="50" height="50">
                <h4>Listen to your Generated Audio-Book </h4>
            </div>
        </div>     
    </div>

    ''', unsafe_allow_html=True)


# File upload: Allow user to upload multiple PDF files
uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)
if uploaded_files:
    papers_text = []

    # Extract text from each uploaded PDF
    for uploaded_file in uploaded_files:
        text = extract_text_from_pdf(uploaded_file)  # Pass the uploaded file directly
        papers_text.append(text)  # Collect the extracted text from all papers

    cover_art_title = st.text_input("Enter the paper title please ")  # You can change this dynamically

    # Ensure that there is at least one paper uploaded for the dialogue generation
    if len(papers_text) >= 1 and cover_art_title is not None:
        #Generate dialogue from the extracted text using GPT
        #dialogue_script = generate_dialogue(papers_text)

        # Generate cover art for the podcast based on the dialogue
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Generate cover Art Image", use_container_width=True):
                with st.spinner("Generating Cover Art"):
                    cover_art_image = generate_cover_art(cover_art_title)
                    # Display the generated cover art
                    st.image(cover_art_image, caption="Podcast Cover Art", use_column_width=True)
                    # Display success message
                    st.success("Cover Art generated successfully!")

        with col2:
            with st.expander("View the PDF text"):
                # Display the PDF text
                st.write(papers_text[0])


        if st.button("Generate Audio-Book", use_container_width=True):
            with st.spinner("Generating Audio-Book"):
                    cover_art_image = generate_cover_art(cover_art_title)
                    # Convert the dialogue script into speech
                    output_audio_path = "generated_podcast.mp3"
                    if papers_text:
                        combined_text = "\n".join(papers_text)  # Join the list of text into one string
                        text_to_speech(combined_text, output_audio_path)

                    # Provide download link for the generated podcast
                    with open(output_audio_path, "rb") as audio_file:
                        st.success("Audio-Book generated successfully!")
                        st.audio(audio_file.read(), format='audio/mp3')
                        st.download_button("Download The Generated Audio-Book", audio_file, file_name=output_audio_path, use_container_width = True)

  
    else:
        st.warning("Please upload at least one paper for generating a podcast.")
