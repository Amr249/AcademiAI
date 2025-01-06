import streamlit as st
import openai
import PyPDF2
from dotenv import load_dotenv, find_dotenv
import os

# Load environment variables from the .env file
load_dotenv(find_dotenv())

# Retrieve the OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# Helper Function to Extract Text
def extract_text(file):
    if file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        text = " ".join([page.extract_text() for page in reader.pages])
    elif file.name.endswith(".txt"):
        text = file.read().decode("utf-8")
    else:
        text = ""
    return text

# Generate Quiz Using GPT
def generate_quiz(text, num_questions=5):
    prompt = f"""
    Generate a quiz with {num_questions} multiple-choice questions based on the following content:
    {text}
    Each question should have 4 options, with one correct answer clearly marked. 
    Format each question as follows:
    - Question: <question text>
    - a. Option A
    - b. Option B
    - c. Option C
    - d. Option D
    Indicate the correct answer with [Correct Answer].
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# Generate Flashcards Using GPT
def generate_flashcards(text, num_flashcards=5):
    prompt = f"""
    Based on the following text, generate {num_flashcards} flashcards. Each flashcard should contain:
    1. A question.
    2. The correct answer.
    Provide the flashcards in a clear format:
    - Q: <Question>
    - A: <Answer>
    {text}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]



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


# Streamlit App
def main():



# Apply CSS
    st.markdown(custom_css, unsafe_allow_html=True)
       

    st.markdown('''
        <div id="transform-div">
            <h1>Quiz and Flashcards Generator 📑</h1>
            <h6>Welcome to the Quiz and Flashcards Generator page! Transform your study material into interactive quizzes and flashcards in just a few steps. Whether you're preparing for exams or reinforcing learning, this tool makes studying engaging and efficient. Simply input your content, and let us handle the rest. Start mastering your knowledge today!</h6>
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
                <img src="https://cdn-icons-png.flaticon.com/512/709/709337.png" width="50" height="50">
                <h4>Choose the number of questions  </h4>
            </div>
            <div id="Audio-div">
                <img src="https://cdn-icons-png.flaticon.com/512/7128/7128236.png" width="50" height="50">
                <h4>Get AI generated questions</h4>
            </div>
        </div>     
    </div>

    ''', unsafe_allow_html=True)
    
    # File Uploader
    uploaded_file = st.file_uploader("Upload a Text or PDF File", type=["txt", "pdf"])
    num_questions = st.slider("Number of Quiz Questions", min_value=1, max_value=20, value=5)
    num_flashcards = st.slider("Number of Flashcards", min_value=1, max_value=20, value=5)
    
    if uploaded_file:
        text = extract_text(uploaded_file)
        st.write("### Document Content Preview:")
        with st.expander('Click to preview the extracted text'):
            st.write(text)
        #st.text_area("Extracted Text", text[:1000] + "..." if len(text) > 1000 else text, height=200)
        

        col1, col2 = st.columns(2)

        with col1:
            # Quiz Generation
            if st.button("Generate Quiz", use_container_width=True):
                st.write("### Quiz:")
                quiz = generate_quiz(text, num_questions)
            
            # Modify the output to ensure each choice is in a separate line
                quiz_lines = quiz.splitlines()
                for line in quiz_lines:
                    if line.startswith("a.") or line.startswith("b.") or line.startswith("c.") or line.startswith("d."):
                        st.write(line)
                    else:
                        st.markdown(f"**{line}**")  # Questions in bold
                st.success("Quiz generated successfully!")
        
        with col2:
            # Flashcards Generation
            if st.button("Generate Flashcards", use_container_width=True):
                st.write("### Flashcards:")
                flashcards = generate_flashcards(text, num_flashcards)
                st.markdown(flashcards)
                st.success("Flashcards generated successfully!")
    
if __name__ == "__main__":
    main()
