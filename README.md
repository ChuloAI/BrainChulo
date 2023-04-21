# BrainChulo: Harnessing the Memory Power of the Camelids

BrainChulo is a powerful memory management system that is inspired by the camel family's resilience and adaptability. The repository contains a custom LLM (Long-Term Memory) implementation that is based on a trained model called Vicuna, and is designed to help users store and retrieve memories for use in their Vicuna-powered LLM services.


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

Note that you will need to be running your own Vicuna model in API mode and ensure your `.env` file is setup properly. See [.env-example](.env-example). Please refer to [Oobabooga Text Generation WebUI](https://github.com/oobabooga/text-generation-webui) for more information.

Additionally, a highly-inspired from Oobabooga's repo `download-model.py` has been made available to help you download the model.

## Usage

To start using BrainChulo, simply run the `main.py` script:

```
python main.py
```

This will launch the BrainChulo interface, where you can start storing and retrieving memories. For more information on how to use BrainChulo, please refer to the documentation.

## Contributing

We welcome contributions to BrainChulo from the open source community! If you would like to contribute to the project, please fork the repository and submit a pull request. For more information on how to contribute, please see the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## License
BrainChulo is licensed under the MIT license. See [LICENSE.md](LICENSE.md) for more information.
