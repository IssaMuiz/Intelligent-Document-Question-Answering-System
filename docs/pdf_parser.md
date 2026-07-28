# 02. PDF Parser

## Overview

The PDF Parser is the first core component of the Intelligent Document Question Answering System. Its responsibility is to read PDF documents and convert them into a structured Python representation that can be consumed by downstream components such as the text preprocessor, chunker, embedding generator, vector database, retriever, and Large Language Model (LLM).

The parser is designed with modularity and extensibility in mind. Rather than simply extracting raw text, it produces structured document information while separating different responsibilities into dedicated methods.

---

# Objectives

The objectives of the PDF Parser are to:

- Read PDF documents from disk.
- Extract document metadata.
- Extract text from every page.
- Preserve page-level information.
- Return a structured representation of the document.
- Serve as the entry point of the RAG pipeline.

---

# Why PDF Parsing Matters

PDF files are one of the most common formats used to distribute books, research papers, manuals, reports, and business documents. However, a PDF is not plain text—it contains layout information, fonts, images, and other document elements.

Before a document can be processed by an LLM, its textual content must first be extracted into a machine-readable format.

The PDF Parser performs this transformation.

---

# Design Philosophy

The parser follows several software engineering principles.

## 1. Single Responsibility Principle (SRP)

Each method performs one specific task.

- parse() coordinates the parsing workflow.
- extract_metadata() extracts document metadata.
- extract_pages() extracts page information.
- extract_text() extracts text from a single page.

This makes the code easier to maintain, test, and extend.

---

## 2. Separation of Concerns

The parser only extracts information.

It does **not**:

- clean text
- remove empty pages
- split text into chunks
- generate embeddings
- answer questions

Those responsibilities belong to later stages of the pipeline.

---

## 3. Modularity

The parser is implemented as a reusable Python class.

```python
parser = PDFParser()

document = parser.parse("Atomic Habits.pdf")
```

This allows the parser to be reused by different applications without modification.

---

# Parser Architecture

```
PDF File
    │
    ▼
PDFParser.parse()
    │
    ├──────────────┐
    ▼              ▼
extract_metadata() extract_pages()
                       │
                       ▼
                extract_text()
                       │
                       ▼
             Structured Document
```

---

# Parser Workflow

The parser follows the workflow below.

1. Open the PDF document.
2. Read document metadata.
3. Iterate through every page.
4. Extract page text.
5. Compute page statistics.
6. Build a structured document dictionary.
7. Return the parsed document.

---

# Methods

## parse()

Coordinates the complete parsing process.

Responsibilities:

- Open the PDF.
- Call metadata extraction.
- Call page extraction.
- Build the final document structure.
- Return the parsed document.

---

## extract_metadata()

Extracts metadata stored inside the PDF.

Currently extracted fields include:

- title
- author
- subject
- keywords
- creator
- producer
- creation_date
- modified_date
- pdf_format

The metadata is normalized into Python's snake_case naming convention.

---

## extract_pages()

Processes every page in the document.

For each page it extracts:

- page number
- page text
- word count
- character count
- has_text flag

Each page is represented as a dictionary.

---

## extract_text()

Extracts plain text from an individual page using PyMuPDF.

Current implementation:

```python
page.get_text("text")
```

The extraction method is isolated into its own function so it can easily be replaced by other extraction strategies in the future.

---

# Output Structure

The parser returns a dictionary with the following structure.

```python
{
    "filename": "...",
    "filepath": "...",
    "page_count": 256,
    "metadata": {...},
    "pages": [
        {
            "page_number": 1,
            "text": "...",
            "word_count": 120,
            "character_count": 750,
            "has_text": True
        },
        ...
    ]
}
```

This structured representation serves as the standard input for the remainder of the RAG pipeline.

---

# Design Decisions

## Why use a class instead of standalone functions?

A class provides a clean interface and allows future parser implementations (e.g., DOCXParser, TXTParser, PPTXParser) to follow the same design.

---

## Why keep extract_text() separate?

Although text extraction currently consists of a single line of code, isolating it behind a dedicated method makes it easy to replace or improve the extraction strategy later without modifying other parts of the parser.

---

## Why preserve page information?

Keeping page numbers enables source attribution during retrieval.

Example:

> Source: Atomic Habits, Page 127.

This improves transparency and allows users to verify generated answers.

---

## Why return structured data instead of raw text?

Returning structured data allows downstream components to access both document-level and page-level information without reprocessing the original PDF.

---

## Why doesn't the parser clean text?

Cleaning is intentionally excluded from the parser.

The parser's responsibility is to faithfully extract information from the document.

Cleaning, normalization, and filtering belong to the preprocessing stage.

This separation follows the Single Responsibility Principle.

---

# Current Capabilities

The current parser can:

- Read PDF documents.
- Extract metadata.
- Extract text from every page.
- Preserve page-level information.
- Compute page statistics.
- Return a structured document representation.

---

# Current Limitations

The current implementation does not yet support:

- OCR for scanned PDFs.
- Table extraction.
- Image extraction.
- Hyperlink extraction.
- Multi-column reading optimization.
- Header and footer detection.
- Layout preservation.
- Form field extraction.

These features may be added in future versions.

---

# Lessons Learned

Building the parser from scratch provided several important insights:

- A parser should expose a clean interface rather than simply returning raw text.
- Modular design makes future extensions significantly easier.
- Separating responsibilities leads to cleaner and more maintainable code.
- Structured outputs provide much greater flexibility for downstream components.

---

# Next Step

With a working parser in place, the next stage of the project is **Text Preprocessing**.

The preprocessing module will analyze and clean the extracted text before it is divided into chunks for embedding generation and semantic retrieval.