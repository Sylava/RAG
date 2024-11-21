# AI RAG project

Language used: Python

**RAG** is a way to enhance the capabilities of LLMs by combining their powerful language understanding with targeted retrieval of relevant information from external sources often with using embeddings in vector databases, leading to more accurate, trustworthy, and versatile AI-powered applications

## Pre-requirement:

You need to have **Ollama** installed https://ollama.com/download.
This project uses Llama 3.2 but feel free to change the model at will.

## How to run:

### **Launch the project with RAG :**

```bash
make start
```

Upload pdf file from AWS S3 Bucket using boto3 library and store the content in text.text

_Optional:_
You can see the content of text.txt using

```bash
cat text.txt
```

You can take a coffee when it's pulling, it might take some time ☕
