import os
import tkinter as tk
from csv_processor import analyze_csv
from tkinter import filedialog, messagebox, ttk

class CsvAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Analyzer")
        self.root.geometry("650x450")
        self.root.minsize(550, 350)

        self._build_ui()

    def _build_ui(self):
        top_frame = ttk.Frame(self.root, padding="15")
        top_frame.pack(fill=tk.X)

        self.btn_upload = ttk.Button(
            top_frame, text="Upload CSV file", command = self.upload_csv
        )
        self.btn_upload.pack(anchor = tk.W, pady=(0, 10))

        self.lbl_file = ttk.Label(
            top_frame, text="Selected file: None", font=("Helvetica", 9, "bold")
        )
        self.lbl_file.pack(anchor = tk.W, pady=2)

        self.lbl_columns = ttk.Label(
            top_frame, text="Numerical Columns: None", foreground="gray"
        )
        self.lbl_columns.pack(anchor = tk.W, pady=2)

        ttk.Separator(self.root, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=15, pady=5)

        table_frame = ttk.Frame(self.root, padding=15)
        table_frame.pack(fill=tk.BOTH ,expand=True)

        columns = ("Column", "Average", "Minimum", "Maximum", "Sum")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            width = 150 if col == "Column" else 100
            self.tree.column(col, width=width, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def upload_csv(self):
        file_path = filedialog.askopenfilename(
            title = "Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All Files", "*.*")],
        )

        if not file_path:
            return

        try:
            results, numeric_columns = analyze_csv(file_path)

            filename = os.path.basename(file_path)

            if results is None or not numeric_columns:
                self.lbl_file.config(text=f"Selected file: {filename}")
                self.lbl_columns.config(text="Numerical Columns: None")
                self._clear_table()
                messagebox.showinfo(
                    "No numerical Columns",
                    "No numerical columns were found in the selected csv file. Please select a different file"
                )
                return
            self.lbl_file.config(text=f"Selected file: {filename}")
            self.lbl_columns.config(
                text=f"Numerical Columns: {','.join(numeric_columns)}"
            )

            self.display_results(results)

        except Exception as error:
            messagebox.showerror("Error Reading File", str(error))

    def display_results(self, results):
        self._clear_table()

        for col_name, stats in results.items():
            self.tree.insert("", tk.END, values=(
                col_name,
                f"{stats['Average']:.2f}",
                f"{stats['Minimum']:.2f}",
                f"{stats['Maximum']:.2f}",
                f"{stats['Sum']:.2f}"
            ))

    def _clear_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)