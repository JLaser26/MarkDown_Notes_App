import markdown, pypandoc, os

NOTES_DIR = "notes"

if not os.path.exists(NOTES_DIR): os.makedirs(NOTES_DIR)

def create_note():
    title = input("Enter note title: ").strip()
    filename = os.path.join(NOTES_DIR, f"{title}.md")

    print("Write your note below. Type '---END---' on a new line to finish:")
    lines = []
    while True:
        line = input()
        if line.strip() == "---END---":
            break
        lines.append(line)

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Note saved as {filename}")

def list_notes():
    notes = [f for f in os.listdir(NOTES_DIR) if f.endswith(".md")]
    if not notes:
        print("No notes found.")
        return []
    print("\n📂 Saved Notes:")
    for idx, note in enumerate(notes, start=1):
        print(f"{idx}. {note}")
    return notes


def view_note():
    notes = list_notes()
    if not notes:
        return
    choice = int(input("Enter note number to view: ")) - 1
    if 0 <= choice < len(notes):
        with open(os.path.join(NOTES_DIR, notes[choice]), "r", encoding="utf-8") as f:
            print("\n" + f.read())
    else:
        print("Invalid choice.")


def search_notes():
    keyword = input("Enter keyword to search: ").lower()
    notes = [f for f in os.listdir(NOTES_DIR) if f.endswith(".md")]
    found = []
    for note in notes:
        with open(os.path.join(NOTES_DIR, note), "r", encoding="utf-8") as f:
            content = f.read().lower()
            if keyword in content or keyword in note.lower():
                found.append(note)

    if found:
        print("\n🔍 Found in:")
        for note in found:
            print(f"- {note}")
    else:
        print("No matches found.")


def export_note():
    notes = list_notes()
    if not notes:
        return
    choice = int(input("Enter note number to export: ")) - 1
    if 0 <= choice < len(notes):
        filepath = os.path.join(NOTES_DIR, notes[choice])
        with open(filepath, "r", encoding="utf-8") as f:
            md_content = f.read()

        # Convert Markdown → HTML
        html_content = markdown.markdown(md_content)
        html_file = filepath.replace(".md", ".html")
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_content)

        # Convert Markdown → PDF (requires Pandoc installed)
        pdf_file = filepath.replace(".md", ".pdf")
        try:
            pypandoc.convert_text(md_content, "pdf", format="md", outputfile=pdf_file)
            print(f"✅ Exported to {html_file} and {pdf_file}")
        except Exception:
            print("⚠️ PDF export failed (install Pandoc). HTML export successful.")

    else:
        print("Invalid choice.")


def main():
    while True:
        print("\n===== Markdown Notes App =====")
        print("1. Create Note")
        print("2. View Notes")
        print("3. Search Notes")
        print("4. Export Note")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            create_note()
        elif choice == "2":
            view_note()
        elif choice == "3":
            search_notes()
        elif choice == "4":
            export_note()
        elif choice == "5":
            print("Goodbye! 👋")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
