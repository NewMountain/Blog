""""Make all your publication super fast and easy with Python!"""
import os
import shutil
from acquire_content import acquire_content_files
from parse_content import parse_content
import json
import markdown
from mdx_gfm import GithubFlavoredMarkdownExtension
import jinja2

# Note: If you add a new extension type, do not forget to add
# logic to parse_content
CONTENT_EXTENSIONS_SUPPORTED = [".j2", ".md"]


def wipe_and_replace_folder(path):
    """Delete the directory if it exists and create a new one."""
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.mkdir(path)


def create_file(content, full_file_path):
    """Create your new file."""
    os.makedirs(os.path.dirname(full_file_path), exist_ok=True)

    with open(full_file_path, "w") as f:
        f.write(content)


def read_file(full_file_path):
    """Helper function to read file."""
    with open(full_file_path, "r") as f:
        return f.read()


def insert_content_blog_template(header, content, footer, assets_path):
    """Insert Markdown into blog template."""
    templateLoader = jinja2.FileSystemLoader(searchpath=assets_path)
    templateEnv = jinja2.Environment(loader=templateLoader)
    template_file = "blog-template.j2"
    template = templateEnv.get_template(template_file)
    outputText = template.render(header=header, content=content, footer=footer)

    return outputText


def insert_blog_preview(previews, assets_path):
    """Insert Markdown into blog template."""
    templateLoader = jinja2.FileSystemLoader(searchpath=assets_path)
    templateEnv = jinja2.Environment(loader=templateLoader)
    template_file = "blog-preview.j2"
    template = templateEnv.get_template(template_file)
    outputText = template.render(previews=previews)

    return outputText


def get_header(path):
    """Return the header template."""
    return read_file(f"{path}/header.html")


def get_footer(path):
    """Return the footer template."""
    return read_file(f"{path}/footer.html")


def generate_markdown_page(build_path, markdown_page):
    """Take the markdown dictionary and make it an HTML page."""
    has_metadata = markdown_page["has_metadata"]
    if has_metadata:
        metadata = markdown_page["metadata"]

    content = markdown_page["content"]

    html_body = markdown.markdown(
        content, extensions=[GithubFlavoredMarkdownExtension()]
    )

    base_path = build_path.replace("/build", "")
    assets_path = f"{base_path}/content/assets/"

    html = insert_content_blog_template(
        get_header(assets_path), html_body, get_footer(assets_path), assets_path
    )

    new_file_full_path = (
        f"{build_path}/{markdown_page['new_path']}{markdown_page['file_name']}.html"
    )

    create_file(html, new_file_full_path)


def generate_markdown_content(build_path, parsed_data):
    """Create a directory at the specified path and fill with blog content."""
    # Delete the directory if it exists
    wipe_and_replace_folder(build_path)

    for page in parsed_data[".md"]:
        generate_markdown_page(f"{build_path}", page)

    # TODO: Blog posts actually using Jinja2


def generate_blog_preview(build_path, parsed_data):
    """Generate an intro for all blog posts marked to publish."""
    base_path = build_path.replace("/build", "")
    assets_path = f"{base_path}/content/assets/"

    pages = []
    for page in parsed_data[".md"]:
        if "has_metadata" in page and page["has_metadata"]:
            metadata = page["metadata"]
            if metadata["publish"] is not None and "blog" in metadata["publish"]:
                new_data = {
                    "written": metadata["written"],
                    "title": metadata["title"],
                    "lead": metadata["lead"],
                    "rel_link": f"/{page['new_path']}{page['file_name']}.html",
                }
                pages.append(new_data)

    pages.sort(key=lambda x: x["written"], reverse=True)

    html = insert_blog_preview(pages, assets_path)

    return html


def generate_index(build_path, parsed_content):
    """Generate the index.html homepage."""
    page_of_interest = {}
    for page in parsed_content[".j2"]:
        if "index" in page["original_file_name"]:
            page_of_interest = page

    base_path = build_path.replace("/build", "")
    assets_path = f"{base_path}/content/assets/"

    # Put the data in the template
    blog_preview = generate_blog_preview(build_path, parsed_content)
    rtemplate = jinja2.Environment(loader=jinja2.BaseLoader).from_string(
        page_of_interest["content"]
    )
    html = rtemplate.render(
        header=get_header(assets_path),
        blog_preview=blog_preview,
        footer=get_footer(assets_path),
    )

    new_file_full_path = f"{build_path}/{page_of_interest['new_path']}{page_of_interest['file_name']}.html"

    create_file(html, new_file_full_path)


def main():
    # Find the current working directory
    cwd = os.getcwd()
    sub_dirs = os.listdir()

    # Make sure we have a content directory
    if "content" not in sub_dirs:
        raise Exception("Unable to generate a blog without a content directory")

    raw_content_locations = acquire_content_files(cwd, CONTENT_EXTENSIONS_SUPPORTED)

    parsed_content = parse_content(
        cwd, raw_content_locations, CONTENT_EXTENSIONS_SUPPORTED
    )

    build_dir = f"{cwd}/build"

    generate_markdown_content(build_dir, parsed_content)

    generate_index(build_dir, parsed_content)


if __name__ == "__main__":
    main()
