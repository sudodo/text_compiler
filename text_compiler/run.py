import argparse
import re
import os

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Compile text files with "@import" directives.')
    parser.add_argument('-i', '--input-file-path', type=str, required=True, help='Path to the input file')
    parser.add_argument('-o', '--output-file-path', type=str, required=True, help='Path for the output file')
    return parser.parse_args()

import os
import re

def process_file(file_path: str, base_path: str = '', current_chain: set = None) -> str:
    """
    Process a file, replacing "@import" directives with the content of the referenced files.
    Also checks for circular imports within the current import chain.

    Args:
    file_path (str): Path to the file to process. Can be absolute or relative.
    base_path (str): Base path to resolve relative paths for imports.
    current_chain (set): Set of files in the current import chain to detect circular imports.

    Returns:
    str: The processed content of the file.
    """
    if current_chain is None:
        current_chain = set()

    # Resolve the absolute path of the file if a relative path is provided
    abs_file_path = os.path.abspath(os.path.join(base_path, file_path))

    if abs_file_path in current_chain:
        print(f"Warning: Circular import detected for file {abs_file_path}. Skipping import.")
        return ''

    if not os.path.isfile(abs_file_path):
        raise FileNotFoundError(f"The file {abs_file_path} does not exist.")

    current_chain.add(abs_file_path)

    with open(abs_file_path, 'r') as file:
        content = []
        for line in file:
            match = re.match(r'@import\((.*?)\)', line.strip())
            if match:
                import_path = match.group(1)
                import_base_path = os.path.dirname(abs_file_path)
                imported_content = process_file(import_path, import_base_path, current_chain.copy())
                if imported_content and not imported_content.endswith('\n'):
                    imported_content += '\n'
                content.append(imported_content)
            else:
                content.append(line)

        current_chain.remove(abs_file_path)
        return ''.join(content)

def main():
    args = parse_arguments()
    try:
        compiled_content = process_file(args.input_file_path)
        with open(args.output_file_path, 'w') as output_file:
            output_file.write(compiled_content)
        print(f"Compiled file saved to {args.output_file_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
