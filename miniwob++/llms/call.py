from transformers import AutoTokenizer, AutoModel
from .providers import call_method
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import os
import torch

class CallLLM():
    def __init__(self, model_path, cuda='0'):
        self.cuda = cuda
        self.model_path = model_path
        
        # Initialize the model and tokenizer based on model_path
        if "llama" in model_path.lower():
            # Load Llama model and tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.float16).to(f'cuda:{self.cuda}').eval()
            self.model_type = "llama"
        elif "chatglm" in model_path.lower():
            # Load ChatGLM model and tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
            self.model = AutoModel.from_pretrained(model_path, trust_remote_code=True).half().to(f'cuda:{self.cuda}').eval()
            self.model_type = "chatglm"
        else:
            raise ValueError("Model not supported. Please use 'llama' or 'chatglm' models.")
        
        self.func = self.call_pretrain_model
    
    def call_pretrain_model(self, query: str, sample_times: int=1):        
        def base_template(query, history=None, system=None):
            prompt = f'Q: {query}\n\nA: '
            return prompt
        
        def model_chat(prompt: str):
            # Use chat method for ChatGLM
            output, updated_history = self.model.chat(self.tokenizer, prompt, history=None)
            return output
        
        def generation(prompt: str, sample_times: int=1):
            # Encode the prompt
            input_ids = self.tokenizer.encode(
                text=prompt,
                return_tensors='pt',
                max_length=8192,
                truncation=True
            ).to(f'cuda:{self.cuda}')

            if len(input_ids[0]) > 7500:
                return ''
            
            # Generate output based on model type
            if self.model_type == "llama":
                # Generate response for Llama
                output_ids = self.model.generate(
                    input_ids=input_ids,
                    max_new_tokens=1024,
                    do_sample=True,
                    top_p=0.7,
                    temperature=0.95,
                    num_return_sequences=sample_times
                )
                output_text_list = []
                for i in range(sample_times):
                    output_text = self.tokenizer.decode(output_ids[i], skip_special_tokens=True)
                    output_text = output_text.split('A: ')[-1]
                    output_text_list.append(output_text)
                output = output_text_list[0]
            
            elif self.model_type == "chatglm":
                # Use ChatGLM chat method
                output = model_chat(prompt)
            
            return output
        
        prompt = base_template(query)
        output = generation(prompt)
        output = output.splitlines()[0].strip() if output else output
        print('[Model]', output)
        return output
    
    def model_call(self, prompt):
        output = self.func(prompt)
        return output


# class CallLLM():
#     def __init__(self, model_path, cuda='0'):
#         self.model_name = model_path
#         self.cuda = cuda
        
#         if model_path in call_method:
#             self.func = call_method[model_path]
#             return
        
#         model = AutoModel.from_pretrained(model_path, trust_remote_code=True, device=f'cuda:{cuda}')
#         self.cuda = cuda
#         self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
#         self.model = model.eval()
#         self.func = self.call_pretrain_model
    
#     def call_pretrain_model(self, query: str, sample_times: int=1):        
#         def chatglm3_base_template(query, history=None, system=None):
#             prompt = f'Q: {query}\n\nA: '
#             return prompt
        
#         def model_chat(prompt: str):
#             output, updated_history = self.model.chat(self.tokenizer, prompt, history=None)
#             return output
        
#         def generation(prompt: str, sample_times: int=1):
#             input_ids = self.tokenizer.encode(
#                 text=prompt,
#                 return_tensors='pt',
#                 max_length=8192,
#                 truncation=False
#             ).to(f'cuda:{self.cuda}')

#             if len(input_ids[0]) > 7500:
#                 return ''
            
#             output_ids = self.model.generate(
#                 input_ids=input_ids,
#                 max_new_tokens=1024,
#                 do_sample=True,
#                 top_p=0.7,
#                 temperature=0.95,
#                 num_return_sequences=sample_times
#             )
            
#             output_text_list = []
#             for i in range(sample_times):
#                 output_text = self.tokenizer.decode(output_ids[i], skip_special_tokens=True)
#                 output_text = output_text.split('A: ')[-1]
#                 output_text_list.append(output_text)
            
#             output = output_text_list[0]
#             return output
        
#         prompt = chatglm3_base_template(query)
#         output = generation(prompt)
#         # output = model_chat(prompt)
#         print('[Model]', output)
#         return output
    
#     def model_call(self, prompt):
#         output = self.func(prompt)
#         return output
#     # async def model_call(self, prompt):
#     #     if self.func == call_llama:
#     #         output = await self.func(self.model_name, prompt)
#     #     else:
#     #         output = self.func(prompt)
#     #     print('[Model]', output)
#     #     return output