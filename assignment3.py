import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')

class Book:
    def __init__(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status

    def __str__(self):
        return f"{self.title} by {self.author} | ISBN: {self.isbn} | Status: {self.status}"

    def to_dict(self):
        return {"title": self.title, "author": self.author, "isbn": self.isbn, "status": self.status}

    def issue(self):
        if self.status == "available":
            self.status = "issued"
            return True
        return False

    def return_book(self):
        if self.status == "issued":
            self.status = "available"
            return True
        return False

    def is_available(self):
        return self.status == "available"

class LibraryInventory:
    def __init__(self, file_path="books.json"):
        self.file_path = Path(file_path)
        self.books = []
        self.load_books()

    def add_book(self, book):
        self.books.append(book)
        self.save_books()
        logging.info(f"Book added: {book.title}")

    def search_by_title(self, title):
        return [b for b in self.books if title.lower() in b.title.lower()]

    def search_by_isbn(self, isbn):
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def display_all(self):
        return self.books

    def save_books(self):
        try:
            with self.file_path.open("w") as f:
                json.dump([b.to_dict() for b in self.books], f, indent=4)
        except Exception as e:
            logging.error(f"Error saving books: {e}")

    def load_books(self):
        if not self.file_path.exists():
            self.books = []
            return
        try:
            with self.file_path.open("r") as f:
                data = json.load(f)
                self.books = [Book(**b) for b in data]
        except Exception as e:
            logging.error(f"Error loading books: {e}")
            self.books = []

inventory = LibraryInventory()

def menu():
    while True:
        print("\nLibrary Inventory Manager")
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. View All Books")
        print("5. Search Book")
        print("6. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            title = input("Title: ")
            author = input("Author: ")
            isbn = input("ISBN: ")
            inventory.add_book(Book(title, author, isbn))
        elif choice == "2":
            isbn = input("Enter ISBN to issue: ")
            book = inventory.search_by_isbn(isbn)
            if book and book.issue():
                inventory.save_books()
                print(f"Issued: {book.title}")
            else:
                print("Book not available or not found.")
        elif choice == "3":
            isbn = input("Enter ISBN to return: ")
            book = inventory.search_by_isbn(isbn)
            if book and book.return_book():
                inventory.save_books()
                print(f"Returned: {book.title}")
            else:
                print("Book not found or not issued.")
        elif choice == "4":
            books = inventory.display_all()
            for b in books:
                print(b)
        elif choice == "5":
            keyword = input("Search by title: ")
            results = inventory.search_by_title(keyword)
            for b in results:
                print(b)
            if not results:
                print("No books found.")
        elif choice == "6":
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    menu()
