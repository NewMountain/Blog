"""Helper functions to locate content."""
import os


def file_of_interest(file_name, supported_extensions):
    """Filter for CONTENT_EXTENSIONS_SUPPORTED."""

    for f in supported_extensions:
        if f in file_name:
            return True

    return False


def locate_content_files(os_walk_values, supported_extensions):
    """Turn the os.walk() data structure into one that works better for us."""
    acc = []
    for path, dirs, files in os_walk_values:
        desired_files = [
            f"{path}/{file}"
            for file in files
            if file_of_interest(file, supported_extensions)
        ]
        acc += desired_files

    return acc


def split_by_content_type(list_of_files, supported_extensions):
    """Split the files into a dict by type."""
    d = {}
    for file_type in supported_extensions:
        d[file_type] = [f for f in list_of_files if file_type in f]

    return d


def acquire_content_files(cwd, supported_extensions):
    """Locate the files from which to generate content."""
    content_files = locate_content_files(
        os.walk(f"{cwd}/content"), supported_extensions
    )

    return split_by_content_type(content_files, supported_extensions)
