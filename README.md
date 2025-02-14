# **Flashcard Generator with Natural Language Processing**

## **Overview**
The **Flashcard Generator** is a Python-based application designed to **automatically create flashcards** from various learning materials, such as **PDF, Word documents, and plain text files**.
Using **Natural Language Processing (NLP)** techniques and deep learning models, the program extracts key concepts, summarizes text, and generates **interactive flashcards**, aiding in active recall and memory retention.

---

## **Features**
- **Supports Multiple Input Formats**: Works with `.txt`, `.docx`, and `.pdf` files.
- **Summarization & Question Generation**: Uses NLP libraries like **spaCy** and **Hugging Face’s T5 model** to extract key terms and generate fill-in-the-blank questions.
- **Interactive Flashcards**: Users can navigate flashcards with **"Next" and "Previous"** buttons and reveal key terms interactively.
- 🖥**Easy-to-Use Interface**: A simple **GUI (Tkinter)** allows users to upload files and generate flashcards instantly.

---

## **How to Use**
1. **Upload a File**: Click the **"Upload File"** button and select a `.txt`, `.docx`, or `.pdf` file.
2. **Generate Flashcards**: The program will analyze the content and create a set of interactive flashcards.
3. **Interact with Flashcards**:
   - Use **"Next" and "Previous"** buttons to navigate.
   - Click **"Show Term"** to reveal the answer.

---

## **Technologies Used**
| Technology            | Purpose |
|----------------------|------------------------------------------|
| **Python**           | Core programming language |
| **spaCy**            | NLP library for Named Entity Recognition (NER) |
| **Hugging Face**     | T5 model for text summarization & question generation |
| **Tkinter**          | GUI framework for user interaction |
| **pdfplumber**       | Extracting text from PDF files |
| **python-docx**      | Extracting text from Word documents |

---

## **Methodology**
The program follows a **structured NLP pipeline** to transform raw text into flashcards:

1. **Text Preprocessing**: Extracts and splits text into meaningful sections.
2. **Named Entity Recognition (NER)**: Identifies key terms using **spaCy**.
3. **Summarization**: Uses the **T5 model** from Hugging Face to create concise summaries.
4. **Question Generation**: Generates **fill-in-the-blank** questions based on extracted entities and summaries.

The program intelligently processes text, identifies key information, and generates **relevant, quiz-style questions** for each section.
