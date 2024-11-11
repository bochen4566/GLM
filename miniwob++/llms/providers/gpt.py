from openai import OpenAI
import os
import requests

async def call_gpt(model, prompt, history=None, system=None):
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


# async def call_gpt(model, prompt, history=None, system=None):
#     if "OPENAI_API_KEY" not in os.environ:
#         raise ValueError(
#             "OPENAI_API_KEY environment variable must be set when using OpenAI API."
#         )
    
#     client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    
#     messages = []
#     if system:
#         messages.append({
#             "role": "system",
#             "content": system
#         })
    
#     if history:
#         for chat in history:
#             messages.append({
#                 "role": "user",
#                 "content": chat[0]
#             })
#             messages.append({
#                 "role": "assistant",
#                 "content": chat[1]
#             })
    
#     messages.append({
#         "role": "user",
#         "content": prompt
#     })

#     response = client.chat.completions.create(
#         model="gpt-4o",
#         messages=messages,
#         timeout=1000
#     )

#     return response.choices[0].message.content