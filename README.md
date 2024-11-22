# AI RAG project

Language used: Python

**RAG** is a way to enhance the capabilities of LLMs by combining their powerful language understanding with targeted retrieval of relevant information from external sources often with using embeddings in vector databases, leading to more accurate, trustworthy, and versatile AI-powered applications

## How to run:

### **Launch the project with RAG :**

**Install the dependencies for the project**

```bash
make install
```

Upload pdf file from AWS S3 Bucket using boto3 library and store the content in text.txt. Install all the Python dependencies
You can take a coffee when it's pulling, it might take some time ☕

_Optional:_
You can see the content of text.txt using

```bash
cat text.txt
```

**Run the project**

```bash
make start
```

Starts the chatbot where you can write your questions about the uploaded file from S3.
In this example, we are using a PDF file about coffee.

> [!IMPORTANT]
> Queries about other subject might return an inacurrate answer

**Clean the temp files**

```bash
make clean
```

Clean the text.txt
