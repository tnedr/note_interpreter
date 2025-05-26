import os
import re

def get_markdown_files(root_dir, exclude_dirs_set):
    markdown_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Modify dirnames in-place to prevent descending into excluded directories
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs_set]
        
        for filename in filenames:
            if filename.endswith(".md"):
                # Ensure we are not processing files within an excluded directory path
                # This check is somewhat redundant if dirnames[:] is effective,
                # but good for robustness if script is called on a subpath.
                is_in_excluded_path = False
                for excluded_dir in exclude_dirs_set:
                    if os.path.join(root_dir, excluded_dir) in dirpath:
                        is_in_excluded_path = True
                        break
                if not is_in_excluded_path:
                     markdown_files.append(os.path.join(dirpath, filename))
    return markdown_files

def process_markdown_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()

        # Regex to find frontmatter at the beginning of the file.
        # Captures the content between '---' lines. DOTALL allows '.' to match newlines.
        frontmatter_re = re.compile(r'\\A---\\s*\\n(.*?)\\n---\\s*\\n', re.DOTALL)
        match = frontmatter_re.match(original_content)

        new_field_line = 'seen_by_human: "n/a"'
        
        if match:
            frontmatter_internal_content = match.group(1) # Text between the --- lines
            body_after_frontmatter = original_content[match.end():]

            lines = frontmatter_internal_content.strip().split('\\n')
            
            # Remove existing 'seen_by_human' field to ensure it's updated and potentially reordered
            # Keep only non-empty lines that are not the 'seen_by_human' field
            updated_lines = [line for line in lines if line.strip() and not line.strip().startswith('seen_by_human:')]
            updated_lines.append(new_field_line) # Add the new field, ensuring it's last among current lines
            
            updated_frontmatter_text = "\\n".join(updated_lines)
            new_content = f"---\\n{updated_frontmatter_text}\\n---\\n{body_after_frontmatter}"
        else:
            # No frontmatter found, or it's not at the very start / malformed for the regex
            # Prepend a new frontmatter block
            # Ensure there's a newline after the new frontmatter if original content exists
            if original_content.strip():
                new_content = f"---\\n{new_field_line}\\n---\\n{original_content}"
            else: # Empty or whitespace-only file
                new_content = f"---\\n{new_field_line}\\n---\\n"


        if new_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Modified: {file_path}")
            return True
        else:
            print(f"No change needed (content identical or field already present as specified): {file_path}")
            return False

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

if __name__ == "__main__":
    # Assumes the script is in a 'scripts' subdirectory and project root is one level up.
    # If running this script from the project root as 'python scripts/add_seen_by_human_field.py',
    # os.getcwd() will be the project root.
    project_root = os.getcwd() 
    
    # Define directories to exclude from processing
    # Adding '_scripts' itself to prevent it from processing its own potential .md files if any
    exclude_dirs = {'.git', '.idea', '__pycache__', 'venv', 'node_modules', '_scripts'}
    
    markdown_files_to_process = get_markdown_files(project_root, exclude_dirs)
    
    count_modified = 0
    count_total = len(markdown_files_to_process)
    
    if not markdown_files_to_process:
        print(f"No markdown files found to process in '{project_root}' (excluding specified directories).")
    else:
        print(f"Found {count_total} markdown files in '{project_root}'. Starting processing...")
        for md_file in markdown_files_to_process:
            # Normalize path for display and consistency
            relative_file_path = os.path.relpath(md_file, project_root)
            if process_markdown_file(md_file):
                count_modified += 1
        print(f"\\nProcessing complete. Modified {count_modified} out of {count_total} files.") 