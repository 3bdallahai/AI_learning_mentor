import fitz

def extrcat_text_from_pdf(file_path: str)-> str:
    text = ""

    with fitz.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text

def extract_text_from_txt(file_path: str) -> str:
    text= ""
    with open(file_path, "r",encoding="utf-8") as f:
        return f.read()