import sys
import os
import subprocess

DEFAULT_EMBEDDINGS_MODEL ="sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_MODEL = "TheBloke/wizardLM-7B-GPTQ"
MODEL_DIR = "./models"


def _download_if_not_exists(model):
    models_dir = os.path.join(MODEL_DIR, model)
    if os.path.exists(models_dir):
        print(f"Directory {models_dir} already exists! Skpping download!")

    else:
        print(f"Downloading model {model} to {models_dir}")
        print("Please note that if model is large this may take a while.")
        process = subprocess.run(["python3",  "download-model.py", model, "--output", MODEL_DIR], capture_output=True)
        process.check_returncode()


def main(model, embeddings_model):
    print(f"""Your choices:
MODEL: {model}
EMBEDDINGS MODEL: {embeddings_model}
""")
    try:
        os.mkdir(MODEL_DIR)
    except FileExistsError:
        pass

    _download_if_not_exists(embeddings_model)
    _download_if_not_exists(model)
    print("Success!")

if __name__ == "__main__":
    model = None
    embeddings = None
    
    if len(sys.argv) > 2:
        embeddings = sys.argv[2]

    if len(sys.argv) > 1:
        model = sys.argv[1]

    if len(sys.argv) == 1:
        print(
            "NOTE: You can change the default downloaded model by passing an additional argument:"
            + f"{sys.argv[0]} [hugging-face-llm-model-name] [hugging-face-embeddings-model-name]"
        )

    if not embeddings:
        embeddings = DEFAULT_EMBEDDINGS_MODEL
    
    if not model:
        model = DEFAULT_MODEL

    main(model, embeddings)