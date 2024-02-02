import argparse
import re
import os

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Compile text files with "@import" directives.')
    parser.add_argument('-i', '--input-file-path', type=str, required=True, help='Path to the input file')
    parser.add_argument('-o', '--output-file-path', type=str, required=True, help='Path for the output file')
    return parser.parse_args()

def process_file(file_path: str, base_path: str = '') -> str:
    """
    Process a file, replacing "@import" directives with the content of the referenced files.

    Args:
    file_path (str): Path to the file to process.
    base_path (str): Base path to resolve relative paths for imports.

    Returns:
    str: The processed content of the file.
    """
    if not os.path.isabs(file_path):
        file_path = os.path.join(base_path, file_path)

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    with open(file_path, 'r') as file:
        content = []
        for line in file:
            match = re.match(r'@import\((.*?)\)', line.strip())
            if match:
                import_path = match.group(1)
                imported_content = process_file(import_path, os.path.dirname(file_path))
                if not imported_content.endswith('\n'):
                    imported_content += '\n'
                content.append(imported_content)
            else:
                content.append(line)
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
