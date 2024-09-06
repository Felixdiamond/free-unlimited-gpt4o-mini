# Free Unlimited GPT-4o mini API

## Overview

Why pay for GPT-3.5 API when you can just self host a GPT-4o-mini?

This project provides a simple web API to interact with openAI gpt4o-mini trial though browser automation. The API is built with FastAPI and nodriver (the package that made it all come together) and allows users to send prompts and receive completions from a web-based GPT model.

The core functionality is implemented in `main.py`, which handles interactions with the gpt4o-mini web interface. The FastAPI server is set up in `server.py`, exposing an endpoint for prompt completions.

## Setup

### Prerequisites

Make sure you have Python 3.7 or later installed. You also need to install the necessary Python packages.

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Felixdiamond/free-unlimited-gpt4o-mini.git
    cd free-unlimited-gpt4o-mini
    ```

2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

### Running the Server

1. Start the FastAPI server by running `server.py`:

    ```bash
    python server.py
    ```

2. The server will start at `http://localhost:8000`. You can interact with it via the `/complete/` endpoint.

### Running through terminal

1. Run the script:
```bash
python main.py
```

2. Follow the prompts from the script

### Using the API

To get a completion, send a POST request to `http://localhost:8000/complete/` with a JSON body that includes the prompt. 

Example request:

```bash
curl -X POST "http://localhost:8000/complete/" -H "Content-Type: application/json" -d '{"prompt": "What is the meaning of life?"}'
```

### Limitations
- Low context history (7 messages tops)

### Contributions
You can contribute if you see any meaning in this ¯\_(ツ)_/¯