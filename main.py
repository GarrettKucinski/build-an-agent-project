import os
import sys
from token import STRING

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.call_tool_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if sys.argv[1] == None:
    print("Error: a prompt must be provided.")
    sys.exit(1)

client = genai.Client(api_key=api_key)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

user_prompt = sys.argv[1]
messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, list files in the working directory itself always specified as the argument '.'",
            ),
        },
    ),
)

schema_get_file_contents = types.FunctionDeclaration(
    name="get_file_contents",
    description="Lists the contents of a file constrained to the working directory, output is truncated to 10,000 characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read the contents of, reletive to the working directory.",
            )
        },
    ),
)

scheme_overwrite_file = types.FunctionDeclaration(
    name="overwrite_file",
    description="Overwrites the contents of the file given a file path, relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to overwrite the contents of, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING, description="The content to write to the file"
            ),
        },
    ),
)

scheme_run_python = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a file containing python code in the relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file containing the python code to be executed, relative to the working directory.",
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_contents,
        scheme_overwrite_file,
        scheme_run_python,
    ]
)

set_verbose = sys.argv[-1] == "--verbose"

for i in range(20):
    last_message = messages[-1] if messages else None

    if (
        last_message
        and last_message.parts[-1].function_call is None
        and last_message.parts[-1].function_response is None
        and i > 0
    ):
        # if i == 20:
        # print("GEMINI RESPONSE:", last_message[-1].text)
        print(last_message)
        break

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt, tools=[available_functions]
        ),
    )

    for candidate in response.candidates:
        message_content = candidate.content
        messages.append(message_content)
        if message_content.parts[-1].function_call is not None:
            function_call_result = call_function(
                message_content.parts[-1].function_call, set_verbose
            )
            messages.append(function_call_result)

if set_verbose:
    print(f"Working on: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(f"Candidates: {response.candidates}")
