import os


def parse_file(target):
    MAX_CHARS = 10000
    CHUNK_SIZE = 1024

    total_chars = 0
    chunks = ""

    with open(target, "r") as f:
        while True:
            chunks += f.read(CHUNK_SIZE)
            total_chars += len(chunks)
            if not chunks or total_chars > MAX_CHARS:
                break

    if total_chars > MAX_CHARS:
        chunks += f'\n\n[...File "{target}" truncated at 10000 characters]'

    return chunks


def get_file_contents(working_directory: str, file_path: str) -> str:

    try:
        working_dir = os.path.abspath(working_directory)
        target = os.path.join(working_dir, file_path)

        if not target.startswith(working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        file_contents = parse_file(target)

        return file_contents
    except Exception as e:
        return f"Error: {str(e)}"
