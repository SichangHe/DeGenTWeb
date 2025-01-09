import os


def include_file(module_path: str, file_name: str):
    """Include a file in the same directory as the module.
    Pass in `__file__` as `module_path`."""
    current_dir = os.path.dirname(os.path.abspath(module_path))
    file_path = os.path.join(current_dir, file_name)
    with open(file_path, "r") as file:
        return file.read()
