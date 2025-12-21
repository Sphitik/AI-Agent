import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, verbose)


def generate_content(client, messages, verbose):
    MAX_STEPS = 4

    for step in range(MAX_STEPS):
        if verbose:
            print(f"\n=== LLM STEP {step+1} ===")

        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
            )
        )

        for cand in response.candidates:
            if cand.content:
                messages.append(cand.content)

        if response.text and not response.function_calls:
            print("\nFinal response:\n" + response.text)
            return

        if not response.function_calls:
            print("Model returned no text and no function calls. Stopping.")
            return

        for fc in response.function_calls:
            if verbose:
                print(f" - Calling function: {fc.name}({fc.args})")
            tool_message = call_function(fc, verbose=verbose)

            messages.append(tool_message)

    print("Reached max iteration limit (20). Stopping.")



if __name__ == "__main__":
    main()