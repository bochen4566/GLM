import requests
import asyncio



async def generate_text(model, prompt, history=None, system=None):
    API_URL = "http://127.0.0.1:1234"
    messages = []
    
    # Add system message if provided
    if system:
        messages.append({
            "role": "system",
            "content": system
        })
    
    # Add chat history if provided
    if history:
        for chat in history:
            messages.append({
                "role": "user",
                "content": chat[0]
            })
            messages.append({
                "role": "assistant",
                "content": chat[1]
            })
    
    # Add current user prompt
    messages.append({
        "role": "user",
        "content": prompt
    })
    
    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 100
    }
    
    response = requests.post(f"{API_URL}/v1/chat/completions", json=data)
    
    return response.json()["choices"][0]["message"]["content"]


# if __name__ == "__main__":
#     system_prompt = "You are a helpful assistant that provides clear and concise answers."
#     chat_history = [
#         ("What's the weather like?", "I don't have access to current weather information."),
#         ("Who are you?", "I'm an AI assistant.")
#     ]
#     user_prompt = "What is the capital of France?"
    
#     # Run the async function
#     response = asyncio.run(generate_text(
#         model="your-model-name",
#         prompt=user_prompt,
#         history=chat_history,
#         system=system_prompt
#     ))
#     print(response)