from openai import OpenAI
import os

async def call_gpt(model, prompt, history=None, system=None):
    if "OPENAI_API_KEY" not in os.environ:
        raise ValueError(
            "OPENAI_API_KEY environment variable must be set when using OpenAI API."
        )
    
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    
    messages = []
    if system:
        messages.append({
            "role": "system",
            "content": system
        })
    
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
    
    messages.append({
        "role": "user",
        "content": prompt
    })

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        timeout=1000
    )

    return response.choices[0].message.content