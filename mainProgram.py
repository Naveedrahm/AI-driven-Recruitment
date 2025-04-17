import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer, util
import os

def extract_text_from_pdf(file_path):
    with fitz.open(file_path) as doc:
        text = ''
        for page in doc:
            text += page.get_text()
        return text

def read_cv(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        raise ValueError("Endast PDF eller TXT-filer stöds just nu.")

def main():
    # Ladda jobbannons
    with open("job_description.txt", "r", encoding="utf-8") as f:
        job_text = f.read()

    # Ladda CV (byt ut med rätt filnamn)
    cv_path = input("Ange sökväg till CV (PDF eller TXT): ")
    cv_text = read_cv(cv_path)

    # Initiera BERT-modellen
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Skapa vektorrepresentationer
    job_embedding = model.encode(job_text, convert_to_tensor=True)
    cv_embedding = model.encode(cv_text, convert_to_tensor=True)

    # Beräkna likhet
    similarity = util.pytorch_cos_sim(cv_embedding, job_embedding).item()
    score = round(similarity * 100, 2)

    print(f"\n Matchningspoäng: {score} / 100")

    if score >= 75:
        print("CV:t matchar mycket bra med jobbannonsen.")
    elif score >= 50:
        print("Viss matchning finns – kan vara relevant kandidat.")
    else:
        print("Låg matchning – rekommenderas ej för denna roll.")

if __name__ == "__main__":
    main()
