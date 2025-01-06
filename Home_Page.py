import streamlit as st 
st.set_page_config(layout="wide")

# Custom CSS
custom_css = """
<style>

@import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;800&display=swap");

:root {
  --clr-1: #00c2ff;
  --clr-2: #33ff8c;
  --clr-3: #ffc640;
  --clr-4: #e54cff;

  --blur: 1rem;
  --fs: clamp(1rem, 4vw, 3rem); /* Adjusted to smaller values */
  --ls: clamp(-1.75px, -0.25vw, -3.5px);
}

body {
  min-height: 100vh;
  margin: 0; /* Remove default margin */
  padding: 0; /* Remove default padding */
  background-color: var(--bg);
  font-family: "Inter", "DM Sans", Arial, sans-serif;
}

*,
*::before,
*::after {
  font-family: inherit;
  box-sizing: border-box;
}

#header-div {
  height: 400px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  gap: 20px; /* Space between text and image */
  padding: 0 20px; /* Optional: Add padding to the sides */
  width: 100%; /* Ensure it takes full width */
  max-width: 1100px; /* Optional: Limit maximum width */
  margin: 0 auto; /* Center the container */
}

#text-div {
  width: 50%; /* Ensure it takes exactly 50% width */
  text-align: left;
  padding-top: 50px; /* Adjust top padding if needed */
  padding-right: 10px; /* Adjust right padding if needed */
  box-sizing: border-box; /* Include padding in the width calculation */
}

#text-div p{
    color: white;
}



/* Content and Aurora Effects */
.content {
  text-align: center;
}

.title {
  font-size: var(--fs);
  font-weight: 800;
  letter-spacing: var(--ls);
  position: relative;
  overflow: hidden;
  background: var(--bg);
  margin: 0;
}

.subtitle {
  font-size: clamp(0.8rem, 2vw, 1.5rem); /* Adjusted for subtitle */
}

.aurora {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 2;
  mix-blend-mode: darken;
  pointer-events: none;
}

.aurora__item {
  overflow: hidden;
  position: absolute;
  width: 60vw;
  height: 60vw;
  background-color: var(--clr-1);
  border-radius: 37% 29% 27% 27% / 28% 25% 41% 37%;
  filter: blur(var(--blur));
  mix-blend-mode: overlay;
}

.aurora__item:nth-of-type(1) {
  top: -50%;
  animation: aurora-border 6s ease-in-out infinite,
    aurora-1 12s ease-in-out infinite alternate;
}

.aurora__item:nth-of-type(2) {
  background-color: var(--clr-3);
  right: 0;
  top: 0;
  animation: aurora-border 6s ease-in-out infinite,
    aurora-2 12s ease-in-out infinite alternate;
}

.aurora__item:nth-of-type(3) {
  background-color: var(--clr-2);
  left: 0;
  bottom: 0;
  animation: aurora-border 6s ease-in-out infinite,
    aurora-3 8s ease-in-out infinite alternate;
}

.aurora__item:nth-of-type(4) {
  background-color: var(--clr-4);
  right: 0;
  bottom: -50%;
  animation: aurora-border 6s ease-in-out infinite,
    aurora-4 24s ease-in-out infinite alternate;
}

@keyframes aurora-1 {
  0% {
    top: 0;
    right: 0;
  }

  50% {
    top: 100%;
    right: 75%;
  }

  75% {
    top: 100%;
    right: 25%;
  }

  100% {
    top: 0;
    right: 0;
  }
}

@keyframes aurora-2 {
  0% {
    top: -50%;
    left: 0%;
  }

  60% {
    top: 100%;
    left: 75%;
  }

  85% {
    top: 100%;
    left: 25%;
  }

  100% {
    top: -50%;
    left: 0%;
  }
}

@keyframes aurora-3 {
  0% {
    bottom: 0;
    left: 0;
  }

  40% {
    bottom: 100%;
    left: 75%;
  }

  65% {
    bottom: 40%;
    left: 50%;
  }

  100% {
    bottom: 0;
    left: 0;
  }
}

@keyframes aurora-4 {
  0% {
    bottom: -50%;
    right: 0;
  }

  50% {
    bottom: 0%;
    right: 40%;
  }

  90% {
    bottom: 50%;
    right: 25%;
  }

  100% {
    bottom: -50%;
    right: 0;
  }
}

@keyframes aurora-border {
  0% {
    border-radius: 37% 29% 27% 27% / 28% 25% 41% 37%;
  }

  25% {
    border-radius: 47% 29% 39% 49% / 61% 19% 66% 26%;
  }

  50% {
    border-radius: 57% 23% 47% 72% / 63% 17% 66% 33%;
  }

  75% {
    border-radius: 28% 49% 29% 100% / 93% 20% 64% 25%;
  }

  100% {
    border-radius: 37% 29% 27% 27% / 28% 25% 41% 37%;
  }
}




/* ------------------------------------------------------ Assistant Image - Section  ------------------------------------------------------------ */

#AIimg-div {
    height: 500px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden; /* Ensure the zoom effect doesn't overflow */
}

#AIimg-div img {
    width: 30%; /* Adjust as needed */
    height: 400px; /* Maintain aspect ratio */
    display: block;
    margin: auto;
    border-radius: 50%;
    animation: zoomInOut 3s infinite alternate; /* Add zoom animation */
}

@keyframes zoomInOut {
    0% {
        transform: scale(1); /* Original size */
    }
    100% {
        transform: scale(1.2); /* Zoomed size */
    }
}

/* ------------------------------------------------------ More That Just A Tool - Section  ------------------------------------------------------------ */

#offer-div {
    margin-top: 50px;
    
}

#text-offer-div{
    text-align: center;
    margin-bottom: 10px;
}

#text-offer-div h6{
    color: gray;
}

#offer-div p {
    color: white; 
    font-size: 16px; 
    line-height: 1.5; 
}



/* --------------------------------------------------------- First Features Row - Section -------------------------------------------------------------- */

#row2-div1 {
    display: flex;
    justify-content: space-between;
    width: 100%;
    overflow: auto;
    padding: 10px;
}

#chat-div{
    display: flex;
    justify-content: space-between;
    width: 100%;
    overflow: auto;
    padding: 10px;
    background-color: yellow;

    width: 63%;
    text-align: center;
    padding: 10px;
    background-image: linear-gradient(to right, #7372d8 , white);
    border-style: solid;
    border-color: #7f7f7f;
    border-width: 2px;
    border-radius: 10px
}

#chat-div #img-div {
    width: 35%;
    text-align: center;

    overflow: hidden; /* Ensures the image respects the border radius */
}

#img-div img {
  width: 80%;
  height: 100%;
  object-fit: cover; /* Ensures the image covers the div without distortion */
  border-radius: inherit; /* Inherits the border radius from the parent */
}

#paragragh-div{
    width: 63%;
    text-align: left;
    padding: 50px 20px 10px;
}

#summarize-div{
    width: 35%;
    height: 260px;
    text-align: center;
    padding: 10px;
        background-image: linear-gradient(to left, #37aeda , white);
    border-style: solid;
    border-color: #7f7f7f;
    border-width: 2px;
    border-radius: 10px;
}


#row2-div1 #chat-div p, #row2-div1 #summarize-div p, #row2-div1 #chat-div h4, #row2-div1 #summarize-div h4{
    color: black;
}


/* --------------------------------------------------------------- Second Features Row -------------------------------------------------------------- */


#row2-div2 {
    display: flex;
    justify-content: space-between;
    width: 100%;
    overflow: auto;
    padding: 10px;
    gap: 20px; /* Add space between flex items */
}

#quiz-div {
    width: 35%;
    text-align: center;
    padding: 10px;
    background-image: linear-gradient(to right, #7372d8 , white);

}

#Presentation-div {
    width: 63%;
    text-align: center;
    padding: 10px;
    display: flex;
    justify-content: space-between;
    overflow: auto;
    background-image: linear-gradient(to left, #ba37da , white);

}

#Presentation-div #img-div {
    width: 40%;
    text-align: center;
    overflow: hidden; /* Ensures the image respects the border radius */
}

#Presentation-div #paragragh-div {
    width: 60%;
    text-align: left;
    padding: 30px;
}

#row2-div2 #quiz-div p, #row2-div2 #Presentation-div p, #row2-div2 #quiz-div h4, #row2-div2 #Presentation-div h4{
    color: black;
}

#quiz-div , #Presentation-div{
    border-style: solid;
    border-color: #7f7f7f;
    border-width: 2px;
    border-radius: 10px;
}

/* --------------------------------------------------------- 3rd Features Row - Section -------------------------------------------------------------- */

#row-div3{
    padding: 10px;
}

#audiobook-div {
    background-image: linear-gradient(to right, white, white, #7372d8, #df13ac);
    display: flex;
    justify-content: space-around;
    width: 100%;
    overflow: auto;
    text-align: center;
    padding: 10px;
    border-style: solid;
    border-color: #7f7f7f;
    border-width: 2px;
    border-radius: 10px
} 

#audiobook-div #img-div {
    width: 33%;
    text-align: center;
    overflow: hidden; /* Ensures the image respects the border radius */
    border-style: solid;
    border-width: 2px;
    border-radius: 50px;
}

#audiobook-div #img-div img {
  width: 100%;
  height: 100%;
  object-fit: cover; /* Ensures the image covers the div without distortion */
  border-radius: inherit; /* Inherits the border radius from the parent */
  
}

#audiobook-div #paragragh-div{
    width: 63%;
    text-align: left;
    padding: 50px 20px 10px;
}

#audiobook-div p, #audiobook-div h4{
    color: black;
}

#audiobook-div, #summarize-div, #chat-div, #quiz-div , #Presentation-div {

}

/* --------------------------------------------------------------- Footer section -------------------------------------------------------------- */

#transform-div{
        margin-top: 150px;
        position: relative;
        border-radius: 50px;
}

#transform-div h1{
    color: white;
    text-align: center;
}
#transform-div h6{
    color: #afafaf;
    padding: 1px 100px;
    text-align: center;
    font-size: 20px;
}

#button-div {
    display: flex;
    justify-content: center; /* Fixed: Changed space-center to center */
    width: 100%;
    overflow: auto;
    padding: 30px;
}

#transform-div button {
    margin: auto;
    color: black;
    font-size: 25px;
    font-weight: bold;
    background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
    background-size: 400% 400%;
    animation: gradient 15s ease infinite;
    height: 70px;
    width: 300px;
    border-style: solid;
    border-color: black;
    border-width: 5px;
    border-radius: 50px;
    cursor: pointer; /* Add cursor pointer for better UX */
}

@keyframes gradient {
	0% {
		background-position: 0% 50%;
	}
    25%{
        background-position: 100% 50%;
    }
	50% {
		background-position: 0% 50%;
	}
    75%{
        background-position: 100% 50%;
    }
	100% {
		background-position: 0% 50%;
	}
}

}



</style>
"""

