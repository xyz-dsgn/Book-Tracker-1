import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class BookTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.books = []
        self.load_books()

        # --- Создание виджетов ---
        self.create_widgets()
        self.update_listbox()

    def create_widgets(self):
        # Поля ввода
        tk.Label(self.root, text="Название:").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = tk.Entry(self.root, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Автор:").grid(row=1, column=0, padx=5, pady=5)
        self.author_entry = tk.Entry(self.root, width=30)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Жанр:").grid(row=2, column=0, padx=5, pady=5)
        self.genre_entry = tk.Entry(self.root, width=30)
        self.genre_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Страниц:").grid(row=3, column=0, padx=5, pady=5)
        self.pages_entry = tk.Entry(self.root, width=30)
        self.pages_entry.grid(row=3, column=1, padx=5, pady=5)

        # Кнопка добавления
        self.add_btn = tk.Button(self.root, text="Добавить книгу", command=self.add_book)
        self.add_btn.grid(row=4, column=0, columnspan=2, pady=10)

        # Фильтрация
        tk.Label(self.root, text="Фильтр по жанру:").grid(row=5, column=0, padx=5, pady=5)
        self.filter_genre = tk.Entry(self.root, width=30)
        self.filter_genre.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Мин. страниц:").grid(row=6, column=0, padx=5, pady=5)
        self.filter_pages = tk.Entry(self.root, width=30)
        self.filter_pages.grid(row=6, column=1, padx=5, pady=5)

        self.filter_btn = tk.Button(self.root, text="Применить фильтр", command=self.apply_filter)
        self.filter_btn.grid(row=7, column=0, columnspan=2, pady=10)

        # Список книг
        self.books_listbox = tk.Listbox(self.root, width=60, height=15)
        self.books_listbox.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

    def add_book(self):
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages = self.pages_entry.get().strip()

        if not title or not author or not genre or not pages:
            messagebox.showerror("Ошибка", "Все поля обязательны для заполнения!")
            return

        if not pages.isdigit():
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
            return

        book = {
            "title": title,
            "author": author,
            "genre": genre,
            "pages": int(pages)
        }

        self.books.append(book)
        self.save_books()
        self.update_listbox()

    def apply_filter(self):
        genre_filter = self.filter_genre.get().strip().lower()
        try:
            pages_filter = int(self.filter_pages.get().strip())
        except:
            pages_filter = 0

        filtered_books = [
            b for b in self.books
            if (not genre_filter or genre_filter in b["genre"].lower())
            and (pages_filter == 0 or b["pages"] >= pages_filter)
        ]

        self.display_books(filtered_books)

    def update_listbox(self):
        self.display_books(self.books)

    def display_books(self, books_list):
        self.books_listbox.delete(0, tk.END)
        for book in books_list:
            line = f"{book['title']} | {book['author']} | {book['genre']} | {book['pages']} стр."
            self.books_listbox.insert(tk.END, line)

    def save_books(self):
        with open("books.json", "w", encoding="utf-8") as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)

    def load_books(self):
        if os.path.exists("books.json"):
            with open("books.json", "r", encoding="utf-8") as f:
                self.books = json.load(f)

if __name__ == "__main__":
    root = tk.Tk()
    app = BookTrackerApp(root)
    root.mainloop()
