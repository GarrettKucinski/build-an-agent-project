import os


def overwrite_file(working_directory, file_path, content):
    working_dir = os.path.abspath(working_directory)
    target = os.path.join(working_dir, file_path)

    if not target.startswith(working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        if not os.path.exists(os.path.dirname(target)):
            os.makedirs(os.path.dirname(target))

        with open(target, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} bytes written)'
    except Exception as e:
        return f"Error: {e}"
