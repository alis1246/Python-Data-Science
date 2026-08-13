import tkinter as tk
from csv_gui import CsvAnalyzerGUI

def main():
    root = tk.Tk()
    app = CsvAnalyzerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
