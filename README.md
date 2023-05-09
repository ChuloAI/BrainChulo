# BrainChulo: Harnessing the Memory Power of the Camelids

BrainChulo is a powerful memory management system that is inspired by the camel family's resilience and adaptability. The repository contains a custom LLM (Long-Term Memory) implementation that is based on a trained model called Vicuna, and is designed to help users store and retrieve memories for use in their Vicuna-powered LLM services.

## Current Look-n-Feel
<img width="465" alt="image" src="https://user-images.githubusercontent.com/95258328/235260559-650cfb84-a77d-45af-94c4-ac829d7621f5.png">

## Features

- Custom LLM implementation based on the Vicuna model
- Memory retrieval algorithms for quick recall
- Easy-to-use interface for storing and managing memories
- Integration with other memory systems for seamless data transfer

## Installation

To use BrainChulo, simply clone the repository to your local machine and install the required dependencies:

```bash
git clone https://github.com/your-username/BrainChulo.git
cd BrainChulo
pip install -r requirements.txt

```

Note that you will need to be running your own Vicuna model in API mode and ensure your `.env` file is setup properly. See [.env.example](.env.example). Please refer to [Oobabooga Text Generation WebUI](https://github.com/oobabooga/text-generation-webui) for more information.

Additionally, a highly-inspired from Oobabooga's repo `download-model.py` has been made available to help you download the model.

## Usage

### Oobabooga Text Generation WebUI

Make sure to navigate to your installation directory of Oobabooga's Text Generation WebUI, then start the web server using `--api`. In my case, this is the command I run:

```bash
python server.py --model TheBloke_vicuna-7B-1.1-GPTQ-4bit-128g --wbits 4 --groupsize 128 --verbose --model_type llama --xformers --api
```

You may be running it via `start_webui.bat`. In this case, you'll need to edit it to include the two parameters mentioned above.

### BrainChulo

To start BrainChulo, simply run the `main.py` script at the root of this repository:

```
python main.py
```


This will eventually launch the BrainChulo application. Point your web browser to the following default URL:

```
http://localhost:7865/
```

This interface allows you to chat or load text documents which will be used as context in the BrainChulo application.

### &#9888; WARNING &#9888;
As we develop BrainChulo the application is gaining abilities which allow it to access and change files on the filesystem. This is a major security risk. We strongly recommend that you run BrainChulo in a Docker container, using the provided `Dockerfile`.

To run BrainChulo in a Docker container, you just need to run:

`docker-compose up`

To shut down the container:

`docker-compose down`


## Roadmap

Here's a detailed roadmap for the BrainChulo project:

1. **Create an End-to-End capable of creating, persisting, and using an index which can be loaded as context to a conversation using `langchain memory` module or `llama-index` package.** This will allow the agent to maintain context and continuity between conversations and ensure that information is not lost over time.

2. **Implement a Long-Term Memory (LTM) mechanism using a Vector Database layer with fine-tuning/training capabilities for LTM Management.** This will allow the agent to remember past conversations and information for longer periods of time, and provide a more personalized experience to the user.

3. **Implement Tools for the agent (ability to browse the web, send a tweet, read a file, use the REPL).** These tools will enable the agent to perform various tasks and make it more versatile.

4. **Create an Integration point for external systems.** This will allow other systems to interact with the BrainChulo agent and expand its capabilities.

5. **Integrate into existing Text Generation Systems such as oobabooga and Kobold.** This will enable the BrainChulo agent to work with other text generation systems and provide a wider range of outputs to the user.

Please note that this roadmap is subject to change based on community feedback and contributions. We welcome your input and ideas as we work together to add long-term memory to custom LLMs!



## Contributing

We welcome contributions to BrainChulo from the open source community! If you would like to contribute to the project, please fork the repository and submit a pull request. For more information on how to contribute, please see the [CONTRIBUTING.md](CONTRIBUTING.md) file.


<a href="https://discord.gg/9prDPY2rpU" target="_blank" title="Join us on Discord"><img src="https://user-images.githubusercontent.com/95258328/235766839-47336cbb-f338-4939-b2ec-b33363020f95.png" width="150" alt="Join BrainChulo on Discord" /></a>

## License
BrainChulo is licensed under the MIT license. See [LICENSE.md](LICENSE.md) for more information.


## Notes for developers
More commands are available on Docker. They are not necessary but can help developers
Build the Docker image: 

`docker build -t brainchulo .`

Run the Docker container: 

`docker run -p 7865:7865 --name brainchulo brainchulo`


If you wish to mount the BrainChulo local repository to the running container, run the following command:

`docker run -p 7865:7865 -v /path/to/local/code:/app brainchulo`

If you want hot reloading when coding, start the app with the following command:
```
gradio main.py
```