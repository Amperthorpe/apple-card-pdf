import re, sys
import PyPDF2 as pdf
from utilities import Transaction, money_int_to_str, interactive

from config import StatementFiles, merchants

# Written for use with Apple Card monthly statement PDF files.

@interactive
def main(args):
    def parse_statements(statement_files: list[str], results_file: str):
        """Parse Apple Card statement PDF files into a results output file with sorted totals for each merchant."""
        transaction_pages = []
        for file in statement_files:
            reader = pdf.PdfFileReader(file)
            num_pages = reader.getNumPages()
            page_texts = []
            for p in range(num_pages):
                page: pdf.pdf.PageObject = reader.getPage(p)
                page_texts.append(page.extractText())

            transaction_pages.extend(page_texts[1:-2]) # First page and last two pages do not contain transactions

        transaction_list: list[Transaction] = []
        for page in transaction_pages:
            lines = page.split('\n')
            for i, line in enumerate(lines):
                if re.match("\d+\/\d+\/\d+", line): # Matches date format, 00/00/0000

                    try: # If a value doesn't match, transaction is invalid.
                        transaction_list.append(Transaction( # If date matches, next 4 lines are details of a transaction.
                            lines[i],
                            lines[i+1],
                            lines[i+2],
                            lines[i+3],
                            lines[i+4]
                        ))
                    except ValueError:
                        continue

        sorted_transactions = sorted(transaction_list, key=lambda transaction: transaction.desc)

        transaction_dict = {}
        for trans in sorted_transactions:
            found_merchant = False
            for m in merchants:
                if m in trans.desc:
                    found_merchant = True
                    if m not in transaction_dict:
                        transaction_dict[m] = []
                    transaction_dict[m].append(trans)
            if not found_merchant:
                if trans.desc not in transaction_dict:
                    transaction_dict[trans.desc] = []
                transaction_dict[trans.desc].append(trans)

        totals_tuple_list = [ 
            ( t_key, sum( [t.money for t in t_value] ) ) 
            for (t_key, t_value) 
            in transaction_dict.items()
        ]

        sorted_totals_list = sorted(totals_tuple_list, key=lambda t: t[1], reverse=True)

        with open(results_file, 'w') as f:
            for desc, price in sorted_totals_list:
                f.write(f"{money_int_to_str(price):9} {desc}\n")


    # Handle commandline arguments.
    if "--files" in args: # Use files explictly stated in arguments.
        for i, arg in enumerate(args):
            if arg == "--files":
                files = args[i+1:] # Files are every argument after this one.
                parse_statements(files, "results_files.txt")
    elif "-c" in args: # Use files from config.py
        files_dict = StatementFiles.lists()
        for name, files_list in files_dict.items():
            parse_statements(files_list, f"results_{name}.txt")

if __name__ == "__main__":
    main(sys.argv)