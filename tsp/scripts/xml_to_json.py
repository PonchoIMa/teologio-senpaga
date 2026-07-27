# xml to json
import xml.etree.ElementTree as ET
import json, os, re

# The Protestant 66-book mapping (1 to 66) to Universal Verse ID codes
BOOK_MAP = {
    1: 'GEN', 2: 'EXO', 3: 'LEV', 4: 'NUM', 5: 'DET', 6: 'JOS', 7: 'JUE', 8: 'RUT',
    9: '1SA', 10: '2SA', 11: '1RE', 12: '2RE', 13: '1CR', 14: '2CR', 15: 'ESD',
    16: 'NEH', 17: 'EST', 18: 'JOB', 19: 'SAL', 20: 'PRV', 21: 'ECL', 22: 'CNT',
    23: 'ISA', 24: 'JER', 25: 'LAM', 26: 'EZQ', 27: 'DAN', 28: 'OSE', 29: 'JOL',
    30: 'AMO', 31: 'ABD', 32: 'JON', 33: 'MIQ', 34: 'NAH', 35: 'HAB', 36: 'SOF',
    37: 'HAG', 38: 'ZAC', 39: 'MAL', 40: 'MAT', 41: 'MAR', 42: 'LUC', 43: 'JUA',
    44: 'HCH', 45: 'ROM', 46: '1CO', 47: '2CO', 48: 'GAL', 49: 'EFE', 50: 'FIL',
    51: 'COL', 52: '1TS', 53: '2TS', 54: '1TI', 55: '2TI', 56: 'TIT', 57: 'FLM',
    58: 'HEB', 59: 'STG', 60: '1PE', 61: '2PE', 62: '1JN', 63: '2JN', 64: '3JN',
    65: 'JUD', 66: 'APO'
}

# Provide fallback display names for the book_name column based on the UVID
BOOK_NAMES = {
    'GEN': 'Genezo', 'EXO': 'Eliro', 'LEV': 'Levitiko', 'NUM': 'Nombroj', 'DET': 'Readmono',
    'JOS': 'Josuo', 'JUE': 'Juĝistoj', 'RUT': 'Rut', '1SA': '1 Samuelo', '2SA': '2 Samuelo',
    '1RE': '1 Reĝoj', '2RE': '2 Reĝoj', '1CR': '1 Kroniko', '2CR': '2 Kroniko', 'ESD': 'Esdras',
    'NEH': 'Neĥemja', 'EST': 'Ester', 'JOB': 'Ijob', 'SAL': 'Psalmaro', 'PRV': 'Sentencoj',
    'ECL': 'Predikanto', 'CNT': 'Alta Kanto', 'ISA': 'Jesaja', 'JER': 'Jeremia', 'LAM': 'Plorkanto',
    'EZQ': 'Jeĥezkel', 'DAN': 'Daniel', 'OSE': 'Hoŝea', 'JOL': 'Joel', 'AMO': 'Amos',
    'ABD': 'Obadja', 'JON': 'Jona', 'MIQ': 'Miĥa', 'NAH': 'Naĥum', 'HAB': 'Ĥabakuk',
    'SOF': 'Cefanja', 'HAG': 'Ĥagaj', 'ZAC': 'Zeĥarja', 'MAL': 'Malaĥi', 'MAT': 'Mateo',
    'MAR': 'Marko', 'LUC': 'Luko', 'JUA': 'Johano', 'HCH': 'Agoj', 'ROM': 'Romanoj',
    '1CO': '1 Korintanoj', '2CO': '2 Korintanoj', 'GAL': 'Galatoj', 'EFE': 'Efesanoj', 'FIL': 'Filipianoj',
    'COL': 'Koloseanoj', '1TS': '1 Tesalonikanoj', '2TS': '2 Tesalonikanoj', '1TI': '1 Timoteo',
    '2TI': '2 Timoteo', 'TIT': 'Tito', 'FLM': 'Filemon', 'HEB': 'Hebreoj', 'STG': 'Jakobo',
    '1PE': '1 Petro', '2PE': '2 Petro', '1JN': '1 Johano', '2JN': '2 Johano', '3JN': '3 Johano',
    'JUD': 'Juda', 'APO': 'Apokalipso'
}

# Configuration for your specific files to ensure accurate metadata
FILES_CONFIG = {
    '../data/bibles/EsperantoBible.xml':     {'abbr': 'ESP', 'lang': 'eo', 'desc': 'La Sankta Biblio 1926'},
    '../data/bibles/SpanishNBLABible.xml':   {'abbr': 'NBLA', 'lang': 'es', 'desc': 'Nueva Biblia de las Américas'},
    '../data/bibles/EnglishKJBible.xml':     {'abbr': 'KJV', 'lang': 'en', 'desc': 'King James Version'},
    '../data/bibles/RussianSynodalBible.xml':{'abbr': 'SYN', 'lang': 'ru', 'desc': 'Russian Synodal 1876'}
}

def parse_bible_xml(xml_filename, config):
    print(f"Parsing {xml_filename}...")
    
    tree = ET.parse(xml_filename)
    root = tree.getroot()
    
    # Extract root metadata
    translation_title = root.attrib.get('translation', config['desc'])
    copyright_status = root.attrib.get('status', 'Public Domain')
    
    # Exact JSON metadata block structure
    json_output = {
        "metadata": {
            "abbreviation": config['abbr'],
            "title_full": translation_title,
            "verse_system": "Protestant",
            "language_code": config['lang'],
            "copyright": copyright_status,
            "description": config['desc'],
            "publication_date": "TBD"
        },
        "verses": []
    }
    
    # Iterate through all testaments -> books -> chapters -> verses
    for testament in root.findall('.//testament'):
        for book in testament.findall('book'):
            book_num = int(book.attrib['number'])
            
            # Restrict to standard 66 book canon
            if book_num not in BOOK_MAP:
                continue
                
            book_code = BOOK_MAP[book_num]
            book_display_name = BOOK_NAMES.get(book_code, book_code)
            
            for chapter in book.findall('chapter'):
                chapter_num = int(chapter.attrib['number'])
                
                for verse in chapter.findall('verse'):
                    verse_num = int(verse.attrib['number'])
                    # Safe text extraction to avoid the cut-off letter bug
                    if verse.text:
                        verse_text = re.sub(r'([,.:;])([^ ])', r'\g<1> \g<2>', verse.text.strip()) 
                    else:
                        verse_text = ''

                    # Target UVID construction
                    uvid = f"{book_code}.{chapter_num}.{verse_num}"
                    
                    # Append strictly structured dictionary
                    json_output["verses"].append({
                        "uvid": uvid,
                        "book_name": book_display_name,
                        "chapter": chapter_num,
                        "verse": verse_num,
                        "text": verse_text,
                        "pericope": ""
                    })
                
    output_filename = f"../data/bibles/{config['abbr']}_{config['lang']}.json"
    
    # Ensure data directory exists
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        # Use separators=(',', ': ') to keep the output highly compressed but readable
        json.dump(json_output, f, ensure_ascii=False, separators=(',', ': '))
        
    print(f"Successfully created {output_filename} with {len(json_output['verses'])} verses!")

if(__name__ == "__main__"):
    for xml_file, config in FILES_CONFIG.items():
        if os.path.exists(xml_file):
            parse_bible_xml(xml_file, config)
        else:
            print(f"File not found: {xml_file} (Skipping...)")
