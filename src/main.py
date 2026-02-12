import os, shutil, sys

from pathlib import Path

from transformers import markdown_to_html_node
from helpers import extract_title

static_dir = "./static"
public_dir = "./docs"
content_dir = "./content"
template_loc = "./template.html"

def copy_contents(from_dir, to_dir):
    os.makedirs(to_dir, exist_ok=True)
    for item in os.listdir(from_dir):
        from_path = os.path.join(from_dir, item)
        to_path = os.path.join(to_dir, item)
        if os.path.isdir(from_path):
            copy_contents(from_path, to_path)
        else:
            print(f"\tCopying {item} from {from_dir} -> {to_dir}")
            shutil.copy(from_path, to_path)

def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_file = open(from_path, "r")
    markdown = markdown_file.read()
    markdown_file.close()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    href_rep = "href=\""
    template = template.replace(f"{href_rep}/", f"{href_rep}{base_path}")
    src_rep = "src=\""
    template = template.replace(f"{src_rep}/", f"{src_rep}{base_path}")

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    for item in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, item)
        
        if os.path.isdir(from_path):
            to_path = os.path.join(dest_dir_path, item)
            generate_pages_recursive(from_path, template_path, to_path, base_path)
        elif item.endswith(".md"):
            to_path = os.path.join(dest_dir_path, Path(item).with_suffix(".html"))
            generate_page(from_path, template_path, to_path, base_path)

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    print(basepath)

    if os.path.exists(public_dir):
        print("Public Directory Found.. Deleting")
        shutil.rmtree(public_dir)
    print("Copying Static Files To Public Directory..")
    copy_contents(static_dir, public_dir)
    
    generate_pages_recursive(content_dir, template_loc, public_dir, basepath)

if __name__ == "__main__":
    main()
