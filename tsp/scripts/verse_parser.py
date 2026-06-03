# Data for book recognizing (Flat Dictionary: EN, ES, EO)
possible_names = {
    # Genesis
    "génesis": "GEN", "genesis": "GEN", "gen": "GEN", "gn": "GEN", "genezo": "GEN",
    # Exodus
    "éxodo": "EXO", "exodo": "EXO", "exodus": "EXO", "exo": "EXO", "eliro": "EXO",
    # Leviticus
    "levítico": "LEV", "levitico": "LEV", "leviticus": "LEV", "lev": "LEV", "levitiko": "LEV",
    # Numbers
    "números": "NUM", "numeros": "NUM", "numbers": "NUM", "num": "NUM", "nombroj": "NUM",
    # Deuteronomy
    "deuteronomio": "DET", "deuteronomy": "DET", "det": "DET", "readmono": "DET",
    # Joshua
    "josué": "JOS", "josue": "JOS", "joshua": "JOS", "jos": "JOS", "josuo": "JOS",
    # Judges
    "jueces": "JUE", "judges": "JUE", "jue": "JUE", "juĝistoj": "JUE",
    # Ruth
    "rut": "RUT", "ruth": "RUT",
    # 1 Samuel (Handling both spaced and unspaced for parser safety)
    "1 samuel": "1SA", "1samuel": "1SA", "1sa": "1SA", "1 samuelo": "1SA", "1samuelo": "1SA",
    # 2 Samuel
    "2 samuel": "2SA", "2samuel": "2SA", "2sa": "2SA", "2 samuelo": "2SA", "2samuelo": "2SA",
    # 1 Kings
    "1 reyes": "1RE", "1reyes": "1RE", "1 kings": "1RE", "1kings": "1RE", "1re": "1RE", "1 reĝoj": "1RE", "1reĝoj": "1RE",
    # 2 Kings
    "2 reyes": "2RE", "2reyes": "2RE", "2 kings": "2RE", "2kings": "2RE", "2re": "2RE", "2 reĝoj": "2RE", "2reĝoj": "2RE",
    # 1 Chronicles
    "1crónicas": "1CR", "1cronicas": "1CR", "1 chronicles": "1CR", "1chronicles": "1CR", "1cr": "1CR", "1 kroniko": "1CR", "1kroniko": "1CR",
    # 2 Chronicles
    "2crónicas": "2CR", "2cronicas": "2CR", "2 chronicles": "2CR", "2chronicles": "2CR", "2cr": "2CR", "2 kroniko": "2CR", "2kroniko": "2CR",
    # Ezra
    "esdras": "ESD", "ezra": "ESD", "esd": "ESD",
    # Nehemiah
    "nehemías": "NEH", "nehemias": "NEH", "nehemiah": "NEH", "neh": "NEH", "neĥemja": "NEH",
    # Esther
    "ester": "EST", "esther": "EST", "est": "EST",
    # Job
    "job": "JOB",
    # Psalms
    "salmos": "SAL", "psalms": "SAL", "sal": "SAL", "psalmaro": "SAL", "psa": "SAL",
    # Proverbs
    "proverbios": "PRV", "proverbs": "PRV", "prv": "PRV", "sentencoj": "PRV",
    # Ecclesiastes
    "eclesiastés": "ECL", "eclesiastes": "ECL", "ecclesiastes": "ECL", "ecl": "ECL", "predikanto": "ECL",
    # Song of Solomon / Cantares
    "cantares": "CNT", "song of solomon": "CNT", "songofsolomon": "CNT", "cnt": "CNT", "alta kanto": "CNT", "altakanto": "CNT",
    # Isaiah
    "isaías": "ISA", "isaias": "ISA", "isaiah": "ISA", "isa": "ISA", "jesaja": "ISA",
    # Jeremiah
    "jeremías": "JER", "jeremias": "JER", "jeremiah": "JER", "jer": "JER", "jeremia": "JER",
    # Lamentations
    "lamentaciones": "LAM", "lamentations": "LAM", "lam": "LAM", "plorkanto": "LAM",
    # Ezekiel
    "ezequiel": "EZQ", "ezekiel": "EZQ", "ezq": "EZQ", "jeĥezkel": "EZQ",
    # Daniel
    "daniel": "DAN", "dan": "DAN",
    # Hosea
    "oseas": "OSE", "hosea": "OSE", "ose": "OSE", "hoŝea": "OSE",
    # Joel
    "joel": "JOL", "jol": "JOL",
    # Amos
    "amós": "AMO", "amos": "AMO", "amo": "AMO",
    # Obadiah
    "abdías": "ABD", "abdias": "ABD", "obadiah": "ABD", "abd": "ABD", "obadja": "ABD",
    # Jonah
    "jonás": "JON", "jonas": "JON", "jonah": "JON", "jon": "JON", "jona": "JON",
    # Micah
    "miqueas": "MIQ", "micah": "MIQ", "miq": "MIQ", "miĥa": "MIQ",
    # Nahum
    "nahúm": "NAH", "nahum": "NAH", "nah": "NAH", "naĥum": "NAH",
    # Habakkuk
    "habacuc": "HAB", "habakkuk": "HAB", "hab": "HAB", "ĥabakuk": "HAB",
    # Zephaniah
    "sofonías": "SOF", "sofonias": "SOF", "zephaniah": "SOF", "sof": "SOF", "cefanja": "SOF",
    # Haggai
    "hageo": "HAG", "haggai": "HAG", "hag": "HAG", "ĥagaj": "HAG",
    # Zechariah
    "zacarías": "ZAC", "zacarias": "ZAC", "zechariah": "ZAC", "zac": "ZAC", "zeĥarja": "ZAC",
    # Malachi
    "malaquías": "MAL", "malaquias": "MAL", "malachi": "MAL", "mal": "MAL", "malaĥi": "MAL",
    # Matthew
    "mateo": "MAT", "matthew": "MAT", "mat": "MAT",
    # Mark
    "marcos": "MAR", "mark": "MAR", "mar": "MAR", "marko": "MAR",
    # Luke
    "lucas": "LUC", "luke": "LUC", "luc": "LUC", "luko": "LUC",
    # John
    "juan": "JUA", "john": "JUA", "jua": "JUA", "johano": "JUA",
    # Acts
    "hechos": "HCH", "acts": "HCH", "hch": "HCH", "agoj": "HCH",
    # Romans
    "romanos": "ROM", "romans": "ROM", "rom": "ROM",
    # 1 Corinthians
    "1 corintios": "1CO", "1corintios": "1CO", "1 corinthians": "1CO", "1corinthians": "1CO", "1co": "1CO", "1 korintanoj": "1CO", "1korintanoj": "1CO",
    # 2 Corinthians
    "2 corintios": "2CO", "2corintios": "2CO", "2 corinthians": "2CO", "2corinthians": "2CO", "2co": "2CO", "2 korintanoj": "2CO", "2korintanoj": "2CO",
    # Galatians
    "gálatas": "GAL", "galatas": "GAL", "galatians": "GAL", "gal": "GAL", "galatoj": "GAL",
    # Ephesians
    "efesios": "EFE", "ephesians": "EFE", "efe": "EFE", "efesanoj": "EFE",
    # Philippians
    "filipenses": "FIL", "philippians": "FIL", "fil": "FIL", "filipianoj": "FIL",
    # Colossians
    "colosenses": "COL", "colossians": "COL", "col": "COL", "koloseanoj": "COL",
    # 1 Thessalonians
    "1 tesalonicenses": "1TS", "1tesalonicenses": "1TS", "1 thessalonians": "1TS", "1thessalonians": "1TS", "1ts": "1TS", "1 tesalonikanoj": "1TS", "1tesalonikanoj": "1TS",
    # 2 Thessalonians
    "2 tesalonicenses": "2TS", "2tesalonicenses": "2TS", "2 thessalonians": "2TS", "2thessalonians": "2TS", "2ts": "2TS", "2 tesalonikanoj": "2TS", "2tesalonikanoj": "2TS",
    # 1 Timothy
    "1 timoteo": "1TI", "1timoteo": "1TI", "1 timothy": "1TI", "1timothy": "1TI", "1ti": "1TI",
    # 2 Timothy
    "2 timoteo": "2TI", "2timoteo": "2TI", "2 timothy": "2TI", "2timothy": "2TI", "2ti": "2TI",
    # Titus
    "tito": "TIT", "titus": "TIT", "tit": "TIT",
    # Philemon
    "filemón": "FLM", "filemon": "FLM", "philemon": "FLM", "flm": "FLM",
    # Hebrews
    "hebreos": "HEB", "hebrews": "HEB", "heb": "HEB",
    # James
    "santiago": "STG", "james": "STG", "stg": "STG", "jakobo": "STG",
    # 1 Peter
    "1 pedro": "1PE", "1pedro": "1PE", "1 peter": "1PE", "1peter": "1PE", "1pe": "1PE",
    # 2 Peter
    "2 pedro": "2PE", "2pedro": "2PE", "2 peter": "2PE", "2peter": "2PE", "2pe": "2PE",
    # 1 John
    "1 juan": "1JN", "1juan": "1JN", "1 john": "1JN", "1john": "1JN", "1jn": "1JN", "1 johano": "1JN", "1johano": "1JN",
    # 2 John
    "2 juan": "2JN", "2juan": "2JN", "2 john": "2JN", "2john": "2JN", "2jn": "2JN", "2 johano": "2JN", "2johano": "2JN",
    # 3 John
    "3 juan": "3JN", "3juan": "3JN", "3 john": "3JN", "3john": "3JN", "3jn": "3JN", "3 johano": "3JN", "3johano": "3JN",
    # Jude
    "judas": "JUD", "jude": "JUD", "juda": "JUD",
    # Revelation
    "apocalipsis": "APO", "revelation": "APO", "rv": "APO", "rev": "APO", "apo": "APO", "apokalipso": "APO"
}

def get_bible_book(candidate: str) -> str:
    return possible_names.get(candidate)

def get_bible_reference(candidate: str) -> str:
    if('.' in candidate or ':' in candidate):
        # Case for 1:1
        new_verse = '.'.join(candidate.split(':'))
        if('-' in new_verse):
            return new_verse.split('-')[0]
        return new_verse

    # Only chapters
    return candidate + '.1'

def uvid(candidate):
    try:
        # This turns "1 Samuel 1:1" into "1samuel 1:1" so c_verse[0] captures the whole book.
        candidate = candidate.lower().replace("1 ", "1").replace("2 ", "2").replace("3 ", "3")
        
        c_verse = candidate.split()
        book_code = get_bible_book(c_verse[0])
        
        if book_code != None:
            return '.'.join([book_code, get_bible_reference(c_verse[1])])
        return 'invalid'
    except Exception as e:
        raise
    return 'invalid'
