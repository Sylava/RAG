# AI RAG project

Language used: Python

**RAG** is a way to enhance the capabilities of LLMs by combining their powerful language understanding with targeted retrieval of relevant information from external sources often with using embeddings in vector databases, leading to more accurate, trustworthy, and versatile AI-powered applications

## How to run:

### **Launch the project with RAG :**

```bash
make rag
```

Upload pdf file from AWS S3 Bucket using boto3 library and store the content in text.text

_Optional:_
You can see the content of text.txt using

```bash
cat text.txt
```

### **Launch the project without RAG (Ollama only)**

```bash
make ragless
```

Open Llama3.2 chatbot.
If it doesn't work properly, download the Llama3.2 model using

```bash
ollama pull llama3.2
```

You can take a coffee when it's pulling, it might take some time ☕
