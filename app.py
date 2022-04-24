import pdfplumber
path_pdf = 'Lib/Curricula.pdf'

if __name__ == "__main__":
    with pdfplumber.open(path_pdf) as pdf:
        print(pdf.pages)
        print()
        page = pdf.pages[2]
        table = page.extract_table()
        print(table)
        print()
        text = page.extract_text()
        print(text)
        print()
