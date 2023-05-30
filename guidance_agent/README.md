# Custom Guidance Server with LangChain Integration



The project primarily focuses on integrating the Guidance and LangChain libraries to offer a solution for querying and understanding documentation with the help of AI. A Flask server is set up that utilizes Oobabooga, LangChain, and Chroma vector store for intelligent retrieval and responses.



## Project Structure


constants.py

This file defines several important constants used in the project. The constants defined include:

    EMB_OPENAI_ADA: Specifies the embedding model name for OpenAI Ada.
    EMB_INSTRUCTOR_XL: Specifies the embedding model name for Instructor XL.
    LLM_OPENAI_GPT35: Specifies the language model name for OpenAI GPT-3.5.
    OOBA: A string constant.
    TEST_FILE: Specifies the path to a test file.
    MODEL: Specifies the path to the custom model.

These constants are used throughout the code, especially in tools.py where the tools are defined and loaded.
Installation

Before running the server, ensure the following Python libraries are installed:

    Flask
    Flask-CORS
    nest_asyncio
    dotenv
    gradio
    guidance
    torch
    LangChain
    Chroma

You can install the dependencies using pip:

bash

pip install -r requirements.txt


Make also sure you have text-generation-webui running in the background with arguments as such: python server.py --listen --model your-model  --api  --verbose  --xformers  --no-stream


## Running the Server

    Load the model using the '/load_model' POST endpoint. The model loads into memory on startup.
    Load the tools using the '/load_tools' POST endpoint. It checks if the model is loaded before loading the tools.
    Use the '/run_script' POST endpoint to run the script. It checks if the tools are loaded before running the script.

To start the server, use the following command:

python gdc_server.py

This will start a Flask server listening on 0.0.0.0:5001.



## Customization

The CustomAgentGuidance class is defined in the agent.py file. This class can be customized to provide different behaviors for guidance.

In tools.py, a dictionary of tool functions can be loaded for use in the server. Each tool should be a function that takes an input and returns an output. The Chroma Search tool is provided as an example.

The server script (gdc_server.py) is set up to load a custom model and toolset, and then provide guidance based on those. The loaded model and toolset can be customized as needed.



## Interconnection of Guidance and LangChain

This project's key feature is the combination of the Guidance and LangChain libraries. It loads a model using the Guidance library and then uses LangChain to set up a document retrieval system.

This system is based on a Chroma vector store, which indexes and retrieves documents using AI embeddings. This allows for complex queries to be run on large amounts of documentation, with the AI providing intelligent, context-based answers.

The server offers a '/run_script' endpoint to make queries against this document retrieval system and obtain AI-guided responses.



## Known Issues

If you encounter an issue where the event loop is already running, you can solve this problem by calling nest_asyncio.apply().
