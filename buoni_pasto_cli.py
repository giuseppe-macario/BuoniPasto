import sys
from buoni_pasto_core import elabora_pdf

def main():
    if len(sys.argv) < 2:
        print("Errore: specifica un file PDF.\nUso: python buoni_pasto_cli.py <file.pdf>")
        sys.exit(2)

    pdf_path = sys.argv[1]
    result = elabora_pdf(pdf_path)
    # elabora_pdf ritorna già tutti i messaggi e la tabella come stringa
    print(result, end="")

if __name__ == "__main__":
    main()

