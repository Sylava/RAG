.PHONY: start

start:
	touch text.txt
	@if [ ! -d ".venv" ]; then \
		python3 -m venv .venv; \
	fi
	. .venv/bin/activate && \
	pip install tiktoken boto3 pdfplumber openai langchain chainlit langchain-community && \
	python3 upload.py
	#python3 localrag.py
