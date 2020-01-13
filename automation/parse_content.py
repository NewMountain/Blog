"""Module to parse the idiosyncratic file types into dictionaries of useful data."""
import yaml


def has_metadata(file_contents):
    """Check to see if the file contains metadata."""
    lines = file_contents.split("\n")
    return "---" in lines[0]


def find_metadata_end(raw_file):
    """Extract the metadata from the raw file."""
    lines = raw_file.split("\n")
    start = None
    end = None

    for idx, line in enumerate(lines):
        if "---" in line and start is None:
            start = idx
        elif "---" in line and start is not None:
            return idx


def extract_metadata(last_metadata_line, raw_content):
    """Extract metatdata is pythonic format."""
    lines = raw_content.split("\n")
    raw_metadata = "\n".join(lines[1:last_metadata_line])
    yaml_data = yaml.load(raw_metadata, Loader=yaml.FullLoader)
    return yaml_data


def extract_content(last_metadata_line, raw_content):
    """Extract the content without the metadata."""
    lines = raw_content.split("\n")
    content = "\n".join(lines[last_metadata_line + 1 :])
    return content


def make_file_name(full_file_path, supported_extensions):
    """Generate a pure file name for the file."""
    chunks = full_file_path.split("/")
    file_name = chunks[-1]

    for ext in supported_extensions:
        # Remove all extensions
        file_name = file_name.replace(ext, "")

    return file_name


def get_original_file_name(full_file_path):
    """Get the file name from the path."""
    return full_file_path.split("/")[-1]


def parse_file_content(cwd, full_file_path, supported_extensions):
    """Return a dictionary of content to be more easily processed downstream."""
    processed_data = {}

    processed_data["full_file_path"] = full_file_path

    original_file_name = get_original_file_name(full_file_path)
    processed_data["original_file_name"] = original_file_name

    with open(full_file_path, "r") as file:
        processed_data["raw_contents"] = file.read()

    processed_data["relative_path"] = full_file_path.replace(cwd, "")

    processed_data["new_path"] = processed_data["relative_path"].replace(
        original_file_name, ""
    )

    processed_data["has_metadata"] = has_metadata(processed_data["raw_contents"])

    processed_data["file_name"] = make_file_name(full_file_path, supported_extensions)

    if processed_data["has_metadata"]:
        raw_content = processed_data["raw_contents"]
        last_metadata_line = find_metadata_end(raw_content)
        processed_data["end_of_metadata"] = last_metadata_line
        processed_data["metadata"] = extract_metadata(last_metadata_line, raw_content)
        processed_data["content"] = extract_content(last_metadata_line, raw_content)
    else:
        # No metadata only content
        processed_data["content"] = processed_data["raw_contents"]

    return processed_data


def parse_content(cwd, content_locations, supported_extensions):
    """Parse content files to prepare for rendering."""
    parsed_content = {}
    content_dir = f"{cwd}/content/"

    for ext in supported_extensions:
        files = content_locations[ext]
        parsed_content[ext] = [
            parse_file_content(content_dir, file, supported_extensions)
            for file in files
        ]

    return parsed_content
