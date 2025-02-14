import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os
import re
import pdfplumber
from PIL import Image, ImageTk

try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
except ModuleNotFoundError:
    messagebox.showerror("Error", "The spaCy library is not installed. Please install it using 'pip install spacy'.")
    exit()

try:
    from docx import Document
    from transformers import pipeline
except ImportError:
    messagebox.showerror("Error", "Required libraries are not installed. Use 'pip install python-docx transformers torch sentencepiece pdfplumber pillow'.")
    exit()

try:
    summarizer = pipeline("summarization", model="t5-small")
    question_generator = pipeline("text2text-generation", model="t5-small", tokenizer="t5-small")
except Exception as e:
    messagebox.showerror("Error", f"Failed to load NLP models: {e}")
    exit()

def preprocess_text(text):
    sections = [section.strip() for section in text.split("\n\n") if section.strip()]
    return sections

def clean_summary(summary):
    sentences = summary.split('. ')
    unique_sentences = []
    seen_sentences = set()

    for sentence in sentences:
        sentence = sentence.strip()
        if sentence and sentence not in seen_sentences:
            seen_sentences.add(sentence)
            if not sentence[0].isupper():
                sentence = sentence[0].upper() + sentence[1:]
            unique_sentences.append(sentence)

    return '. '.join(unique_sentences)

def summarize_text(text):
    try:
        input_length = len(text.split())
        max_length = max(50, min(200, int(input_length * 0.9)))
        min_length = max(30, int(max_length * 0.7))

        summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        cleaned_summary = clean_summary(summary[0]['summary_text'])
        return cleaned_summary
    except Exception as e:
        return text

def generate_question(text):
    try:
        question = question_generator(f"question: {text}", max_length=200, min_length=50, do_sample=False)
        return question[0]['generated_text']
    except Exception as e:
        return f"What is {text}?"

def extract_key_terms(doc):
    entities = [ent.text for ent in doc.ents if ent.label_ not in ["CARDINAL", "QUANTITY", "DATE", "TIME"]]

    if not entities:
        noun_chunks = [chunk.text for chunk in doc.noun_chunks if len(chunk.text.split()) > 1 or chunk.text.istitle()]
        entities = noun_chunks

    unique_terms = list(dict.fromkeys(entities))
    return unique_terms

def extract_flashcards(text):
    sections = preprocess_text(text)
    flashcards = []

    for section in sections:
        summarized = summarize_text(section)
        doc = nlp(summarized)
        key_terms = extract_key_terms(doc)

        if key_terms:
            term = key_terms[0]
            definition = summarized.replace(term, "______", 1)
            flashcards.append((definition, term))
        else:
            combined_text = " ".join(section.split(". ")[:2])
            question = generate_question(combined_text)
            flashcards.append((question, combined_text))

    return flashcards

def refine_word_text(doc):
    paragraphs = [para.text.strip() for para in doc.paragraphs if para.text.strip()]
    return "\n\n".join(paragraphs)

def refine_pdf_text(text):
    lines = text.splitlines()
    refined_lines = [line.strip() for line in lines if line.strip() and not line.isspace()]
    refined_text = " ".join(refined_lines)
    paragraphs = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\n)\s+', refined_text)
    return "\n\n".join(paragraphs)

def extract_text_from_pdf(filename):
    with pdfplumber.open(filename) as pdf:
        raw_text = "\n\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    return refine_pdf_text(raw_text)

def read_file(filename):
    _, ext = os.path.splitext(filename)
    if ext.lower() == ".txt":
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    elif ext.lower() == ".docx":
        doc = Document(filename)
        return refine_word_text(doc)
    elif ext.lower() == ".pdf":
        return extract_text_from_pdf(filename)
    else:
        raise ValueError("Unsupported file type.")

def show_flashcard(flashcards, index):
    if index < 0 or index >= len(flashcards):
        messagebox.showinfo("End", "No more flashcards.")
        return

    definition_with_blank, term = flashcards[index]

    def show_term():
        flashcard_label.config(text=f"Correct Answer: {term}", bg="#fbe4d5", fg="#d14b24")
        flip_button.config(text="Next", command=next_flashcard)

    def next_flashcard():
        flashcard_window.destroy()
        show_flashcard(flashcards, index + 1)

    flashcard_window = tk.Toplevel()
    flashcard_window.title(f"Flashcard {index + 1}")
    flashcard_window.configure(bg="#f5f5f5")

    try:
        img = Image.open("flashcard_image.png")
        img = img.resize((100, 100))
        photo = ImageTk.PhotoImage(img)
        img_label = tk.Label(flashcard_window, image=photo, bg="#f5f5f5")
        img_label.image = photo
        img_label.pack(pady=10)
    except FileNotFoundError:
        pass

    flashcard_label = tk.Label(flashcard_window, text=f"Definition: {definition_with_blank}", font=("Arial", 14, "bold"), wraplength=400, bg="#fbe4d5", fg="#d14b24", padx=10, pady=10)
    flashcard_label.pack(pady=20)

    flip_button = tk.Button(flashcard_window, text="Show Term", font=("Arial", 12), bg="#fddfa3", fg="#5a3e1f", command=show_term)
    flip_button.pack(pady=10)

    navigation_frame = tk.Frame(flashcard_window, bg="#f5f5f5")
    navigation_frame.pack(pady=10)

    prev_button = tk.Button(navigation_frame, text="Previous", font=("Arial", 12), bg="#c5dce7", fg="#2e658d", command=lambda: [flashcard_window.destroy(), show_flashcard(flashcards, index - 1)])
    prev_button.pack(side="left", padx=10)

    next_button = tk.Button(navigation_frame, text="Next", font=("Arial", 12), bg="#c5dce7", fg="#2e658d", command=lambda: [flashcard_window.destroy(), show_flashcard(flashcards, index + 1)])
    next_button.pack(side="right", padx=10)

def upload_file():
    filename = filedialog.askopenfilename(filetypes=[
        ("Supported Files", "*.txt *.docx *.pdf"),
        ("Text Files", "*.txt"),
        ("Word Documents", "*.docx"),
        ("PDF Files", "*.pdf")
    ])
    if not filename:
        return

    try:
        text = read_file(filename)
        flashcards = extract_flashcards(text)
        if flashcards:
            show_flashcard(flashcards, 0)
        else:
            messagebox.showinfo("No Flashcards", "No flashcards could be generated from the text.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process the file: {e}")

def main():
    root = tk.Tk()
    root.title("Flashcard Generator")

    style = ttk.Style()
    style.configure("TButton", font=("Arial", 12), padding=6)
    style.configure("TLabel", font=("Arial", 14))

    root.configure(bg="#eef2f3")

    title_label = tk.Label(root, text="Flashcard Generator", font=("Arial", 18, "bold"), bg="#eef2f3", fg="#2e658d")
    title_label.pack(pady=10)

    instruction_label = ttk.Label(root, text="Upload a text, Word, or PDF file to generate flashcards:")
    instruction_label.pack(pady=20)

    upload_button = tk.Button(root, text="Upload File", command=upload_file, font=("Arial", 14), bg="#90caf9", fg="#0d47a1", padx=10, pady=5)
    upload_button.pack(pady=10)

    root.geometry("500x300")
    root.mainloop()

if __name__ == "__main__":
    main()
