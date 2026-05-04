import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json


class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")

        # Список книг
        self.books = []

        # Создание интерфейса
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        # Поля для ввода
        frame_input = tk.Frame(self.root)
        frame_input.pack(padx=10, pady=10)

        tk.Label(frame_input, text="Название книги").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_title = tk.Entry(frame_input, width=40)
        self.entry_title.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Автор").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_author = tk.Entry(frame_input, width=40)
        self.entry_author.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Жанр").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_genre = tk.Entry(frame_input, width=40)
        self.entry_genre.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame_input, text="Количество страниц").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_pages = tk.Entry(frame_input, width=40)
        self.entry_pages.grid(row=3, column=1, padx=5, pady=5)

        # Кнопка добавления
        btn_add = tk.Button(self.root, text="Добавить книгу", command=self.add_book)
        btn_add.pack(pady=5)

        # Фильтр
        frame_filter = tk.Frame(self.root)
        frame_filter.pack(padx=10, pady=10)

        tk.Label(frame_filter, text="Фильтр по жанру").grid(row=0, column=0, padx=5, sticky="w")
        self.entry_filter_genre = tk.Entry(frame_filter, width=20)
        self.entry_filter_genre.grid(row=0, column=1, padx=5)

        tk.Label(frame_filter, text="Мин. страниц").grid(row=0, column=2, padx=5, sticky="w")
        self.entry_filter_pages = tk.Entry(frame_filter, width=10)
        self.entry_filter_pages.grid(row=0, column=3, padx=5)

        btn_filter = tk.Button(frame_filter, text="Применить фильтр", command=self.apply_filter)
        btn_filter.grid(row=0, column=4, padx=5)

        btn_clear_filter = tk.Button(frame_filter, text="Сбросить фильтр", command=self.clear_filter)
        btn_clear_filter.grid(row=0, column=5, padx=5)  # <-- исправлено: пропущена запятая в исходнике

        # Таблица для отображения книг
        columns = ("title", "author", "genre", "pages")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        self.tree.heading("title", text="Название книги")
        self.tree.heading("author", text="Автор")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("pages", text="Страницы")

        self.tree.column("title", width=220, anchor="w")
        self.tree.column("author", width=160, anchor="w")
        self.tree.column("genre", width=120, anchor="w")
        self.tree.column("pages", width=80, anchor="center")

        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        # Меню для сохранения/загрузки
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Сохранить в JSON", command=self.save_to_json)
        file_menu.add_command(label="Загрузить из JSON", command=self.load_from_json)
        menubar.add_cascade(label="Файл", menu=file_menu)
        self.root.config(menu=menubar)

    def add_book(self):
        title = self.entry_title.get().strip()
        author = self.entry_author.get().strip()
        genre = self.entry_genre.get().strip()
        pages = self.entry_pages.get().strip()

        # Проверка корректности
        if not title or not author or not genre or not pages:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
            return

        if not pages.isdigit():
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом")
            return

        book = {"title": title, "author": author, "genre": genre, "pages": int(pages)}
        self.books.append(book)
        self.update_treeview()
        self.clear_entries()

    def clear_entries(self):
        self.entry_title.delete(0, tk.END)
        self.entry_author.delete(0, tk.END)
        self.entry_genre.delete(0, tk.END)
        self.entry_pages.delete(0, tk.END)

    def update_treeview(self, data=None):
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)

        data_to_show = data if data is not None else self.books
        for book in data_to_show:
            self.tree.insert(
                "",
                tk.END,
                values=(book.get("title", ""), book.get("author", ""), book.get("genre", ""), book.get("pages", "")),
            )

    def save_to_json(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
        )
        if not filename:
            return

        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.books, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Успех", "Данные успешно сохранены")
        except OSError as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{e}")

    def load_from_json(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not filename:
            return

        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not isinstance(data, list):
                raise ValueError("Ожидался список книг (list) в JSON")

            # Небольшая нормализация/проверка структуры
            normalized = []
            for item in data:
                if not isinstance(item, dict):
                    continue
                title = str(item.get("title", "")).strip()
                author = str(item.get("author", "")).strip()
                genre = str(item.get("genre", "")).strip()
                pages = item.get("pages", "")

                try:
                    pages_int = int(pages)
                except (TypeError, ValueError):
                    pages_int = 0

                if title and author and genre:
                    normalized.append({"title": title, "author": author, "genre": genre, "pages": pages_int})

            self.books = normalized
            self.update_treeview()
        except (OSError, json.JSONDecodeError, ValueError) as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить JSON:\n{e}")

    def load_data(self):
        # Инициализация/очистка данных при старте
        self.books = []
        self.update_treeview()

    def apply_filter(self):
        genre_filter = self.entry_filter_genre.get().strip().lower()
        pages_filter = self.entry_filter_pages.get().strip()

        filtered = self.books

        if genre_filter:
            filtered = [b for b in filtered if genre_filter in str(b.get("genre", "")).lower()]

        if pages_filter:
            if pages_filter.isdigit():
                min_pages = int(pages_filter)
                filtered = [b for b in filtered if int(b.get("pages", 0)) >= min_pages]
            else:
                messagebox.showerror("Ошибка", "Мин. страниц должно быть числом")
                return

        self.update_treeview(filtered)

    def clear_filter(self):
        self.entry_filter_genre.delete(0, tk.END)
        self.entry_filter_pages.delete(0, tk.END)
        self.update_treeview()


if __name__ == "__main__":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()