import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys

# Ensure parent directory is in sys.path for import
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from passWordPhrase import LoadDictionaryFile

class PasswordApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Phrase Generator")
        self.geometry("400x450")
        self.resizable(True, True)

        self.generator = LoadDictionaryFile()
        try:
            self.generator.LoadFile()
        except Exception as e:
            messagebox.showerror("Error", f"Could not load dictionary: {e}")
            self.destroy()
            return

        # Widgets
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Number of Words:").pack(pady=5)
        self.count_var = tk.IntVar(value=4)
        ttk.Entry(self, textvariable=self.count_var, width=10).pack()

        self.insertNumbers_var = tk.BooleanVar()
        self.insertSpecial_var = tk.BooleanVar()
        self.insertChars_var = tk.BooleanVar()
        self.insertUpper_var = tk.BooleanVar()
        self.repeat_var = tk.IntVar(value=1)

        ttk.Checkbutton(self, text="Include Numbers as Separators", variable=self.insertNumbers_var).pack(anchor="w")
        ttk.Checkbutton(self, text="Include Special Characters as Separators", variable=self.insertSpecial_var).pack(anchor="w")
        ttk.Checkbutton(self, text="Include Letters as Separators", variable=self.insertChars_var).pack(anchor="w")
        ttk.Checkbutton(self, text="Include Uppercase Letters as Separators", variable=self.insertUpper_var).pack(anchor="w")

        ttk.Label(self, text="Number of Passwords:").pack(pady=5)
        ttk.Entry(self, textvariable=self.repeat_var, width=10).pack()

        ttk.Button(self, text="Generate", command=self.generate_passwords).pack(pady=10)

        self.result_box = tk.Text(self, height=8, width=45)
        self.result_box.pack(pady=5)

        ttk.Button(self, text="Save to File", command=self.save_to_file).pack(pady=5)

    def generate_passwords(self):
        self.result_box.delete("1.0", tk.END)
        try:
            for _ in range(self.repeat_var.get()):
                result = self.generator.PassWord(
                    count=self.count_var.get(),
                    insertNumbers=self.insertNumbers_var.get(),
                    insertSpecial=self.insertSpecial_var.get(),
                    insertChars=self.insertChars_var.get(),
                    insertUpper=self.insertUpper_var.get()
                )
                self.result_box.insert(tk.END, result + "\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate password: {e}")

    def save_to_file(self):
        passwords = self.result_box.get("1.0", tk.END).strip()
        if not passwords:
            messagebox.showwarning("Warning", "No passwords to save. Please generate passwords first.")
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(passwords)
                messagebox.showinfo("Success", f"Passwords saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

if __name__ == "__main__":
    PasswordApp().mainloop()