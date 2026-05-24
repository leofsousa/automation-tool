import tkinter as tk
from tkinter import ttk
from pathlib import Path

from ui.excel_page import ExcelPage
from ui.rename_page import RenamePage


class App(tk.Tk):
    """Main application window."""

    def __init__(self) -> None:
        super().__init__()

        self.title("Automation Tool")
        self.geometry("980x640")
        self.minsize(880, 560)

        self._configure_window_icon()
        self._configure_style()
        self._build_layout()

    def _configure_window_icon(self) -> None:
        icon_path = Path(__file__).resolve().parents[1] / "assets" / "app_icon.ico"

        if not icon_path.exists():
            return

        try:
            self.iconbitmap(default=str(icon_path))
        except tk.TclError:
            pass

    def _configure_style(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook.Tab", padding=(16, 8))
        style.configure("Treeview", rowheight=26)
        style.configure("Status.TLabel", foreground="#374151")

    def _build_layout(self) -> None:
        container = ttk.Frame(self, padding=12)
        container.pack(fill="both", expand=True)

        title = ttk.Label(
            container,
            text="Ferramenta de Automacao Interna",
            font=("Segoe UI", 16, "bold"),
        )
        title.pack(anchor="w", pady=(0, 10))

        notebook = ttk.Notebook(container)
        notebook.pack(fill="both", expand=True)

        notebook.add(RenamePage(notebook), text="Renomeador")
        notebook.add(ExcelPage(notebook), text="Excel")
