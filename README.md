Flashcard Generator with Natural Language Processing
Overview
The Flashcard Generator is a Python-based application designed to automatically create flashcards from various types of learning materials, such as PDF, Word documents, and plain text files. By using Natural Language Processing (NLP) techniques and deep learning models, this program summarizes inputted text and generates interactive flashcards, aiding in active recall and memory retention.
Features
•	Supports Multiple Input Formats: The program can process files in .txt, .docx, and .pdf formats.
•	Summarization & Question Generation: Using NLP libraries like spaCy and Hugging Face’s T5 model, the program extracts key terms and generates fill-in-the-blank questions.
•	Interactive Flashcards: Users can interact with flashcards, revealing key terms and navigating between cards using a simple GUI built with Tkinter.
•	Easy-to-use Interface: Users can upload files and instantly get interactive flashcards to enhance learning.
Generating Flashcards
•	Upload a File: Use the "Upload File" button to choose your .txt, .docx, or .pdf file.
•	Generate Flashcards: The program will process the file and create a set of flashcards based on the content.
•	Interact with Flashcards: Navigate through the flashcards using "Next" and "Previous" buttons. Click "Show Term" to reveal the answer on each card.
Technologies Used
•	Python: The core language used for developing the application.
•	spaCy: A fast NLP library used for Named Entity Recognition (NER) and extracting key terms from the text.
•	Hugging Face Transformers: Used for text summarization and question generation with pre-trained models like T5.
•	Tkinter: Used for the graphical user interface (GUI), allowing users to upload files and interact with flashcards.
•	pdfplumber: Used for extracting text from PDF files.
•	python-docx: Used for reading and extracting text from Word (.docx) documents.
Methodology
This project uses Natural Language Processing (NLP) and deep learning techniques to create flashcards automatically:
•	Text Preprocessing: Extracts and splits text into meaningful sections.
•	Named Entity Recognition (NER): Extracts key terms from the text using spaCy.
•	Summarization: Uses the T5 model from Hugging Face to create concise summaries of the text.
•	Question Generation: Generates fill-in-the-blank questions based on the extracted entities and summaries. The program processes the text, identifies important information, and generates relevant questions for each section.

