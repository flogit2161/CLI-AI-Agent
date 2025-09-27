import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.call_function import call_function
from functions.call_function import available_functions

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

    if verbose:
        print(f'User prompt: {prompt}')


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=messages, config = types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
    )
    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if not function_call_result.parts or not function_call_result.parts[0].function_response:
            raise Exception('empty function call')
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])
    if not function_responses:
        raise Exception("no function responses")
    
    
    tokens = response.usage_metadata.prompt_token_count
    candidates = response.usage_metadata.candidates_token_count
    if not response.function_calls:
        return response.text
    if verbose:
         print(f'Prompt tokens: {tokens}')
         print(f'Response tokens: {candidates}')    
        
if __name__ == '__main__':
    main()
