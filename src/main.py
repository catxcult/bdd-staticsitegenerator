import os, shutil

from textnode import TextNode, TextType

static_dir = "./static"
public_dir = "./public"

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

def main():
    if os.path.exists(public_dir):
        print("Public Directory Found.. Deleting")
        shutil.rmtree(public_dir)
    print("Copying Static Files To Public Directory..")
    copy_contents(static_dir, public_dir)

if __name__ == "__main__":
    main()
