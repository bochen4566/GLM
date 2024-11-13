from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

async def call_llama(model_name, prompt, history=None, system=None):
    
    # Set up the model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    llm_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer, device=0 if torch.cuda.is_available() else -1)

    # Construct the conversation prompt
    conversation = ""
    if system:
        conversation += f"System: {system}\n"
    
    if history:
        for user_msg, assistant_msg in history:
            conversation += f"User: {user_msg}\nAssistant: {assistant_msg}\n"
    
    conversation += f"User: {prompt}\nAssistant:"

    # Generate response
    response = llm_pipeline(conversation, max_length=1000, num_return_sequences=1, do_sample=True)[0]['generated_text']

    # Extract only the assistant's response after "Assistant:"
    assistant_response = response.split("Assistant:")[-1].strip()

    return assistant_response