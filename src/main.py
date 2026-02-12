import os, shutil

from pathlib import Path

from transformers import markdown_to_html_node
from helpers import extract_title

static_dir = "./static"
public_dir = "./public"
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

def generate_page(from_path, template_path, dest_path):
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

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, item)
        
        if os.path.isdir(from_path):
            to_path = os.path.join(dest_dir_path, item)
            generate_pages_recursive(from_path, template_path, to_path)
        elif item.endswith(".md"):
            to_path = os.path.join(dest_dir_path, Path(item).with_suffix(".html"))
            generate_page(from_path, template_path, to_path)

def main():
    if os.path.exists(public_dir):
        print("Public Directory Found.. Deleting")
        shutil.rmtree(public_dir)
    print("Copying Static Files To Public Directory..")
    copy_contents(static_dir, public_dir)
    
    generate_pages_recursive(content_dir, template_loc, public_dir)

if __name__ == "__main__":
    main()
