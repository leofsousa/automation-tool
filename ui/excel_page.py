import tkinter as tk
from tkinter import ttk


class ExcelPage(ttk.Frame):
    """Placeholder page for the future intelligent Excel formatter."""

    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent, padding=16)
        self._build_layout()

    def _build_layout(self) -> None:
        title = ttk.Label(
            self,
            text="Formatador Inteligente de Excel",
            font=("Segoe UI", 14, "bold"),
        )
        title.pack(anchor="w", pady=(0, 8))

        description = ttk.Label(
            self,
            text=(
                "Modulo reservado para a proxima etapa: leitura de planilhas, "
                "padronizacao de dados, preview e integracao futura com IA."
            ),
            wraplength=760,
        )
        description.pack(anchor="w")
