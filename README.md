# Bijoy to Unicode Converter

This repository provides Python tools to convert text and `.docx` files written in the Bijoy (SutonnyMJ) encoding into Unicode Bengali.

## Features

- **Convert `.docx` files:** Preserves the formatting of your Microsoft Word documents while converting Bijoy text to standard Unicode (Kalpurush font). Automatically detects and ignores English text.
- **Convert plain text:** Converts `.txt` files containing raw Bijoy-encoded characters into Unicode.
- **Batch Processing:** Can convert entire directories of `.docx` files at once.

## Prerequisites

- Python 3
- `python-docx` library (required for `.docx` conversion)

Install the required dependencies using pip:
```bash
pip install python-docx
```

## How to Use

### 1. Converting Word Documents (`.docx`)

Use the `convert_docx.py` script to convert Word documents.

**Basic Usage:**
```bash
python convert_docx.py document.docx
```
*This will create a new file named `document (Unicode).docx` in the same directory.*

**Convert multiple files:**
```bash
python convert_docx.py file1.docx file2.docx
```

**Convert an entire directory:**
```bash
python convert_docx.py folder_path/
```

**Specify an output directory:**
```bash
python convert_docx.py document.docx -o output_folder/
```

### 2. Converting Plain Text Files (`.txt`)

Use the `bijoy_to_unicode.py` script for standard text files.

**Basic Usage:**
```bash
python bijoy_to_unicode.py input.txt
```
*This will output to `input_unicode.txt`.*

**Specify output file:**
```bash
python bijoy_to_unicode.py input.txt output.txt
```
