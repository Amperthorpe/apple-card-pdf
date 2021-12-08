from types import SimpleNamespace
StatementFiles = SimpleNamespace()


StatementFiles.sf = [
    "/Users/lex/Downloads/Apple Card Statement - August 2021.pdf",
    "/Users/lex/Downloads/Apple Card Statement - September 2021.pdf",
    "/Users/lex/Downloads/Apple Card Statement - October 2021.pdf",
    "/Users/lex/Downloads/Apple Card Statement - November 2021.pdf"
]

StatementFiles.sr = [
    "/Users/lex/Downloads/Apple Card Statement - May 2021.pdf",
    "/Users/lex/Downloads/Apple Card Statement - June 2021.pdf",
    "/Users/lex/Downloads/Apple Card Statement - July 2021.pdf"
]

merchants = ["TRADER JOES", "PEETS", "LYFT", "GOOGLE", "DOORDASH", "CHIPOTLE",
"TARGET", "PATREON", "SPOTIFY", "CLIPPER", "SHAKE SHACK", "LEMONADE", "FOSTER"] # Merchant names to collect into one



##############################
### CONFIG ABOVE THIS LINE ###
##############################

def get_lists():
    files_dict = StatementFiles.__dict__
    files_dict.pop("lists", None)
    return files_dict

StatementFiles.lists = get_lists