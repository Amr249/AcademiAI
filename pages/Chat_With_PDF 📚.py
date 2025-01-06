import os
import streamlit as st
from dotenv import load_dotenv, find_dotenv # to import the API keys 
from PyPDF2 import PdfReader 
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from HtmlTemplates import user_template, bot_template, css
from langchain.llms import huggingface_hub
from gtts import gTTS
import time

# function to extract text from PDFs
def get_pdf_text(user_pdfs):
    text = "" # variable to store all the text from all the PDFs

    for pdf in user_pdfs: # loop through all the PDFs the user entered
        pdf_reader = PdfReader(pdf) # create a PDF object that have pages 
        for page in pdf_reader.pages: # loop throough the pages 
            text += page.extract_text() # append all the text in each page to text variable 
    return text 


# function to turn the entire extracted text into chunks 
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n", # set the seperator as a single line 
        chunk_size=1000, # chunck after a 1000 character 
        chunk_overlap=200,
        length_function=len)
    
    # split all the text into chunks and store it in chunks variable
    chunks = text_splitter.split_text(text)
    return chunks


# function to convert the text chunks into vectors 
def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()

    # embeddings = HuggingFaceInstructEmbeddings(model_name ="hkunlp/instructor-xl") another model to use 
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore



def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    #llm = huggingface_hub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        retriever = vectorstore.as_retriever(),
        memory = memory
    )

    return conversation_chain


def handle_user_question(user_question):   
    # Pass the user's question to the conversational AI model (stored in session state)
    response = st.session_state.conversation({'question': user_question})
    
    # Update the chat history in the session state with the new response
    st.session_state.chat_history = response['chat_history']

    # Loop through the chat history to display each message
    for i, message in enumerate(st.session_state.chat_history):
        # Check if the message is from the user (even index)
        if i % 2 == 0:
            # Use the user template to display the user's message
            st.write(
                user_template.replace("{{MSG}}", message.content),  # Replace placeholder with message content
                unsafe_allow_html=True  # Allow HTML rendering for the template
            )
        else:
            # Use the bot template to display the AI's response
            st.write(
                bot_template.replace("{{MSG}}", message.content),  # Replace placeholder with message content
                unsafe_allow_html=True  # Allow HTML rendering for the template
            )

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
    justify-content: space-around;
    width: 100%;
    overflow: auto;
    padding: 10px;
    margin-bottom: 70px;
}

#chat-div, #summarize-div, #Audio-div {
    width: 30%;
    text-align: center;
    padding: 10px;
    background-color: #f2f2f2;
    border-radius: 50px;
    border-style: solid;
    border-color: #7f7f7f;
    border-width: 2px;
    border-radius: 10px;
}

#row3-div h4{
    color: black;
}


#transform-div{
        margin-top: 20px;
        position: relative;
}

#transform-div h1{
    text-align: center;
}
#transform-div h6{
    color: #afafaf;
    text-align: center;
    padding: 10px 50px;
}





</style>
"""


def main():
    load_dotenv()

    st.set_page_config(page_title="Chat with multiple PDFs", layout="wide")
    st.write(css, unsafe_allow_html=True)


    # check if conversation is in the session state
    if "conversation" not in st.session_state:
        st.session_state.conversation = None

     # Apply CSS
    st.markdown(custom_css, unsafe_allow_html=True)
       
# --------------------------------------------- Main section ------------------------------------------- #
    st.markdown('''
        <div id="transform-div">
            <h1>Chat with multiple PDFs 📚</h1>
            <h6>Effortlessly interact with multiple PDFs at once using AI. Upload your research papers, textbooks, or lecture notes, and ask questions to get instant, context-aware answers. This tool simplifies your study and research by extracting key insights from multiple documents, saving you time and helping you focus on what matters most. Start streamlining your academic workflow today!</h6>
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
                <img src="https://cdn-icons-png.freepik.com/256/16090/16090500.png?semt=ais_hybrid" width="50" height="50">
                <h4>Wait till the documents get processed </h4>
            </div>
            <div id="Audio-div">
                <img src="https://cdn-icons-png.flaticon.com/512/9374/9374926.png" width="50" height="50">
                <h4>Chat with AI about your documents</h4>
            </div>
        </div>     
    </div>

    ''', unsafe_allow_html=True)


    user_pdfs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
    
    if st.button("Process", use_container_width=True):
            with st.spinner("Process"):
                # get the PDF text 
                PDF_raw_text = get_pdf_text(user_pdfs)

                # get the text Chunks
                text_chunks = get_text_chunks(PDF_raw_text)

                # create vectore store
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain 
                st.session_state.conversation = get_conversation_chain(vectorstore)
                
                st.success("Done!")

                # Allow the user to view the PDF text
                with st.expander("Click to view the PDF text"):
                    st.write(PDF_raw_text)

    user_question = st.text_input("Ask a question about your documents:")
    
    if user_question:
        handle_user_question(user_question)

if __name__ == '__main__':
    main()