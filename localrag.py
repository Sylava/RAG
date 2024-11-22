import torch
import ollama
import os
import json
import argparse
import logging
from openai import OpenAI

# ANSI escape codes for colors
PINK = '\033[95m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
NEON_GREEN = '\033[92m'
RESET_COLOR = '\033[0m'

# Configure logging
logging.basicConfig(level=logging.INFO)

def open_file(filepath: str) -> str:
    """Open a file and return its contents as a string  ."""
    try:
        with open(filepath, 'r', encoding='utf-8') as infile:
            return infile.read()
    except Exception as e:
        logging.error(f"Error reading file {filepath}: {e}")
        return ""

def get_relevant_context(rewritten_input: str, vault_embeddings: torch.Tensor, vault_content: list, top_k: int = 3) -> list:
    """Get relevant context from the vault based on user input."""
    if vault_embeddings.nelement() == 0:
        return []
    
    input_embedding = ollama.embeddings(model='mxbai-embed-large', prompt=rewritten_input)["embedding"]
    if not input_embedding or len(input_embedding) == 0:
        logging.error("Generated input embedding is empty.")
        return []
    cos_scores = torch.cosine_similarity(torch.tensor(input_embedding).unsqueeze(0), vault_embeddings)
    top_k = min(top_k, len(cos_scores))
    top_indices = torch.topk(cos_scores, k=top_k)[1].tolist()
    
    return [vault_content[idx].strip() for idx in top_indices]

def rewrite_query(user_input_json: str, conversation_history: list, ollama_model: str, client) -> str:
    """Rewrite the user's query using conversation history."""
    user_input = json.loads(user_input_json)["Query"]
    context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history[-2:]])
    
    prompt = f"""Rewrite the following query by incorporating relevant context from the conversation history.
    The rewritten query should:
    - Preserve the core intent and meaning of the original query
    - Expand and clarify the query to make it more specific and informative for retrieving relevant context
    - Avoid introducing new topics or queries that deviate from the original query
    - DONT EVER ANSWER the Original query, but instead focus on rephrasing and expanding it into a new query
    
    Return ONLY the rewritten query text, without any additional formatting or explanations.
    
    Conversation History:
    {context}
    
    Original query: [{user_input}]
    
    Rewritten query: [{user_input_json}]
    """
    
    response = client.chat.completions.create(
        model=ollama_model,
        messages=[{"role": "system", "content": prompt}],
        max_tokens=200,
        n=1,
        temperature=0.1,
    )
    
    return json.dumps({"Rewritten Query": response.choices[0].message.content.strip()})

def ollama_chat(user_input: str, system_message: str, vault_embeddings: torch.Tensor, vault_content: list, ollama_model: str, conversation_history: list, top_k: int, client) -> str:
    """Handle the chat logic with the Ollama model."""
    conversation_history.append({"role": "user", "content": user_input})
    
    rewritten_query = user_input
    if len(conversation_history) > 1:
        query_json = {"Query": user_input, "Rewritten Query": ""}
        rewritten_query_json = rewrite_query(json.dumps(query_json), conversation_history, ollama_model, client)
        rewritten_query_data = json.loads(rewritten_query_json)
        rewritten_query = rewritten_query_data["Rewritten Query"]
        logging.info(f"{PINK}Original Query: {user_input}{RESET_COLOR}")
        logging.info(f"{PINK}Rewritten Query: {rewritten_query}{RESET_COLOR}")
    
    relevant_context = get_relevant_context(rewritten_query, vault_embeddings, vault_content, top_k)
    if relevant_context:
        context_str = "\n".join(relevant_context)
        logging.info("Context Pulled from Documents: \n\n" + CYAN + context_str + RESET_COLOR)
    else:
        logging.info(CYAN + "No relevant context found." + RESET_COLOR)
    
    user_input_with_context = user_input
    if relevant_context:
        user_input_with_context += "\n\nRelevant Context:\n" + context_str
    
    conversation_history[-1]["content"] = user_input_with_context
    
    messages = [{"role": "system", "content": system_message}, *conversation_history]
    
    response = client.chat.completions.create(
        model=ollama_model,
        messages=messages,
        max_tokens=2000,
    )
    
    conversation_history.append({"role": "assistant", "content": response.choices[0].message.content})
    
    return response.choices[0].message.content

def main():
    """Main function to run the Ollama chat application."""
    parser = argparse.ArgumentParser(description="Ollama Chat")
    parser.add_argument("--model", default="llama3.2", help="Ollama model to use (default: llama3.2)")
    parser.add_argument("--top_k", type=int, default=3, help="Number of top contexts to retrieve (default: 3)")
    args = parser.parse_args()

    logging.info(NEON_GREEN + "Initializing Ollama API client..." + RESET_COLOR)
    client = OpenAI(
        base_url='http://localhost:11434/v1',
        api_key='llama3.2'
    )

    logging.info(NEON_GREEN + "Loading vault content..." + RESET_COLOR)
    vault_content = open_file("text.txt").splitlines()

    logging.info(NEON_GREEN + "Generating embeddings for the vault content..." + RESET_COLOR)
    vault_embeddings = []

    for content in vault_content:
        response = ollama.embeddings(model='mxbai-embed-large', prompt=content)
        embedding = response.get("embedding")
        if embedding is None or len(embedding) == 0:
            logging.warning(f"No embedding generated for content: {content}")
        else:
            vault_embeddings.append(embedding)

    vault_embeddings_tensor = torch.tensor(vault_embeddings)
    logging.info("Embeddings for each line in the vault generated.")

    logging.info("Starting conversation loop...")
    conversation_history = []
    system_message = "You are a helpful assistant that is an expert at extracting the most useful information from a given text. Also bring in extra relevant information to the user query from outside the given context."

    while True:
        user_input = input(YELLOW + "Ask a query about your documents (or type 'quit' to exit): " + RESET_COLOR)
        if user_input.lower() == 'quit':
            logging.info("Exiting the chat application.")
            break
        
        response = ollama_chat(user_input, system_message, vault_embeddings_tensor, vault_content, args.model, conversation_history, args.top_k, client)
        logging.info(NEON_GREEN + "Response: \n\n" + response + RESET_COLOR)

if __name__ == "__main__":
    main()