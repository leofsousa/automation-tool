from pathlib import Path


def get_files_from_folder(folder: Path) -> list[Path]:
    if not folder.exists():
        raise FileNotFoundError(f"Pasta nao encontrada: {folder}")

    if not folder.is_dir():
        raise NotADirectoryError(f"O caminho informado nao e uma pasta: {folder}")

    return sorted(
        [path for path in folder.iterdir() if path.is_file()],
        key=lambda path: path.name.lower(),
    )


def safe_target_path(source_path: Path, new_name: str) -> Path:
    target_path = source_path.with_name(new_name)

    if target_path.exists():
        raise FileExistsError(f"Destino ja existe: {target_path.name}")

    return target_path
