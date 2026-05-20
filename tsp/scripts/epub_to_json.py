import os, json, ebooklib, argparse, logging
from ebooklib import epub
from bs4 import BeautifulSoup

def transform(epub_path):
    # Read the epub file structure[cite: 1]
    book = epub.read_epub(epub_path)
    
    # Handle naming conventions
    input_filename  = os.path.basename(epub_path)
    base_name       = os.path.splitext(input_filename)[0]
    output_filename = f"{base_name}.json"
    
    # Basic Metadata 
    metadata = {
        "author"        : book.get_metadata('DC', 'creator')[0][0] if book.get_metadata('DC', 'creator') else "Unknown",
        "pub_year"      : 'tbd', # TODO: Do something with this.
        "title"         : book.get_metadata('DC', 'title')[0][0] if book.get_metadata('DC', 'title') else "Unknown",
        "city"          : 'tbd', # TODO: Do something with this.
        "publisher"     : 'tbd', # TODO: Do something with this.
        "isbn"          : 'tbd', # TODO: Do something with this.
        "original_file" : input_filename
    }

    segments = []
    para_idx = 0

    # Iterate through the spine items (XHTML documents)[cite: 1]
    for item in book.get_items():
        if(item.get_type() == ebooklib.ITEM_DOCUMENT):
            # Extract raw HTML bytes and parse[cite: 1]
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            
            # Identify all paragraphs
            paragraphs = soup.find_all('p')
            
            for p in paragraphs:
                clean_text = p.get_text().strip()
                
                # Skip non-content paragraphs
                if(len(clean_text) > 10):
                    para_idx += 1
                    
                    unique_id = f"{base_name.upper().replace(' ', '_')}_{para_idx:06d}"
                    
                    segments.append({
                        "id": unique_id,
                        "text": clean_text,
                        "html": str(p),
                    })

    output_data = {
        "metadata": metadata,
        "segments": segments
    }

    # Save with UTF-8 to ensure Esperanto/Russian/Spanish support
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii = False, indent = 2)

    print(f"Index complete: {output_filename}")
    print(f"Total Segments Parsed: {para_idx}")

    return 0

def main(verbose, filename):
    if(verbose):
        logging.basicConfig(level = logging.DEBUG, format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    else:
        logging.basicConfig(level = logging.WARNING) # Only show errors by default

    transform(filename)

    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            prog        = 'epub_to_json.py',
            description = 'TODO',
            epilog      = 'made with <3 by ponchoima')

    parser.add_argument('-f', '--file', required = True,
                        help = 'file to parse to json')
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False,
                        help = 'outputs the steps it follows')

    args = parser.parse_args()
    main(args.verbose, args.file)
