from transformers import AutoTokenizer, AutoModel
from .providers import call_method

class CallLLM():
    def __init__(self, model_path='chatgpt', cuda='0'):
        if model_path in call_method:
            self.func = call_method[model_path]
            return
        
        model = AutoModel.from_pretrained(model_path, trust_remote_code=True, device=f'cuda:{cuda}')
        self.cuda = cuda
        self.tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        self.model = model.eval()
        self.func = self.call_pretrain_model
    
    def call_pretrain_model(self, query: str, sample_times: int=1):        
        def chatglm3_base_template(query, history=None, system=None):
            prompt = f'Q: {query}\n\nA: '
            return prompt
        
        def model_chat(prompt: str):  # unused
            output, updated_history = self.model.chat(self.tokenizer, prompt, history=None)
            return output
        
        def generation(prompt: str, sample_times: int=1):
            print("in-llms/call.py: generation()")
            input_ids = self.tokenizer.encode(
                text=prompt,
                return_tensors='pt',
                max_length=8192,
                truncation=False
            ).to(f'cuda:{self.cuda}')

            print("len(input_ids[0])", len(input_ids[0]))
            if len(input_ids[0]) > 7500:
                return ''
            
            output_ids = self.model.generate(
                input_ids=input_ids,
                max_new_tokens=1024,
                do_sample=True, # 随机采样：生成的 token 是从概率分布中采样，而不是选择概率最高的 token
                top_p=0.7, # Nucleus Sampling避免极端token,只选择累积概率达到 70% 的最有可能的 token
                temperature=0.7, # 控制生成文本的随机性 -> 降低随机性？ # laj: 0.95 -> 0.7
                num_return_sequences=sample_times
            )
            
            output_text_list = []
            for i in range(sample_times):
                output_text = self.tokenizer.decode(output_ids[i], skip_special_tokens=True)
                output_text = output_text.split('A: ')[-1]
                output_text_list.append(output_text)
            
            output = output_text_list[0]
            # # laj debug:
            # # clean the several "`" before the output
            # while output.startswith('`'):
            #     output = output[1:]
            # # clean the several "`" after the output
            # while output.endswith('`'):
            #     output = output[:-1]
            return output
        
        prompt = chatglm3_base_template(query)
        output = generation(prompt)
        # output = model_chat(prompt)
        print('[Model]', output)
        return output
    
    def model_call(self, prompt):
        output = self.func(prompt)  # Eventually goes to call_pretrain_model(16)
        return output  # back main.py -> res = asyncio.run(self.llm.model_call(prompt))
