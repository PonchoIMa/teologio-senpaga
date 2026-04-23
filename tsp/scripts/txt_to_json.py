import json, os, argparse, logging, glob

# TOTEST: When changing chapters, the script adds the captured text in verse 0
# it should generate last verse from previous chapter instead.

# TODO: Pericope logic

# TODO: Solve this?
bible_books = {
        "Protestant" : {
            "OT" : ["GEN", "EXO", "LEV", "NUM", "DET", "JOS",
                    "JUE", "RUT", "1SA", "2SA", "1RE", "2RE",
                    "1CR", "2CR", "ESD", "NEH", "EST", "JOB",
                    "SAL", "PRV", "ECL", "CNT", "ISA", "JER",
                    "LAM", "EZQ", "DAN", "OSE", "JOL", "AMO",
                    "ABD", "JON", "MIQ", "NAH", "HAB", "SOF",
                    "HAG", "ZAC", "MAL"],
            "NT" : ["MAT", "MAR", "LUC", "JUA", "HCH", "ROM",
                    "1CO", "2CO", "GAL", "EFE", "FIL", "COL",
                    "1TS", "2TS", "1TI", "2TI", "TIT", "FLM",
                    "HEB", "STG", "1PE", "2PE", "1JN", "2JN",
                    "3JN", "JUD", "APO"]
        } 

def metadata_collector():
    confirmed = 0

    while(confirmed != 'y'):
        # TODO: Validate that is ISO formatted
        language        = input("Language (default = 'en'): ") or 'en'
        title_full      = input("Title: ")
        abbreviation    = input("Abbreviation: ")
        # TODO : Output a list to choose the system.
        versification   = input("Verse System: ")
        # TODO : datetime - this year
        pub_date        = input("Publication Date (default = 2026): ") or '2026'
        copyright       = input("Copyright (default = 'Public Domain'): ") or 'Public Domain'
        description     = input("Description: ")

        # TODO: Prompt information
        confirmed = input('Is this information correct? (y/n): ').lower()[0] 

    # Dump collected info into metadata
    return {
        "abbreviation"          : abbreviation,
        "title_full"            : title_full,
        "verse_system"          : verse_system,
        "language_code"         : language,
        "copyright"             : copyright,
        "description"           : description,
        "publication_date"      : publication,
    }

def build_json_from_txt(input_path, output_path, chapter_keyword):
    metadata    = []
    verses      = []

    # Verify there's metadata / file exists
    try:
        with open(output_path, 'r+', encoding = 'utf-8') as f:
            logging.debug(f'Opening {output_path} to confirm existance/metadata...')
            json_data = json.load(f)
            metadata  = json_data['metadata']
            verses    = json_data['verses']
    except FileNotFoundError as e:
        logging.error(f'File not found, creating... ')

        # Adding metadata
        with open(output_path, 'w+', encoding = 'utf-8') as f:
            json.dump({'metadata' : metadata}, f)
    except KeyError as e:
        logging.error(f'Metadata not found, calling function to populate... ')
    finally:
        if(metadata == []):
            metadata = metadata_collector()
        pass

    with open(input_path, 'r+', encoding='utf-8') as f:
        book_name = 0 
        book_subt = ''
        book_code = 0
   
        # chapter_keyword = 'Ĉapitro' 
        chapter     = 0
        verse_num   = 0
        verse_txt   = ''
        pericope    = ''

        for line in f:
            logging.debug(f'New line: {line}') 

            # First line is title
            if(not book_name):
                book_name = line
                book_code = input(f'Book code for {book_name}: ').upper()
                continue
            
            # Until first chapter, everything is subtitle
            if(not chapter and not chapter_keyword in line):
                book_subt += line
                continue
            else:
                # New chapter
                if(chapter_keyword in line):
                    if(int(line.split()[1]) != chapter + 1):
                        logging.WARNING(f'Chapter alignment does not match. Calculated is {chapter} while captured is {line.split()[1]}!')
                        pass

                    # Add the last verse from past chapter
                    if(chapter != 0):
                        # dump the previous text.
                        verses.append({
                            "uvid"      : f"{book_code}.{chapter}.{verse_num}",
                            "chapter"   : chapter,
                            "verse"     : verse_num,
                            "text"      : verse_txt,
                            "pericope"  : pericope,
                        })

                    chapter   += 1
                    verse_num = 0
                    continue
    
                # Verse logic
                try:
                    candidate_verse = line.split(' ', 1)
                    if(int(candidate_verse[0])):
                        if(int(candidate_verse[0]) != verse_num + 1):
                           logging.warning(f'Verse alignment has failed')

                        # dump the previous text.
                        if(verse_num != 0):
                            verses.append({
                                "uvid"      : f"{book_code}.{chapter}.{verse_num}",
                                "chapter"   : chapter,
                                "verse"     : verse_num,
                                "text"      : verse_txt,
                                "pericope"  : pericope,
                            })
        
                        # begin a new verse
                        verse_num += 1
                        verse_txt = candidate_verse[1]
                        continue
    
                except ValueError as e:
                    # No initial verse, adding to the current verse and continuing
                    logging.warning(f'The text \'{candidate_verse}\' does note appear to have a verse identifier, adding to verse {verse_num}...')
    
                # Look for pericopes
                verse_txt += line
                continue
            
        # Dumping the last verse captured (if not added?) 
        verses.append({
            "uvid"      : f"{book_code}.{chapter}.{verse_num}",
            "chapter"   : chapter,
            "verse"     : verse_num,
            "text"      : verse_txt,
            "pericope"  : pericope,
        })

    with open(output_path, 'r+', encoding = 'utf-8') as f:
        logging.debug('Adding metadata to file...')
        logging.debug('Adding verses to file...')
        json.dump({'metadata' : metadata, 'verses' : verses}, f)

    return 0

def main(verbose, files):
    if(verbose):
        logging.basicConfig(level = logging.DEBUG, format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    else:
        logging.basicConfig(level = logging.WARNING) # Only show errors by default

    all_files = []
    for pattern in files:
        expanded = glob.glob(pattern)
        if(not expanded):
            print(f"Warning: No files matched pattern '{pattern}'")
        all_files.extend(expanded)

    chapter_keyword = input('Chapter keyword/phrase (check doc if necessary): ')
    for file_path in all_files:
        build_json_from_txt(file_path, '../bibles/esperanto.json', chapter_keyword)

    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            prog        = 'txt_to_json.py',
            description = 'a script to transform the bibles in txt format to the json files for the website',
            epilog      = 'made with <3 by ponchoima')

    parser.add_argument('-f', '--files', nargs = '+', required = True,
                        help = 'path(s) for file(s) to parse (supports wildcards like *.utf)')
    parser.add_argument('-v', '--verbose', action = 'store_true', default = False,
                        help = 'outputs the steps it follows')

    args = parser.parse_args()
    main(args.verbose, args.files)
