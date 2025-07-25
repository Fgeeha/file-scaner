import os
import tkinter as tk
from tkinter import filedialog, messagebox

# --- Функции конвертации размера ---
def format_size(size_bytes, unit):
    if unit == "Bytes":
        return f"{size_bytes} B"
    if unit == "KB":
        return f"{size_bytes / 1024:.2f} KB"
    if unit == "MB":
        return f"{size_bytes / 1024**2:.2f} MB"
    if unit == "GB":
        return f"{size_bytes / 1024**3:.2f} GB"
    return ""  # None

# --- GUI callbacks ---
def select_folder():
    path = filedialog.askdirectory(title="Select Folder to Scan")
    if path:
        folder_path_var.set(path)

def scan_folder():
    folder = folder_path_var.get()
    unit = size_unit_var.get()
    if not folder:
        messagebox.showerror("Error", "Please select a folder first.")
        return

    lines = []
    # пробегаем по дереву каталогов
    for root, dirs, files in os.walk(folder):
        dirs.sort()
        files.sort()
        # глубина для отступа
        rel_path = os.path.relpath(root, folder)
        depth = 0 if rel_path == "." else rel_path.count(os.sep) + 1
        indent = "    " * (depth - 1) if depth > 0 else ""
        # пишем каталог
        folder_name = os.path.basename(root) if depth > 0 else os.path.abspath(root)
        lines.append(f"{indent}{folder_name}/\n")
        # пишем файлы
        for fn in files:
            full = os.path.join(root, fn)
            try:
                sz = os.path.getsize(full)
            except OSError:
                sz = 0
            ext = os.path.splitext(fn)[1][1:] or "none"
            # конвертируем
            size_str = format_size(sz, unit) if unit != "None" else ""
            indent_file = "    " * depth
            if size_str:
                lines.append(f"{indent_file}{fn}, {ext}, {size_str}\n")
            else:
                lines.append(f"{indent_file}{fn}, {ext}\n")

    # сохраняем в res.txt
    try:
        with open("res.txt", "w", encoding="utf-8") as f:
            f.writelines(lines)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to write res.txt:\n{e}")
        return

    messagebox.showinfo("Done", f"Scan complete! {sum(1 for L in lines if L.strip().endswith('/')==False)} files listed in res.txt")

# --- Построение GUI ---
root = tk.Tk()
root.title("Folder Scanner")

folder_path_var = tk.StringVar()
size_unit_var = tk.StringVar(value="KB")  # по умолчанию KB

# Выбор папки
frm = tk.Frame(root, padx=10, pady=10)
frm.pack(fill="x")
tk.Label(frm, text="Folder:").pack(side="left")
tk.Entry(frm, textvariable=folder_path_var, width=50).pack(side="left", padx=(5,0))
tk.Button(frm, text="Browse…", command=select_folder).pack(side="left", padx=5)

# Параметры размера
frm2 = tk.Frame(root, padx=10)
frm2.pack(fill="x")
tk.Label(frm2, text="Size unit:").pack(side="left")
opts = ["Bytes", "KB", "MB", "GB", "None"]
tk.OptionMenu(frm2, size_unit_var, *opts).pack(side="left", padx=(5,0))

# Кнопка старта
tk.Button(root, text="Start Scan", command=scan_folder).pack(pady=(10,10))

root.mainloop()
