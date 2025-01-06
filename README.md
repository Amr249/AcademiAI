# AcademiAI - AI-Powered Academic Assistant

AcaGenie is an AI-powered academic assistant designed to simplify, enhance, and revolutionize the academic and research experience for students, professors, and researchers. The platform offers a suite of tools that help users save time, streamline their work, and focus on learning, teaching, and discovery. The project is built using **Streamlit** for the frontend and integrates various AI models, including **OpenAI's GPT-4**, for backend processing.

---

<video width="640" height="480" controls>
  <source src="https://youtu.be/Uc78DAk4kdw" type="video/mp4">
  Your browser does not support the video tag.
</video>
## Features

- **Chat with PDFs**: Interact with multiple PDFs at once using AI. Upload your research papers, textbooks, or lecture notes, and ask questions to get instant, context-aware answers.
- **Custom Summarization**: Summarize content from PDFs, blogs, or YouTube videos with customizable prompts and settings.
- **Quiz and Flashcards Generator**: Transform your study material into interactive quizzes and flashcards.
- **Text to Presentation**: Turn your written content into visually engaging presentations in minutes.
- **Paper to Audio-Book**: Convert your research papers and documents into immersive audiobooks.

---

## Installation Instructions

1. **Clone the AcaGenie repository**:
   ```bash
   git clone https://github.com/Amr249/AcademiAI.git
2. **Navigate to the project directory:**:
   ```bash
   cd AcademiAI
3. **Create a virtual environment:**:
   ```bash
   python -m venv venv
4. **Activate the virtual environment:**:
      ```bash
      On Windows:
      venv\Scripts\activate

      On macOS/Linux:
      source venv/bin/activate
4. **Install the dependencies:**:
   ```bash
   pip install -r requirements.txt
5. **Create a .env file in the project root and add your OpenAI API key:**:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
6. **Run the Streamlit app:**:
   ```bash
   streamlit run Home_Page.py

---

## Usage
**Home Page:** The home page provides an overview of the available tools and features. Navigate through the different sections to explore the functionalities.

**Chat with PDFs:** Upload your PDFs and start interacting with the AI to get instant answers to your questions.

**Custom Summarization:** Upload a PDF, blog URL, or YouTube video link, and generate summaries with customizable prompts.

**Quiz and Flashcards Generator:** Upload a document and generate quizzes or flashcards based on its content.

**Text to Presentation:** Enter a topic and generate a PowerPoint presentation with AI-generated content and images.

**Paper to Audio-Book:** Upload a PDF and convert it into an audiobook with a custom cover image.

---

## Dependencies
The project relies on the following Python libraries:

**streamlit:** For building the web interface.

**openai:** For accessing GPT models.

**PyPDF2:** For extracting text from PDF files.

**langchain:** For text processing and summarization.

**faiss-cpu:** For vector storage and retrieval.

**python-dotenv:** For loading environment variables.

**gtts:** For text-to-speech conversion.

**pptx:** For creating PowerPoint presentations.

**requests:** For making HTTP requests.

**beautifulsoup4:** For parsing HTML content.

**youtube-transcript-api:** For fetching YouTube transcripts.

---

## Acknowledgments
OpenAI for providing the GPT models.

Streamlit for the web framework.

Unsplash for providing free images for presentations.

### Contact
For any questions or feedback, please contact amrogamaraldwlah@gmail.com .
