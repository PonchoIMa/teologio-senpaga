import json, os, argparse, logging

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
    }

def metadata_collector():
    confirmed = 0

    while(confirmed != 'y'):
        language        = input("Language (default = 'en'): ") or 'en'
        title_full      = input("Title: ")
        abbreviation    = input("Abbreviation: ")
        # TODO : Output a list to choose the system.
        versification   = input("Verse System: ")
        translator      = input("Translator (default = 'PonchoIMa'): ") or 'PonchoIMa'
        # TODO : datetime - this year
        publication     = input("Publication Date (default = 2026): ") or '2026'
        copyright       = input("Copyright (default = 'Public Domain'): ") or 'Public Domain'
        source_format   = input("Source Format: ") or 'NA'
        digital_source  = input("Digital Source: ") or 'NA'

        # TODO: Prompt information
        confirmed = input('Is this information correct? (y/n): ').lower()[0] 

    # Dump collected info into metadata
    return {
            "version_info" : {
                "title_full"            : title_full,
                "language"              : language,
                "abbreviation"          : abbreviation,
                "versification_system"  : versification,
                "has_old_testament"     : 1,
                "has_new_testament"     : 1,
                "has_apocrypha"         : 0,
                "has_pseudepigrapha"    : 0
            },
            "archival_info": {
                "translator"            : translator,
                "publication_date"      : publication,
                "copyright"             : copyright,
                "source_format"         : source_format,
                "digital_source"        : digital_source
            }
    },

def build_json_from_txt(input_path, output_path):
    metadata    = []
    verses      = []

    # Verify there's metadata / file exists
    try:
        with open(output_path, 'r+', encoding = 'utf-8') as f:
            logging.debug(f'Opening {output_path} to confirm existance/metadata...')
            json_data = json.load(f)
            metadata  = json_data['metadata']
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
        
        book_dbid = 1 # TODO
        book_name = 0 
        book_subt = ''
        book_code = 0
        section   = 'foo' # TODO: ?
    
        chapter_keyword = input('Chapter keyword/phrase (check doc if necessary): ')
        # chapter_keyword = 'Ĉapitro' 
        chapter     = 0
        verse_num   = 0
        verse_txt   = ''
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
                        verses.append({
                            "uvid"      : f"{book_code}.{chapter}.{verse_num}",
                            "chapter"   : chapter,
                            "verse"     : verse_num,
                            "text"      : verse_txt,
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
        })

    with open(output_path, 'r+', encoding = 'utf-8') as f:
        logging.debug('Adding metadata to file...')
        logging.debug('Adding verses to file...')
        json.dump({'metadata' : metadata, 'verses' : verses}, f)

    return 0

def main(verbose):
    if(1):
        logging.basicConfig(level = logging.DEBUG, format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    else:
        logging.basicConfig(level = logging.WARNING) # Only show errors by default
    
    build_json_from_txt('../bibles/39biblio.mal_formatted.txt', '../bibles/esperanto.json')

    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            prog        = 'txt_to_json.py',
            description = 'a script to transform the bibles in txt format to the json files for the website',
            epilog      = 'made with <3 by ponchoima')

    parser.add_argument('-v', '--verbose', action = 'store_true',
                        help = 'outputs the steps it follows')

    args = parser.parse_args()

    main(args.verbose)
