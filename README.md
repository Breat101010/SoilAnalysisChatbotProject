# Zimbabwe Soil Analysis Chatbot

This is an AI-powered chatbot designed to provide helpful information and advice on soil analysis, crop requirements, and farming practices specific to Zimbabwe. It utilizes Google's Gemini AI model and a custom knowledge base compiled from relevant agricultural resources.

## Features

* Provides information on Zimbabwean soil types and their characteristics.
* Offers guidance on common crops grown in Zimbabwe and their nutrient needs.
* Explains relevant agricultural practices and addresses common soil fertility issues.
* Leverages Retrieval Augmented Generation (RAG) to provide context-aware responses.

## Getting Started

Follow these steps to set up and run the chatbot on your local machine.

### Prerequisites

Before you begin, ensure you have the following installed:

* **Python 3.8+:** Download from [python.org](https://www.python.org/downloads/). During installation on Windows, make sure to check "Add Python to PATH".
* **Git:** Download from [git-scm.com](https://git-scm.com/downloads).
* **Google Gemini API Key:**
    * Go to [Google AI Studio](https://ai.google.dev/).
    * Sign in with your Google account.
    * Generate a new API key.
    * **Keep this key secure and do NOT share it publicly.**

### Installation and Setup

1.  **Clone the Repository:**
    Open your Command Prompt (CMD) or Terminal and navigate to the directory where you want to save the project. Then, clone this repository:
    ```bash
    git clone [https://github.com/YourUsername/SoilChatbotProject.git](https://github.com/YourUsername/SoilChatbotProject.git)
    ```
    (Replace `YourUsername` with your actual GitHub username, and `SoilChatbotProject.git` with your repo's correct URL).

2.  **Navigate to the Project Directory:**
    ```bash
    cd SoilChatbotProject
    ```

3.  **Create a Python Virtual Environment:**
    It's highly recommended to use a virtual environment to manage dependencies.
    ```bash
    python -m venv venv
    ```

4.  **Activate the Virtual Environment:**
    * **Windows (Command Prompt):**
        ```bash
        .\venv\Scripts\activate
        ```
    * **macOS/Linux (Terminal):**
        ```bash
        source venv/bin/activate
        ```
    (You should see `(venv)` at the beginning of your terminal prompt once activated.)

5.  **Install Required Python Packages:**
    With your virtual environment activated, install the Google Generative AI SDK:
    ```bash
    pip install -q -U google-generativeai
    ```

6.  **Set Your Gemini API Key:**
    You need to set your API key as an environment variable for the chatbot to access it. **Replace `YOUR_ACTUAL_API_KEY_HERE` with the key you generated from Google AI Studio.**

    * **Windows (Command Prompt):**
        ```bash
        set GOOGLE_API_KEY=YOUR_ACTUAL_API_KEY_HERE
        ```
    * **macOS/Linux (Terminal):**
        ```bash
        export GOOGLE_API_KEY="YOUR_ACTUAL_API_KEY_HERE"
        ```
    **Important:** This command needs to be run every time you open a new terminal session to use the chatbot.

### Running the Chatbot

With your virtual environment activated and API key set, you can run the chatbot:

```bash
python soil_chatbot.py


### How to Use
Once the chatbot starts, type your questions or soil parameters related to agriculture in Zimbabwe. Examples:

What is the ideal pH for maize in Zimbabwe?

My soil has low nitrogen, what should I do for groundnuts?

Tell me about common soil types in Zimbabwe.

What are conservation agriculture practices?

What are the symptoms of phosphorus deficiency?

What fertilizer is good for cotton?

Type exit to quit the chatbot.
