from llama_cpp import Llama
import os
from itertools import cycle
import threading
import time

# Function to list all model files in a directory
def list_model_files(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

# Directory containing the model files
model_directory = "C:\\Work\\AIModels"

# List all model files
model_files = list_model_files(model_directory)
print("Available models:")
for idx, model in enumerate(model_files, start=1):
    print(f"{idx}: {model}")

# Ask the user to select a model
selected_index = int(input("Enter the number of the model you want to use: ")) - 1
selected_model = model_files[selected_index]
model_path = os.path.join(model_directory, selected_model)

# Initialize the Llama model
llm = Llama(model_path=model_path, verbose=False, n_ctx=32768)

# Start an infinite loop to interact with the user
previous_prompt = ""
doContinue = False

progress_running = False

def show_progress_bar():
    for char in cycle("|/-\\"):
        if not progress_running:
            break
        print(f"\rThinking... {char}", end="", flush=True)
        time.sleep(0.1)
   


while True:
    if doContinue:
        revious_prompt += f" Continue:"
    else:
        user_input = input("\nEnter your question or type 'exit' to quit: ")
        if user_input.lower() == 'exit':
            break
        if (user_input.lower() == 'clear'):
            previous_prompt = ""
            continue
        previous_prompt += f"\nQ: {user_input}\nA:"

    progress_running = True 
    progress_thread = threading.Thread(target=show_progress_bar)
    progress_thread.start()

    response = llm(previous_prompt, max_tokens=1024)
    progress_running = False
    
    response_text = response['choices'][0]['text']
    print(response_text)
    
    doContinue = response['choices'][0]['finish_reason'] == 'length'
        

    previous_prompt += f" {response_text}"

