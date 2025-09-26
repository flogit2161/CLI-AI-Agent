import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    if len(sys.argv) < 2 :
        print('wrong usage, please try uv run main.py "prompt"')
        sys.exit(1)
    
    prompt = sys.argv[1]
    messages = [
        types.Content(role='user', parts=[types.Part(text=prompt)])
    ]
    verbose = '--verbose' in sys.argv[2:]
    
    generate_content(client, messages, verbose)


available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )
def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=messages, config = types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
    )
    func_call = response.function_calls
    if func_call:
        for call in func_call:
            print(f'Calling function: {call.name}({call.args})')
    print(response.text)
    user_prompt = sys.argv[1]
    tokens = response.usage_metadata.prompt_token_count
    candidates = response.usage_metadata.candidates_token_count
    if verbose:
        print(f'User prompt: {user_prompt}')
        print(f'Prompt tokens: {tokens}')
        print(f'Response tokens: {candidates}')    
        
if __name__ == '__main__':
    main()
