from google.genai import types

from functions.get_file_contents import get_file_contents
from functions.get_files_info import get_files_info
from functions.overwrite_file import overwrite_file
from functions.run_python_file import run_python_file

function_map = {
    "get_file_contents": get_file_contents,
    "get_files_info": get_files_info,
    "overwrite_file": overwrite_file,
    "run_python_file": run_python_file,
}


def call_function(function, verbose=False):
    if verbose:
        print(f"Calling function: {function.name}({function.args})")
    else:
        print(f" - Calling function: {function.name}")

    if function_map.get(function.name, None) == None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function.name,
                    response={"error": f"Unknown function: {function.name}"},
                )
            ],
        )

    function.args["working_directory"] = "./calculator"

    result = function_map[function.name](**function.args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function.name,
                response={"result": result},
            )
        ],
    )
