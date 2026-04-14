import re, argparse, glob, os

def process_file(input_file, output_file, verbose):
    try:
        if(output_file is None):
            output_file = input_file.rsplit('.', 1)[0] + '_formatted.txt'

        if(verbose):
            print(f"Reading: {input_file}...")

        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Join internal line breaks
        content = re.sub(r"\n([^\n])", r"\1", content)

        # 2. Force newline before verse number
        content = re.sub(r"(?<!Ĉapitro )(\d+) ?(?!\n)", r"\n\1 ", content)

        # 3. Collapse double newlines
        content = re.sub(r"\n\n+", r"\n", content)

        content = content.strip()

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"Success: '{input_file}' -> '{output_file}'")

    except Exception as e:
        print(f"An error occurred while processing {input_file}: {e}")

def main():
    parser = argparse.ArgumentParser(
        prog='regex_utf.py',
        description='Formats UTF files into parseable files for Bible indexing',
        epilog='made with <3 by ponchoima'
    )

    parser.add_argument('-f', '--filenames', nargs = '+', required = True,
                        help = 'path(s) for file(s) to parse (supports wildcards like *.utf)')
    parser.add_argument('-o', '--output', type = str,
                        help = 'custom output name (only works if processing a single file)')
    parser.add_argument('-v', '--verbose', action = 'store_true',
                        help = 'outputs the steps it follows')
    
    args = parser.parse_args()

    all_files = []
    for pattern in args.filenames:
        expanded = glob.glob(pattern)
        if(not expanded):
            print(f"Warning: No files matched pattern '{pattern}'")
        all_files.extend(expanded)

    if len(all_files) > 1 and args.output:
        print("Error: You cannot specify a custom output name when processing multiple files.")
        return 1

    for file_path in all_files:
        process_file(file_path, args.output, args.verbose)

if __name__ == '__main__':
    main()
