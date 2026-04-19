import streamlit as st
from PIL import Image
from google import genai
import os
from dotenv import load_dotenv


# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=api_key)

# Streamlit UI
st.title("🤖 AI Code Debugger")
st.divider()

# File uploader
uploaded_file = st.file_uploader(
    "Upload your code error screenshot",
    type=["png", "jpg", "jpeg"]
)



# Option bar
option = st.selectbox(
    "Choose Output Type",
    ["Hints", "Solution with code"]
)

# Debug button
debug_btn = st.button("Debug Code")

# Button logic
if debug_btn:

    # Validation
    if uploaded_file is None or option is None:
        st.error("⚠️ Please upload an image and select an option!")
    else:
        image = Image.open(uploaded_file)

        # Show spinner
        with st.spinner("Analyzing your code... 🔍"):

            # Gemini Model
            model = genai.GenerativeModel("gemini-3-flash-preview")

            # Prompt based on option
            if option == "Hints":
                prompt = """
                Analyze this screenshot of code error.
                Give ONLY hints to fix the issue.
                Do NOT provide full solution code.
                """
            else:
                prompt = """
                Analyze this screenshot of code error.
                Explain the error clearly and provide the correct fixed code step by step.
                """

            # Generate response
            response = model.generate_content([prompt, image])

            # Display result
            st.markdown("## 🧠 Result")
            st.markdown(response.text)
