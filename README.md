# AI Chat Application

This is an AI chat application built using Streamlit and Google Generative AI. It allows users to interact with various AI models provided by Google AI.

## Features

- **Model Selection:** Choose from multiple AI models.
- **Advanced Settings:** Adjust parameters like temperature, top_k, top_p, and max_output_tokens.
- **Live Chat:** Engage in real-time conversations with the AI.
- **Copy Responses:** Easily copy AI responses to the clipboard.
- **Stop Generation:** Interrupt the AI response generation if needed.
- **Model Information:** Detailed descriptions of available models.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- [Google AI API Key](https://ai.google.com/studio)

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/ai-chat-app.git
    cd ai-chat-app
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Create a [.env](http://_vscodecontentref_/0) file in the project root directory and add your Google API key:
    ```env
    GOOGLE_API_KEY=your_google_api_key_here
    ```

4. If you want to use the application locally, uncomment the following lines in [main.py](http://_vscodecontentref_/1):
    ```python
    # import dotenv
    ```
    ```python
    # dotenv.load_dotenv()  # load from .env file
    ```

## Usage

You can use the application online with my personal Google AI Studio API at the following URL:
[https://ilpoppattuso.streamlit.app/](https://ilpoppattuso.streamlit.app/)

### Local Usage

1. Run the Streamlit application:
    ```sh
    streamlit run main.py
    ```

2. Open your web browser and navigate to `http://localhost:8501` to start interacting with the AI chat application.

## Configuration

### Sidebar Parameters

- **Temperature:** Controls the randomness of the output. Higher values make the output more creative and unpredictable, while lower values make it more deterministic and focused.
- **Top K:** Limits the sampling to the *k* most likely tokens. A value of 1 means that only the most likely token is selected (greedy sampling).
- **Top P:** Limits the sampling to tokens whose cumulative probability does not exceed *p*. This method, also called *nucleus sampling*, allows selecting from a variable number of tokens depending on the probability distribution.
- **Max Output Tokens:** Specifies the maximum number of tokens that the model can generate in the response.

## Models

- **Gemini 1.5 Flash:** Versatile model, balanced for various applications.
- **Gemini 2.0 Flash (exp):** Experimental version of Gemini 2.0, optimized for speed.
- **Gemini 2.0 Flash Thinking (exp):** Variant of Gemini 2.0, with an emphasis on reasoned responses.
- **1206 (exp):** Generic experimental model.
- **LearnLM 1.5 Pro (exp):** Model designed for learning and generating educational content.

## License

This application is released under the GNU General Public License (v3).

## Acknowledgments

This application was developed using the Google AI APIs and Streamlit. Special thanks to all the contributors who made this project possible.

## Feedback

If you have feedback or suggestions on how to improve this application, please let us know by opening an issue on GitHub or sending an email to [your_email@example.com].