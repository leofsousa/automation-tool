from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from services.rename_service import RenameService


class RenamePage(ttk.Frame):
    """Page responsible for the batch file renaming workflow."""

    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent, padding=12)

        self.rename_service = RenameService()
        self.selected_folder: Path | None = None
        self.preview_items = []

        self._build_layout()

    def _build_layout(self) -> None:
        toolbar = ttk.Frame(self)
        toolbar.pack(fill="x", pady=(0, 10))

        select_button = ttk.Button(
            toolbar,
            text="Selecionar pasta",
            command=self._select_folder,
        )
        select_button.pack(side="left")

        self.folder_label = ttk.Label(toolbar, text="Nenhuma pasta selecionada")
        self.folder_label.pack(side="left", padx=12)

        self.rename_button = ttk.Button(
            toolbar,
            text="Renomear",
            command=self._rename_files,
            state="disabled",
        )
        self.rename_button.pack(side="right")

        columns = ("original", "preview", "status")
        self.file_tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            selectmode="browse",
        )
        self.file_tree.heading("original", text="Arquivo original")
        self.file_tree.heading("preview", text="Novo nome")
        self.file_tree.heading("status", text="Status")
        self.file_tree.column("original", width=390, anchor="w")
        self.file_tree.column("preview", width=270, anchor="w")
        self.file_tree.column("status", width=160, anchor="w")
        self.file_tree.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            self.file_tree,
            orient="vertical",
            command=self.file_tree.yview,
        )
        self.file_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        log_frame = ttk.LabelFrame(self, text="Logs e status", padding=8)
        log_frame.pack(fill="x", pady=(10, 0))

        self.log_text = tk.Text(log_frame, height=6, wrap="word", state="disabled")
        self.log_text.pack(fill="x", expand=False)

    def _select_folder(self) -> None:
        folder_name = filedialog.askdirectory(title="Selecione a pasta com arquivos")
        if not folder_name:
            return

        self.selected_folder = Path(folder_name)
        self.folder_label.configure(text=str(self.selected_folder))
        self._load_preview()

    def _load_preview(self) -> None:
        self._clear_tree()
        self.preview_items = []

        if self.selected_folder is None:
            self._set_status("Selecione uma pasta para carregar os arquivos.")
            return

        try:
            self.preview_items = self.rename_service.build_preview(self.selected_folder)
        except Exception as exc:
            self.rename_button.configure(state="disabled")
            self._set_status(f"Erro ao carregar arquivos: {exc}")
            messagebox.showerror("Erro", f"Nao foi possivel carregar a pasta.\n\n{exc}")
            return

        if not self.preview_items:
            self.rename_button.configure(state="disabled")
            self._set_status("Nenhum arquivo encontrado na pasta selecionada.")
            return

        for item in self.preview_items:
            self.file_tree.insert(
                "",
                "end",
                values=(
                    item.original_name,
                    item.new_name,
                    item.status_label,
                ),
            )

        renameable_count = sum(1 for item in self.preview_items if item.can_rename)
        self.rename_button.configure(
            state="normal" if renameable_count > 0 else "disabled"
        )
        self._set_status(
            f"{len(self.preview_items)} arquivo(s) encontrados. "
            f"{renameable_count} arquivo(s) pronto(s) para renomear."
        )

    def _rename_files(self) -> None:
        if self.selected_folder is None:
            messagebox.showwarning("Atencao", "Selecione uma pasta antes de renomear.")
            return

        renameable_count = sum(1 for item in self.preview_items if item.can_rename)
        if renameable_count == 0:
            messagebox.showinfo("Renomeador", "Nao ha arquivos prontos para renomear.")
            return

        confirmed = messagebox.askyesno(
            "Confirmar renomeacao",
            f"Renomear {renameable_count} arquivo(s)?",
        )
        if not confirmed:
            self._set_status("Operacao cancelada pelo usuario.")
            return

        result = self.rename_service.rename_files(self.preview_items)

        self._set_status(
            f"Renomeacao finalizada. Sucesso: {result.success_count}. "
            f"Falhas: {result.failure_count}."
        )

        for message in result.messages:
            self._append_log(message)

        self._load_preview()

    def _clear_tree(self) -> None:
        for item_id in self.file_tree.get_children():
            self.file_tree.delete(item_id)

    def _set_status(self, message: str) -> None:
        self._append_log(message, clear=True)

    def _append_log(self, message: str, clear: bool = False) -> None:
        self.log_text.configure(state="normal")
        if clear:
            self.log_text.delete("1.0", "end")
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")
