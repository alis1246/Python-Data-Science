import os
import tkinter as tk
from csv_processor import analyze_csv
from tkinter import filedialog, messagebox, ttk

class CsvAnalyzerGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("CSV Analyzer")
        self.root.geometry("700x480")
        self.root.minsize(600, 380)

        self._configure_styles()

        self._build_ui()

    def _configure_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure(
            "Treeview.Heading",
            font = ("Helvetica", 10, "bold"),
            background = "#e1e1e1",
            foreground = "#333333",
            padding = 6,
        )
        self.style.configure(
            "Treeview",
            font = ("Helvetica", 9),
            rowheight = 26,
            fieldbackground = "#ffffff",
        )
        self.style.map("Treeview", background=[("selected", "#0078d7")])

    def _build_ui(self):
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)


        top_frame = ttk.Frame(self.root, padding=(15, 12))
        top_frame.grid(row=0, column=0, sticky="ew")
        top_frame.columnconfigure(0, weight=1)

        self.btn_upload = ttk.Button(
            top_frame, text="Upload CSV file", command = self.upload_csv
        )
        self.btn_upload.grid(row=0, column=0, sticky="w", pady=(0, 8))

        self.lbl_file = ttk.Label(
            top_frame, text="Selected file: None", font=("Helvetica", 9, "bold")
        )
        self.lbl_file.grid(row=1, column=0, columnspan=2, sticky="w", pady=2)

        self.lbl_columns = ttk.Label(
            top_frame, text="Numerical Columns: None", foreground="#555555"
        )
        self.lbl_columns.grid(row=2, column=0, columnspan=2, sticky="w", pady=2)

        # ttk.Separator(self.root, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=15, pady=5)

        table_frame = ttk.Frame(self.root, padding=(15, 0, 15, 15))
        table_frame.grid(row=1, column=0, sticky="nsew")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)
        # table_frame.pack(fill=tk.BOTH ,expand=True)

        columns = ("Column", "Average", "Minimum", "Maximum", "Sum")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            width = 160 if col == "Column" else 110
            self.tree.column(col, width=width, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=1, column=1, sticky="ns")

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

    def display_results(self, results: dict):
        self._clear_table()

        for col_name, stats in results.items():
            self.tree.insert("", tk.END, values=(
                col_name,
                f"{stats['Average']:,.2f}",
                self._format_numbers(stats["Minimum"]),
                self._format_numbers(stats["Maximum"]),
                self._format_numbers(stats['Sum'])
            ))

    def _format_numbers(self, val: float) -> str:
        if val.is_integer():
            return f"{int(val):,}"
        return f"{val:,.2f}"

    def _clear_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)