import os
from pathlib import Path
from collections import defaultdict

def smart_read_file(file_path):
    encodings = ['utf-8-sig', 'utf-16', 'utf-16le', 'utf-16be', 'latin-1', 'cp1252']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                lines = f.read().splitlines()
            return lines
        except UnicodeDecodeError:
            continue
    raise RuntimeError("❌ Could not decode the file. Tried multiple common encodings.")

def parse_file_list(file_path):
    lines = smart_read_file(file_path)

    cleaned = []
    for line in lines:
        line = line.strip()
        if line:
            line = line.replace('\\', '/')
            cleaned.append(Path(line))
    if not cleaned:
        raise ValueError("The file was read but contains no usable paths.")
    return cleaned

def build_tree(paths):
    tree = lambda: defaultdict(tree)
    root = tree()
    for path in paths:
        current = root
        for part in path.parts:
            current = current[part]
    return root

def print_tree(d, prefix="", file=None):
    keys = sorted(d.keys())
    last_key = keys[-1] if keys else None
    for key in keys:
        connector = "└── " if key == last_key else "├── "
        line = f"{prefix}{connector}{key}"
        print(line)
        if file:
            file.write(line + "\n")
        if d[key]:
            extension = "    " if key == last_key else "│   "
            print_tree(d[key], prefix + extension, file=file)

def main():
    try:
        print("=== File Tree Generator ===")
        user_input = input("Enter the path to a directory or the name of a txt file: ").strip()

        # Resolve relative or simple filenames to full paths
        input_path = Path(user_input).expanduser()
        if not input_path.is_absolute():
            input_path = (Path.cwd() / input_path).resolve()

        if not input_path.exists():
            raise FileNotFoundError("The path you entered does not exist.")

        paths = []

        if input_path.is_file():
            paths = parse_file_list(input_path)
        elif input_path.is_dir():
            root_path = input_path
            for dirpath, _, filenames in os.walk(root_path):
                for filename in filenames:
                    full_path = Path(dirpath) / filename
                    rel_path = full_path.relative_to(root_path)
                    paths.append(rel_path)
            if not paths:
                raise ValueError("The folder is empty or contains no files.")
        else:
            raise RuntimeError("Unsupported input type.")

        tree = build_tree(paths)
        top = paths[0].parts[0] if paths else "."

        print(f"\n{top}/")
        print_tree(tree[top])

        save = input("\nDo you want to save this to a file? (y/n): ").strip().lower()
        if save == 'y':
            save_dir = Path("./pythonpathmaker")
            save_dir.mkdir(parents=True, exist_ok=True)

            # Use original input filename (no extension) for naming
            original_name = input_path.stem
            output_file = save_dir / f"{original_name}_pathtree.txt"

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"{top}/\n")
                print_tree(tree[top], file=f)
            print(f"\n✅ Tree saved to: {output_file.resolve()}")

    except Exception as e:
        print(f"\n❌ Error: {e}")

    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
