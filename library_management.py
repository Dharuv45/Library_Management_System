import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import library_db

class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("800x600")
        self.root.configure(bg='sky blue')  # Set background color

        # Initialize database
        library_db.create_table()
        # h

        # GUI Elements
        self.title_label = tk.Label(root, text="Library Management System", font=('Helvetica', 18), bg='sky blue')
        self.title_label.pack(pady=10)

        self.book_table = ttk.Treeview(root, columns=("ID", "Title", "Author", "Year", "Status"), show='headings')
        self.book_table.heading("ID", text="ID")
        self.book_table.heading("Title", text="Title")
        self.book_table.heading("Author", text="Author")
        self.book_table.heading("Year", text="Year")
        self.book_table.heading("Status", text="Status")
        self.book_table.pack(pady=20)

        self.refresh_button = tk.Button(root, text="Refresh", command=self.refresh_books, bg='white')
        self.refresh_button.pack(pady=10)

        self.issue_button = tk.Button(root, text="Issue Book", command=self.issue_book, bg='white')
        self.issue_button.pack(pady=10)

        self.return_button = tk.Button(root, text="Return Book", command=self.return_book, bg='white')
        self.return_button.pack(pady=10)

        self.add_book_button = tk.Button(root, text="Add Book", command=self.open_add_book_window, bg='white')
        self.add_book_button.pack(pady=10)

        self.edit_button = tk.Button(root, text="Edit Book", command=self.open_edit_book_window, bg='white')
        self.edit_button.pack(pady=10)

        self.remove_button = tk.Button(root, text="Remove Book", command=self.remove_book, bg='white')
        self.remove_button.pack(pady=10)

        # Load initial data
        self.refresh_books()

    def refresh_books(self):
        for row in self.book_table.get_children():
            self.book_table.delete(row)
        books = library_db.get_all_books()
        for book in books:
            self.book_table.insert("", tk.END, values=book)

    def issue_book(self):
        selected_item = self.book_table.selection()
        if selected_item:
            book_id = self.book_table.item(selected_item)['values'][0]
            library_db.issue_book(book_id)
            self.refresh_books()
            messagebox.showinfo("Success", "Book Issued Successfully!")
        else:
            messagebox.showwarning("Select Book", "Please select a book to issue")

    def return_book(self):
        selected_item = self.book_table.selection()
        if selected_item:
            book_id = self.book_table.item(selected_item)['values'][0]
            library_db.return_book(book_id)
            self.refresh_books()
            messagebox.showinfo("Success", "Book Returned Successfully!")
        else:
            messagebox.showwarning("Select Book", "Please select a book to return")

    def open_add_book_window(self):
        add_book_window = tk.Toplevel(self.root)
        add_book_window.title("Add Book")
        add_book_window.geometry("400x300")
        add_book_window.configure(bg='sky blue')  # Set background color

        tk.Label(add_book_window, text="Title:", bg='sky blue').pack(pady=5)
        title_entry = tk.Entry(add_book_window, width=30)
        title_entry.pack(pady=5)

        tk.Label(add_book_window, text="Author:", bg='sky blue').pack(pady=5)
        author_entry = tk.Entry(add_book_window, width=30)
        author_entry.pack(pady=5)

        tk.Label(add_book_window, text="Year:", bg='sky blue').pack(pady=5)
        year_entry = tk.Entry(add_book_window, width=30)
        year_entry.pack(pady=5)

        def add_book_to_db():
            title = title_entry.get()
            author = author_entry.get()
            year = year_entry.get()

            if title and author and year:
                try:
                    year = int(year)
                    library_db.add_book(title, author, year)
                    messagebox.showinfo("Success", "Book Added Successfully!")
                    self.refresh_books()
                    add_book_window.destroy()
                except ValueError:
                    messagebox.showerror("Invalid Input", "Year must be a number")
            else:
                messagebox.showerror("Missing Information", "Please fill out all fields")

        tk.Button(add_book_window, text="Add Book", command=add_book_to_db, bg='white').pack(pady=20)

    def open_edit_book_window(self):
        selected_item = self.book_table.selection()
        if selected_item:
            book_id = self.book_table.item(selected_item)['values'][0]
            current_title = self.book_table.item(selected_item)['values'][1]
            current_author = self.book_table.item(selected_item)['values'][2]
            current_year = self.book_table.item(selected_item)['values'][3]

            edit_book_window = tk.Toplevel(self.root)
            edit_book_window.title("Edit Book")
            edit_book_window.geometry("400x300")
            edit_book_window.configure(bg='sky blue')  # Set background color

            tk.Label(edit_book_window, text="Title:", bg='sky blue').pack(pady=5)
            title_entry = tk.Entry(edit_book_window, width=30)
            title_entry.insert(0, current_title)
            title_entry.pack(pady=5)

            tk.Label(edit_book_window, text="Author:", bg='sky blue').pack(pady=5)
            author_entry = tk.Entry(edit_book_window, width=30)
            author_entry.insert(0, current_author)
            author_entry.pack(pady=5)

            tk.Label(edit_book_window, text="Year:", bg='sky blue').pack(pady=5)
            year_entry = tk.Entry(edit_book_window, width=30)
            year_entry.insert(0, current_year)
            year_entry.pack(pady=5)

            def update_book_in_db():
                title = title_entry.get()
                author = author_entry.get()
                year = year_entry.get()

                if title and author and year:
                    try:
                        year = int(year)
                        library_db.update_book(book_id, title, author, year)
                        messagebox.showinfo("Success", "Book Updated Successfully!")
                        self.refresh_books()
                        edit_book_window.destroy()
                    except ValueError:
                        messagebox.showerror("Invalid Input", "Year must be a number")
                else:
                    messagebox.showerror("Missing Information", "Please fill out all fields")

            tk.Button(edit_book_window, text="Update Book", command=update_book_in_db, bg='white').pack(pady=20)
        else:
            messagebox.showwarning("Select Book", "Please select a book to edit")

    def remove_book(self):
        selected_item = self.book_table.selection()
        if selected_item:
            book_id = self.book_table.item(selected_item)['values'][0]
            response = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this book?")
            if response:
                library_db.delete_book(book_id)
                self.refresh_books()
                messagebox.showinfo("Success", "Book Deleted Successfully!")
        else:
            messagebox.showwarning("Select Book", "Please select a book to remove")


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementSystem(root)
    root.mainloop()
