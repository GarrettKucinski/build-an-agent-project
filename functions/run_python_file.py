import os
import subprocess


def run(file):
    os.chmod(file, 0o755)
    result = subprocess.run(
        ["python3", file], timeout=30, capture_output=True, text=True
    )
    out = result.stdout
    err = result.stderr

    output = f"""
    STDOUT: {out}
    STDERR: {err}
    """

    if result.returncode != 0:
        output += f"Process exited with code {result.returncode}"

    if out == "" and err == "":
        return "No output produced."

    return output


def run_python_file(working_directory, file_path):
    working_dir = os.path.abspath(working_directory)
    target = os.path.abspath(os.path.join(working_directory, file_path))

    try:
        if not target.startswith(working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        if not os.path.exists(target):
            return f'Error: File "{file_path}" not found'

        return run(target)

    except Exception as e:
        return f"Error: executing Python file: {e}"
