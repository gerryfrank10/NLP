from pathlib import Path

# Combine all .md files into one corpus
corpus = []
for md_file in Path("ctf-wiki-en").rglob("*.md"):
    corpus.append(md_file.read_text())

with open("scraped_pages/ctf-wiki.txt", "w") as f:
    f.write("\n\n".join(corpus))  # Separate files by double newlines