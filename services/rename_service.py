from dataclasses import dataclass
from pathlib import Path
import re

from utils.file_helpers import get_files_from_folder, safe_target_path
from utils.text_helpers import normalize_spaces


@dataclass(frozen=True)
class RenamePreviewItem:
    source_path: Path
    original_name: str
    new_name: str
    can_rename: bool
    status_label: str


@dataclass(frozen=True)
class RenameResult:
    success_count: int
    failure_count: int
    messages: list[str]


class RenameService:
    """Contains the batch renaming business rules."""

    def build_preview(self, folder: Path) -> list[RenamePreviewItem]:
        files = get_files_from_folder(folder)
        planned_names: set[str] = set()
        preview_items: list[RenamePreviewItem] = []

        for file_path in files:
            new_name = self.apply_rules(file_path.name)
            target_path = file_path.with_name(new_name)

            can_rename = True
            status = "Pronto"

            if new_name == file_path.name:
                can_rename = False
                status = "Sem alteracao"
            elif new_name in planned_names:
                can_rename = False
                status = "Nome duplicado no preview"
            elif target_path.exists():
                can_rename = False
                status = "Arquivo ja existe"

            planned_names.add(new_name)
            preview_items.append(
                RenamePreviewItem(
                    source_path=file_path,
                    original_name=file_path.name,
                    new_name=new_name,
                    can_rename=can_rename,
                    status_label=status,
                )
            )

        return preview_items

    def apply_rules(self, file_name: str) -> str:
        path = Path(file_name)
        stem = path.stem
        extension = path.suffix

        name_without_brackets = self._remove_bracket_content(stem)
        normalized_name = normalize_spaces(name_without_brackets)
        words = normalized_name.split()

        if not words:
            return file_name

        prefix = self._normalize_prefix(words[0])
        main_code = self._find_first_main_code(words[1:])

        if main_code is None:
            return f"{prefix}{extension}"

        return f"{prefix} {main_code}{extension}"

    def rename_files(self, preview_items: list[RenamePreviewItem]) -> RenameResult:
        success_count = 0
        failure_count = 0
        messages: list[str] = []

        for item in preview_items:
            if not item.can_rename:
                continue

            try:
                target_path = safe_target_path(item.source_path, item.new_name)
                item.source_path.rename(target_path)
                success_count += 1
                messages.append(f"OK: {item.original_name} -> {item.new_name}")
            except Exception as exc:
                failure_count += 1
                messages.append(f"ERRO: {item.original_name} -> {exc}")

        return RenameResult(
            success_count=success_count,
            failure_count=failure_count,
            messages=messages,
        )

    def _remove_bracket_content(self, value: str) -> str:
        result = []
        inside_brackets = False

        for char in value:
            if char == "[":
                inside_brackets = True
                continue
            if char == "]":
                inside_brackets = False
                continue
            if not inside_brackets:
                result.append(char)

        return "".join(result)

    def _normalize_prefix(self, value: str) -> str:
        if value.upper() == "BATERIA":
            return "BAT"
        return value.upper()

    def _find_first_main_code(self, values: list[str]) -> str | None:
        for value in values:
            match = re.search(r"\d+[A-Za-z]*", value)
            if match:
                return match.group(0).upper()
        return None
