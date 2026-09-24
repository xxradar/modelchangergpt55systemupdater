from __future__ import annotations

import shutil
from pathlib import Path

WORKSPACE_MCP_PATHS = (
    Path('.github/mcp.json'),
    Path('.mcp.json'),
    Path('.vscode/mcp.json'),
)
DOWNLOAD_DIR = Path('downloaded-mcp')


def user_mcp_path() -> Path:
    """Return the default user-level GitHub Copilot MCP config path candidate. The file may not exist."""
    return Path.home() / '.copilot' / 'mcp-config.json'


def search_directories(start_dir: Path) -> list[Path]:
    resolved_start = start_dir.resolve()
    git_root = next(
        (directory for directory in (resolved_start, *resolved_start.parents) if (directory / '.git').exists()),
        None,
    )

    if git_root is None:
        return [resolved_start]

    directories = [resolved_start]
    current_directory = resolved_start
    while current_directory != git_root:
        current_directory = current_directory.parent
        directories.append(current_directory)

    return directories


def candidate_mcp_paths(start_dir: Path) -> list[Path]:
    """Return likely Copilot MCP configuration files in lookup order."""
    candidates: dict[Path, None] = {}

    for directory in search_directories(start_dir):
        for relative_path in WORKSPACE_MCP_PATHS:
            candidates.setdefault(directory / relative_path, None)

    candidates.setdefault(user_mcp_path(), None)
    return list(candidates)


def existing_mcp_paths(start_dir: Path) -> list[Path]:
    return [path for path in candidate_mcp_paths(start_dir) if path.is_file()]


def build_download_name(source_path: Path) -> str:
    suffix = source_path.suffix if source_path.suffix else '.json'
    parent_name = source_path.parent.name.lstrip('.') or 'root'
    stem = source_path.stem.lstrip('.') or 'mcp'
    return f'{parent_name}-{stem}{suffix}'


def next_available_path(destination_dir: Path, file_name: str) -> Path:
    base_path = Path(file_name)
    candidate = destination_dir / file_name
    counter = 2

    while candidate.exists():
        candidate = destination_dir / f'{base_path.stem}-{counter}{base_path.suffix}'
        counter += 1

    return candidate


def download_mcp_files(paths: list[Path], destination_dir: Path) -> list[Path]:
    destination_dir.mkdir(parents=True, exist_ok=True)
    downloaded_paths: list[Path] = []

    for source_path in paths:
        target_path = next_available_path(destination_dir, build_download_name(source_path))
        shutil.copy2(source_path, target_path)
        downloaded_paths.append(target_path)

    return downloaded_paths


def describe_locations(start_dir: Path) -> str:
    lines = [
        'GitHub Copilot MCP configuration is commonly stored in:',
        *[f'- {path}' for path in candidate_mcp_paths(start_dir)],
    ]

    found_paths = existing_mcp_paths(start_dir)
    if not found_paths:
        lines.append('No mcp.json-style configuration files were found to download.')
        return '\n'.join(lines)

    lines.append('Found the following configuration files:')
    lines.extend(f'- {path}' for path in found_paths)

    downloaded_paths = download_mcp_files(found_paths, start_dir / DOWNLOAD_DIR)
    lines.append(f'Downloaded copies into {start_dir / DOWNLOAD_DIR}:')
    lines.extend(f'- {path}' for path in downloaded_paths)
    return '\n'.join(lines)


def main() -> None:
    print(describe_locations(Path.cwd()))


if __name__ == '__main__':
    main()
