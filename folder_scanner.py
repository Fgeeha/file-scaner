import os
import tkinter as tk
from tkinter import filedialog, messagebox

def select_folder():
    """Open a folder dialog and store the selected path."""
    path = filedialog.askdirectory(title="Select Folder to Scan")
    if path:
        folder_path_var.set(path)

def scan_folder():
    """Scan the selected folder and write results to res.txt."""
    folder = folder_path_var.get()
    if not folder:
        messagebox.showerror("Error", "Please select a folder first.")
        return

    entries = []
    # Walk through the directory tree in sorted order
    for root, dirs, files in os.walk(folder):
        dirs.sort()
        files.sort()
        for filename in files:
            fullpath = os.path.join(root, filename)
            try:
                size = os.path.getsize(fullpath)
            except OSError:
                size = 0
            # file type is the extension without the dot (or 'none' if no ext)
            ext = os.path.splitext(filename)[1][1:] or "none"
            entries.append((fullpath, filename, ext, size))

    # Write to res.txt in the current working directory
    with open("res.txt", "w", encoding="utf-8") as f:
        for fullpath, name, ftype, fsize in entries:
            f.write(f"{name}, {ftype}, {fsize}\n")

    messagebox.showinfo("Done", f"Scan complete!\n{len(entries)} files listed in res.txt")

# --- Build the GUI ---
root = tk.Tk()
root.title("Folder Scanner")

folder_path_var = tk.StringVar()

# Folder selection row
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="x")

tk.Label(frame, text="Folder:").pack(side="left")
entry = tk.Entry(frame, textvariable=folder_path_var, width=50)
entry.pack(side="left", padx=(5, 0))
tk.Button(frame, text="Browse…", command=select_folder).pack(side="left", padx=5)

# Scan button
scan_btn = tk.Button(root, text="Start Scan", command=scan_folder)
scan_btn.pack(pady=(0,10))

root.mainloop()
