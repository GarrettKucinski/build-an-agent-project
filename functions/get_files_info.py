import os


def show_files(directory) -> list[str]:
    files: list[str] = os.listdir(directory)
    # for file in files:
    #     if file == "__pycache__":
    #         continue

    # file_path = os.path.join(directory, file)
    # is_dir = os.path.isdir(file_path)
    # file_size = 0 if is_dir else os.path.getsize(file_path)

    return files


def get_files_info(working_directory: str, directory: str = None) -> str:
    if not directory in os.listdir(working_directory) and directory != ".":
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    current_dir = os.path.join(working_directory, directory)

    if not os.path.isdir(current_dir):
        return f'Error: "{directory}" is not a directory'

    try:
        return show_files(current_dir)
    except Exception as e:
        return f"Error: {e}"
