miniwob_prompt = """<html> %s </html>

You are a helpful assistant that can assist with web navigation tasks.
You are given a simplified html webpage and a task description. 
Your goal is to complete the task. You can perform the specified operations below to interact with the webpage. You should only use the provided functions to interact with the webpage, and you should do one step at a time.
For each function, you should only use the provided arguments, you should only put the values of the arguments, and you should not add any other words.

#Valid operations: - #Click# id: Click on the element with the specified id.
- #Hover# id: Hover on the element with the specified id.
- #Scroll_up#: Scroll up 1 page.
- #Scroll_down#: Scroll down 1 page.
- #Type# id "text": Type in the text at the element with the specified id.

#Current viewport position: %s

#Previous Operation: %s

#Task: %s

Your output SHOULD be in the following format:
#Operation: {Next operation to perform}
"""

miniwob_prompt_with_tp = """<html> %s </html>

You are a helpful assistant that can assist with web navigation tasks.
You are given a simplified html webpage and a task description. 
Your goal is to complete the task. You can perform the specified operations below to interact with the webpage.
For each function, you should only use the provided arguments, you should only put the values of the arguments, and you should not add any other words.

#Valid operations: - #Click# id: Click on the element with the specified id.
- #Hover# id: Hover on the element with the specified id.
- #Scroll_up#: Scroll up 1 page.
- #Scroll_down#: Scroll down 1 page.
- #Type# id "text": Type in the text at the element with the specified id.

#Current viewport position: %s

#Previous Operation: %s

#Task: %s

Your output SHOULD be in the following format:
#Thinking Process: {Your thinking process to complete the task, including detailed analysis. For example, I have completed xxx and need to do xxx, so I need to perform xxx operation on the element <a[A]| xxx>}
#Operation: {Next operation to perform}
"""

miniwob_prompt_new_action_space = """<html> %s </html>

You are a helpful assistant that can assist with web navigation tasks.
You are given a simplified html webpage and a task description.
Your goal is to complete the task. You can use the provided functions below to interact with the current webpage.
For each function, you should only use the provided arguments, you should only put the values of the arguments, and you should not add any other words.
When date is present, you should select the datepicker and continue from there.

SAMPLE OUTPUT: (The function name should be all lowercase)
click("A")
hover("B")
type_string("C", "Yes", False)
...
Follow the functions formats exactly like below:
Determine yourself which functions you should use based on the current webpage and the previous operations if there is any.
#Provided sudo python3 functions:
def click(element_id: str) -> None:
    \"\"\"
    Click on the element with the specified id.

    Args:
       element_id: The id of the element.
    \"\"\"

def hover(element_id: str) -> None:
    \"\"\"
    Hover on the element with the specified id.

    Args:
       element_id: The id of the element.
    \"\"\"

def select(element_id: str, option: str) -> None:
 \"\"\"
    Select an option from a dropdown.

    Args:
       element_id: The id of the element.
       option: Value of the option to select.
 \"\"\"

def type_string(element_id: str, content: str, press_enter: bool) -> None:
 \"\"\"
    Type a string into the element with the specified id.

    Args:
       element_id: The id of the element.
       content: The string to type.
       press_enter: Whether to press enter after typing the string.
 \"\"\"

def scroll_page(direction: Literal['up', 'down']) -> None:
 \"\"\"
    Scroll down/up one page.

    Args:
       direction: The direction to scroll.
 \"\"\"

def go(direction: Literal['forward', 'backward']) -> None:
 \"\"\"
    Go forward/backward

    Args:
       direction: The direction to go to.
 \"\"\"

def jump_to(url: str, new_tab: bool) -> None:
 \"\"\"
    Jump to the specified url.

    Args:
       url: The url to jump to.
       new_tab: Whether to open the url in a new tab.
 \"\"\"

def switch_tab(tab_index: int) -> None:
 \"\"\"
    Switch to the specified tab.

    Args:
       tab_index: The index of the tab to switch to.
 \"\"\"

def user_input(message: str) -> str:
 \"\"\"
    Wait for user input.

    Args:
       message: The message to display to the user.

    Returns: The user input.
 \"\"\"

def finish(answer: Optional[str]) -> None:
 \"\"\"
    Finish the task (optionally with an answer).

    Args:
       answer: The answer to the task.
 \"\"\"

#Previous commands: %s

#Window tabs: 1. Default <-- current tab

#Current viewport (pages): %s

#Task: %s

You should output one command to interact to the currrent webpage. The output should consider the previous operations and the current webpage. For example, if you have already clicked on the element "A" and the current webpage has a text input option, you should type the required text in the text input using the type_string function.
"""
