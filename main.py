import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

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



def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=messages,
    )

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
