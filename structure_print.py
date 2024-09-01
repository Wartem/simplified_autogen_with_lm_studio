import os

# Define the directories to exclude and the file extensions to include
excluded_dirs = {'.venv', 'custom,' '.\custom', 'old', 'structure_print', 'venv', '__pycache__', 'test_v2', 'test_v3',  'CO2EmissionForecasting', 'C02TransportCalculator', '.git', 'git'}
included_extensions = {'.py', '.txt', '.html', '.js', '.json', '.yml', '.yaml'}

# The name of the output file
output_filename = 'directory_structure_and_contents.txt'

# Set to track processed files
processed_files = set()

def is_included_file(file_name):
    # Check if the file has one of the allowed extensions
    return any(file_name.endswith(ext) for ext in included_extensions)

def write_file_content(file_path, output_file):
    # Write the name and content of the file to the output file
    output_file.write(f"\nFile: {file_path}\n")
    output_file.write(f"{'-'*len(f'File: {file_path}')}\n")
    with open(file_path, 'r', encoding='utf-8') as f:
        output_file.write(f.read() + '\n\n')

def traverse_directory(directory, output_file):
    # Traverse the directory structure
    for root, dirs, files in os.walk(directory):
        # Skip the excluded directories
        dirs[:] = [d for d in dirs if d not in excluded_dirs]

        # Write the directory path as a heading
        output_file.write(f"\nDirectory: {root}\n")
        output_file.write(f"{'='*len(f'Directory: {root}')}\n")
        
        for file in files:
            if is_included_file(file):
                file_path = os.path.join(root, file)
                # Check if the file has already been processed
                if file_path not in processed_files:
                    write_file_content(file_path, output_file)
                    # Mark the file as processed
                    processed_files.add(file_path)

# Run the script
with open(output_filename, 'w', encoding='utf-8') as output_file:
    traverse_directory('.', output_file)

print(f"Directory structure and contents have been saved to '{output_filename}'.")