# Apply CSS
st.markdown(custom_css, unsafe_allow_html=True)


# --------------------------------------------- Hero section ---------------------------------------------------------- #
st.markdown('''

<div id="header-div">
    <div class="content">
        <h1 class="title">AcamdiAI - Your academic assistant powered by AI.
            <div class="aurora">
            <div class="aurora__item"></div>
            <div class="aurora__item"></div>
            <div class="aurora__item"></div>
            <div class="aurora__item"></div>
            </div>
        </h1>
        <p class="subtitle">Unlock the power of AI to simplify, enhance, and revolutionize your academic and research experience. Designed with students, professors, and researchers in mind, our suite of tools helps you save time, streamline your work, and focus on what truly matters—learning, teaching, and discovery.</p>
    </div>
</div>

''', unsafe_allow_html=True)

st.markdown('''

<div id="AIimg-div">
    <img src="https://i.ibb.co/wwj0zfw/assistant.png">
</div>

''', unsafe_allow_html=True)


# --------------------------------------------- What We Offer ? section ---------------------------------------------------------- #
st.markdown('''

<div id="offer-div">
    <div id="text-offer-div">
        <h1>More That Just A Tool !</h1>
        <h6>Explore what AcGeni offer for you</h6>
    </div>
    <div id="row2-div1">
        <div id="chat-div">
            <div id="img-div">
                <img src="https://www.writecream.com/wp-content/uploads/2023/05/1-61.png">
            </div>
            <div id="paragragh-div">
                <h4>Chat with PDF</h4>
                <p>Transform static documents into interactive conversations. Upload your PDFs, ask questions, and let our AI extract insights, clarify concepts, and provide instant answers.</p>
            </div>
        </div>
        <div id="summarize-div"> 
            <img src="https://cdn-icons-png.flaticon.com/512/5004/5004273.png" width="100" height="100">
            <h4>Custom Summarization</h4>
            <p>Simplify your tasks with AI-powered YouTube, blog, and PDF summarization, delivering key insights quickly and efficiently.</p>
        </div>
    </div>
    <div id="row2-div2">
       <div id="quiz-div">
            <img src="https://cdn-icons-png.flaticon.com/512/2641/2641457.png" width="100" height="100">
            <h4>Quiz and Flashcards Generator</h4>
            <p>Upload a document, and this app will create a quiz or flashcards based on its content.</p>
        </div>
        <div id="Presentation-div"> 
            <div id="paragragh-div">
                <h4>Text to Presentation</h4>
                <p>Turn your written content into visually engaging presentations in minutes. Perfect for professors preparing lectures, students creating class projects, or researchers showcasing their findings.</p>
            </div>
            <div id="img-div">
                <img src="https://create.microsoft.com/_next/image?url=https%3A%2F%2Fdsgrcdnblobprod5u3.azureedge.net%2Fimages%2Fcollections%2Fpowerpoint%2Fppt-seo-1.webp&w=828&q=75">
            </div>
        </div>
    </div>
    <div id="row-div3">  
        <div id="audiobook-div">
                <div id="img-div">
                    <img src="https://img.freepik.com/premium-vector/collection-books-including-headphones-book-book-titled-headphones_9493-63459.jpg">
                </div>
                <div id="paragragh-div">
                    <h4>Paper to Audio-Book Generator</h4>
                    <p>Transform your research papers, study materials, and documents into immersive audio experiences. With our advanced AI-powered tool, you can convert any text into high-quality audiobooks featuring natural-sounding voices. Whether you're commuting, exercising, or multitasking, listen to your content on the go and absorb knowledge effortlessly. Perfect for students, researchers, and professionals who want to make the most of their time while staying productive.</p>
                </div>
        </div>  
    </div>        
</div>

''', unsafe_allow_html=True)




# --------------------------------------------- Transform section ---------------------------------------------------------- #

st.markdown('''

<div id="transform-div">
    <h1>Transform the Way You Work and Learn</h1>
    <h6>Our app is more than a tool—it’s your academic partner. Whether you're a student striving for better grades, a professor managing multiple classes, or a researcher exploring groundbreaking ideas, we’re here to empower you every step of the way.</h6>
    <div id = "button-div"><button type="button">Get Started Now</button></div>
    
</div>

''', unsafe_allow_html=True)


