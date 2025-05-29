import os
from datetime import datetime

# Konfiguráció közvetlenül a szkriptben
SCRIPT_CONFIG = {
    "exclude_dirs": [
        ".git",
        ".idea",
        ".cursor",
        "scripts",
        "_temp",
        "__pycache__"
    ],
    "file_index_title": "Project File Index"
}

def generate_markdown_list(directory, exclude_dirs, current_level=0):
    """Generates a markdown list of files and folders, excluding specified ones."""
    markdown_lines = []
    try:
        for item in sorted(os.listdir(directory)):
            if item in exclude_dirs and current_level == 0: # Only exclude top-level specified dirs
                continue
            if item.startswith('.') and item not in exclude_dirs: # More general dotfile/dir exclusion
                 if item != '.gitattributes' and item != '.gitignore': # Keep these common ones
                    continue

            path = os.path.join(directory, item)
            indent = '  ' * current_level # Indentation for hierarchy

            if os.path.isdir(path):
                # Check if it's in exclude_dirs, not just at top level
                # This is a simpler check for any path segment matching an excluded name.
                # For more robustness, one might want to check full relative paths against exclude_dirs.
                if any(excluded_dir in path.split(os.sep) for excluded_dir in exclude_dirs):
                    if item not in exclude_dirs: # if the folder itself is not excluded at top level
                         # This allows excluding a parent but not explicitly listed children deeper down if needed by a more complex rule
                         # However, with current simple exclude_dirs, this basically means if a part of the path is excluded, skip.
                         pass # placeholder if we want to refine logic for nested excludes
                    # else: # it is explicitly in exclude_dirs and at top level (handled above)
                    #    continue
                    if item in exclude_dirs: # if folder name itself is in exclude list, always skip
                        continue
                    # A more refined check could be done here if we want to allow specific subfolders of excluded parents

                markdown_lines.append(f"{indent}- {item} (folder)")
                # Recursively call for subdirectories, incrementing the level for indentation
                # and passing down the original exclude_dirs list
                markdown_lines.extend(generate_markdown_list(path, exclude_dirs, current_level + 1))
            else:
                markdown_lines.append(f"{indent}- {item}")
    except FileNotFoundError:
        print(f"Warning: Directory not found: {directory}. This can happen if a directory was deleted during script execution.")
    except PermissionError:
        print(f"Warning: Permission denied for directory: {directory}.")
    return markdown_lines

def main():
    """Main function to generate the file index."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
    output_file_path = os.path.join(project_root, '01_meta', 'file_index.md')
    exclude_dirs = SCRIPT_CONFIG["exclude_dirs"]
    # Külön kezeljük, hogy a scripts és _temp mappa NE legyen kizárva a 01_meta-ból
    exclude_dirs = [d for d in exclude_dirs if not (d in ['scripts', '_temp'] and os.path.basename(os.path.dirname(script_dir)) == '10_meta')]
    file_index_title = SCRIPT_CONFIG["file_index_title"]

    markdown_content = generate_markdown_list(project_root, exclude_dirs)

    # --- YAML Frontmatter ---
    yaml_frontmatter = ("---\n"
                        f"modified: {datetime.now().strftime('%Y-%m-%d')}\n"
                        f"title: \"{file_index_title}\"\n"
                        "tags: [index, project_files, structure]\n"
                        "overview: \"This document lists all files and folders in the project, excluding specified ones.\"\n"
                        "---\n\n")
    # --- Table of Contents (simple one for this file) ---
    toc = "## Table of Contents\n- [Project Root](#project-root)\n\n"

    # --- Main Content ---
    output_content = yaml_frontmatter
    output_content += toc
    output_content += "## Project Root\n"
    output_content += "\n".join(markdown_content)
    output_content += "\n"

    try:
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(output_content)
        print(f"File index generated at: {output_file_path}")
    except IOError as e:
        print(f"Error writing to output file {output_file_path}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    main() 