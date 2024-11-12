from .configs import miniwob_prompt, miniwob_prompt_with_tp, miniwob_prompt_new_action_space

class ActionParser:
    operation_pattern = {
        'Click': r'(?s).*?#Click#\s*([A-Z]{1,3})',
        'Hover': r'(?s).*?#Hover#\s*([A-Z]{1,3})',
        'Scroll_up': r'(?s).*?#Scroll_up#',
        'Scroll_down': r'(?s).*?#Scroll_down#',
        'Type': r'(?s).*?#Type#\s*([A-Z]{1,3})\s*"{0,1}(.+)"{0,1}',
    }
    
    new_action_space_pattern = {
        'Click': r'(?s).*?click\([\'\"]([A-Za-z0-9-_]+)[\'\"](?:\s*\)|\s*,\s*.*\))',
        'Hover': r'(?s).*?hover\([\'\"]([A-Za-z0-9-_]+)[\'\"](?:\s*\)|\s*,\s*.*\))',
        'Scroll_up': r'(?s).*?scroll_page\([\'\"]up[\'\"](?:\s*\)|\s*,\s*.*\))',
        'Scroll_down': r'(?s).*?scroll_page\([\'\"]down[\'\"](?:\s*\)|\s*,\s*.*\))',
        'Type': r'(?s).*?type_string\([\'\"]([A-Za-z0-9-_]+)[\'\"],\s*[\'\"](.+)[\'\"](?:\s*,\s*(True|False)|,\s*press_enter\s*=\s*(True|False))\)',
    }
    
    prompts = {
        'basic': miniwob_prompt,
        'tp': miniwob_prompt_with_tp,
        'new_action_space': miniwob_prompt_new_action_space,
    }
    
    def __init__(self, prompt: str='basic') -> None:
        if prompt not in self.prompts:
            raise ValueError('Invalid prompt type.')
        
        funcs = {
            'basic': self.extract_operation,
            'tp': self.extract_operation_with_tp,
            'new_action_space': self.extract_operation_new_action_space,
        }
        
        self.prompt = self.prompts[prompt]
        self.func = funcs[prompt]
    
    def get_prompt(self) -> str:
        return self.prompt

    def extract(self, result: str='') -> (None, tuple):
        return self.func(result)
            
    @staticmethod
    def extract_operation(result: str='') -> (str, str):
        import re
        # match = re.search(r'#Operation:\s*(.+)', result)
        # if not match:
        #     return None
        # opstr = match.group(1)
        opstr = result
        
        for op, pattern in ActionParser.operation_pattern.items():
            match = re.search(pattern, opstr)
            if not match:
                continue
            param = match.groups()
            if op == 'Type':
                param.append(param[1])
            return '', op, param
            
        return None
    
    @staticmethod
    def extract_operation_with_tp(result: str='') -> (str, str):
        import re
        match = re.search(r'#Thinking Process:\s*(.+)\s*#Operation:\s*(.+)', result)
        if not match:
            return None
        tpstr = match.group(1)
        opstr = match.group(2)
        
        for op, pattern in ActionParser.operation_pattern.items():
            match = re.search(pattern, opstr)
            if not match:
                continue
            param = match.groups()
            if op == 'Type':
                param.append(False)
            return tpstr, op, match.groups()
            
        return None

    @staticmethod
    def extract_operation(result: str='') -> (str, str):
        import re
        # match = re.search(r'#Operation:\s*(.+)', result)
        # if not match:
        #     return None
        # opstr = match.group(1)
        opstr = result
        
        for op, pattern in ActionParser.operation_pattern.items():
            match = re.search(pattern, opstr)
            if not match:
                continue
            param = match.groups()
            if op == 'Type':
                param.append(False)
            return '', op, param
            
        return None
    
    @staticmethod
    def extract_operation_new_action_space(result: str='') -> (str, str):
        import re
        opstr = result
        print("--------------------------------here--------------------------------\n")
        print(opstr)
        for op, pattern in ActionParser.new_action_space_pattern.items():
            match = re.search(pattern, opstr)
            print(match)
            if not match:
                continue
            param = match.groups()
            if op == 'Type':
                if param[1] == 'True':
                    param[1] = True
                elif param[1] == 'False':
                    param[1] = False
                    
            return '', op, param
            
        return None