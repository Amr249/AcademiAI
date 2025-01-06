# AcaGenie - AI-Powered Academic Assistant

AcaGenie is an AI-powered academic assistant designed to simplify, enhance, and revolutionize the academic and research experience for students, professors, and researchers. The platform offers a suite of tools that help users save time, streamline their work, and focus on learning, teaching, and discovery. The project is built using **Streamlit** for the frontend and integrates various AI models, including **OpenAI's GPT-4**, for backend processing.

---

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
   git clone https://github.com/yourusername/AcaGenie.git
2. **Navigate to the project directory:**:
   ```bash
   cd AcaGenie
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
