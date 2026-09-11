import os
import re
from pypdf import PdfReader, PdfWriter

PDF_PATH = "KJV-Holy-Bible-1769.pdf"
OUTPUT_DIR = "books"

def split_bible():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Loading {PDF_PATH}...")
    reader = PdfReader(PDF_PATH)
    outline = reader.outline
    total_pages = len(reader.pages)
    print(f"Total pages: {total_pages}, Books found in outline: {len(outline)}")

    # 1. Front Matter (pages prior to Genesis)
    first_book_page = reader.get_destination_page_number(outline[0])
    if first_book_page > 0:
        front_writer = PdfWriter()
        for p in range(first_book_page):
            front_writer.add_page(reader.pages[p])
        front_path = os.path.join(OUTPUT_DIR, "00_Front_Matter.pdf")
        with open(front_path, "wb") as f:
            front_writer.write(f)
        print(f"[00/66] Saved 00_Front_Matter.pdf (pages 0-{first_book_page - 1})")

    # 2. Extract each of the 66 books
    for i, item in enumerate(outline):
        book_num = i + 1
        title = item.title
        safe_title = re.sub(r"[^A-Za-z0-9_ -]", "", title).strip().replace(" ", "_")
        filename = f"{book_num:02d}_{safe_title}.pdf"

        start_page = reader.get_destination_page_number(item)
        if i + 1 < len(outline):
            end_page = reader.get_destination_page_number(outline[i + 1]) - 1
        else:
            end_page = total_pages - 1

        writer = PdfWriter()
        for p in range(start_page, end_page + 1):
            writer.add_page(reader.pages[p])

        output_path = os.path.join(OUTPUT_DIR, filename)
        with open(output_path, "wb") as f:
            writer.write(f)

        page_count = end_page - start_page + 1
        print(f"[{book_num:02d}/66] Saved {filename} ({page_count} pages, {start_page}-{end_page})")

    print(f"\nSuccessfully extracted 66 books and front matter into '{OUTPUT_DIR}/'.")

if __name__ == "__main__":
    split_bible()
