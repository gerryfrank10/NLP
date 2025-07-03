from pathlib import Path
from tika import parser

for pdf_file in Path('hacking-books/').glob("*.pdf"):
    print(f"Processing {pdf_file.name}...")

    parsed = parser.from_file(str(pdf_file))  # Pass the file path, not file object
    content = parsed.get("content", "").strip()

    if content:
        txt_file = pdf_file.with_suffix(".txt")
        with open(txt_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Saved to {txt_file.name}")
    else:
        print(f"No content extracted from {pdf_file.name}")