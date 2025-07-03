from pathlib import Path

# Combine all .md files into one corpus
corpus = []
for md_file in Path("cyber-apocalypse-2024").rglob("*.md"):
    corpus.append(md_file.read_text())

with open("cyber-apocalypse-2024.txt", "w") as f:
    f.write("\n\n".join(corpus))  # Separate files by double newlines