import os


def get_files_info(working_directory: str, directory: str = None) -> None:
    if not directory in working_directory:
        print(
            f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        )

    try:
        if not os.path.isdir(directory):
            print(f'Error: "{directory}" is not a directory')

        files: list[str] = os.listdir(directory)
        for file in files:
            print(
                f"{file}: file_size={os.path.getsize(file)} bytes, is_dir={os.path.isdir(file)}"
            )
    except Exception as e:
        print(f"Error: {e}")
