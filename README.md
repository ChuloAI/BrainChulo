# BrainChulo: Harnessing the Memory Power of the Camelids

BrainChulo is a powerful Chat application with an emphasis on its memory management system. Our work is inspired by the camel family's resilience and adaptability. The repository contains a custom LTM (Long-Term Memory) approach for Llama-based LLMs (Large Language Models), and is designed to help users enhance their experience when using Open-Source LLMs.

## Current Look-n-Feel

![image](https://github.com/iGavroche/BrainChulo/assets/95258328/448c7b0e-1dbd-4ee7-9bfd-da66e2c7bf9c)


## Features

- Custom LTM implementation based on Open Source Large Language Models
- Memory retrieval algorithms for quick recall
- Easy-to-use interface for storing and managing memories
- Modern User Interface
- One-Shot, Few-Shot, and Tool-Capable Agents with Full Vector-Based Memory Integration
- Ability to handle multiple conversations
- Ability to upvote or downvote AI answers for fine-tuning

## Installation
**Update 06.06.2023** As of today, we're dropping support to [Oobabooga Text Generation WebUI](https://github.com/oobabooga/text-generation-webui). The reason being is it does not offer enough support for the (guidance library)[https://github.com/microsoft/guidance] features.

Currently, we only support standard Hugging Face models on GPU. They are loaded with 4-bit NormalFloat quantization (see more)[https://www.google.com/search?client=safari&rls=en&q=hugging+face+4bit+qlora&ie=UTF-8&oe=UTF-8]

According to the link above, the following models are supported with this 4-bit quantization method:

```json
[
    'bigbird_pegasus', 'blip_2', 'bloom', 'bridgetower', 'codegen', 'deit', 'esm', 
    'gpt2', 'gpt_bigcode', 'gpt_neo', 'gpt_neox', 'gpt_neox_japanese', 'gptj', 'gptsan_japanese', 
    'lilt', 'llama', 'longformer', 'longt5', 'luke', 'm2m_100', 'mbart', 'mega', 'mt5', 'nllb_moe', 
    'open_llama', 'opt', 'owlvit', 'plbart', 'roberta', 'roberta_prelayernorm', 'rwkv', 'switch_transformers', 
    't5', 'vilt', 'vit', 'vit_hybrid', 'whisper', 'xglm', 'xlm_roberta'
]
```
We plan to reintroduce CPU support back soon, through GGML / llamacpp-bindings - at least for the LLaMA models.

To use BrainChulo, there are three required steps.

### 1 - Install requirements (docker)

1. [Docker Engine](https://docs.docker.com/engine/)
2. [Docker Compose v2](https://docs.docker.com/compose/)
3. [nvidia-docker](https://github.com/NVIDIA/nvidia-docker)

If you want to use docker-compose v1, you might run into an issue with the port binding - though there's an easy workaround here:
https://github.com/ChuloAI/BrainChulo/issues/39


### 2 - Clone your desired model from Hugging Face
Choose a model that implements the Hugging Face API, if you're downloading them from TheBloke, typically they have the `-HF` suffix.

```bash
mkdir models
cd models
git clone https://huggingface.co/TheBloke/wizardLM-7B-HF
cd ..
```

Make sure the environment variable `MODEL_PATH` in `docker-compose.yaml` matches the path to your downloaded model:
```
    environment:
      MODEL_PATH: /models/wizardLM-7B-HF
```

Additionally, a highly-inspired from Oobabooga's repo `download-model.py` has been made available to help you download the model.


### 3 - Download, build and start Docker containers through the docker-compose
```
docker-compose up --build
```

## Usage
### BrainChulo
#### Starting the service
The easiest way to start BrainChulo is using Docker with `docker-compose`:

```
# from the root directory of the project, start with:
docker-compose up --build

# To shut it down
docker compose down

# After pulling the latest code, make sure to run the database migrations
docker-compose exec backend alembic upgrade head
```

## Creating a Plugin

1. Create a new directory for your plugin, e.g. `/app/plugins/my_plugin`

2. Inside the new directory, create a new Python module, e.g. `myplugin_main.py`

3. In `myplugin_main.py`, define your plugin routes using FastAPI. See the `/app/plugins/sample_plugin` directory for an example.

4. Create a `database.py` file to define your SQLModel models. Data for hese models will be persisted in the main database.

5. Once you have defined your models, run the following command **with your own message** to generate a new Alembic migration file. Migration files allow the application to add your models to the database schema:

```
alembic revision --autogenerate -m "Add Sample Plugin Demo Model"
```

6. Run `alembic upgrade head` to run your migration. This will update your database.

**Note:** If you wish to run these commands using the stood-up containers, prefix them as such:

```
# To create a migration
docker-compose exec backend alembic revision --autogenerate -m "Add Sample Plugin Demo Model"

# To run a migration
docker-compose exec backend alembic upgrade head
```


**Developers:** While you may use the container-based approach since it is a development container with hot reloading you may also wish to start BrainChulo's services manually. To do so, run the `main.py` script from within the `app` directory, then start the frontend:

```
cd ./app
python main.py

# if within the ./app directory
cd ../frontend
npm run dev
```


This will eventually launch the BrainChulo application. Point your web browser to the following default URL:

```
http://localhost:5173/
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

## Further resources

### Medium Articles

#### Introduction to Langchain
https://medium.com/@paolorechia/creating-my-first-ai-agent-with-vicuna-and-langchain-376ed77160e3
#### Q/A with Sentence Transformer + Vicuna
https://medium.com/@paolorechia/building-a-question-answer-bot-with-langchain-vicuna-and-sentence-transformers-b7f80428eadc
#### Fine tuning for Python REPL
https://medium.com/@paolorechia/fine-tuning-my-first-wizardlm-lora-ca75aa35363d
