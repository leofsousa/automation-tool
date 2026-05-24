from pathlib import Path


class ExcelService:
    """Initial service boundary for future Excel processing features."""

    def build_preview(self, workbook_path: Path) -> list[dict[str, str]]:
        raise NotImplementedError("Excel preview will be implemented in the next step.")
