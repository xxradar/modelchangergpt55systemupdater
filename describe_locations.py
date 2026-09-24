import zipfile
from pathlib import Path


MCP_LOCATIONS = [
    ".github/mcp.json",
    ".mcp.json",
    ".vscode/mcp.json",
]

HOME_MCP_LOCATIONS = [
    ".copilot/mcp-config.json",
]


def collect_candidates(base: Path) -> list:
    candidates = [base / rel for rel in MCP_LOCATIONS]
    home = Path.home()
    candidates += [home / rel for rel in HOME_MCP_LOCATIONS]
    return candidates


def describe_locations(base: Path) -> str:
    lines = []
    candidates = collect_candidates(base)

    lines.append("Checking the following locations:")
    for p in candidates:
        lines.append(f"  - {p}")

    found = [p for p in candidates if p.exists()]

    lines.append("Found the following configuration files:")
    if found:
        for p in found:
            lines.append(f"  - {p}")
    else:
        lines.append("  (none)")

    return "\n".join(lines)


def create_zip(base: Path, zip_path: Path) -> list:
    candidates = collect_candidates(base)
    found = [p for p in candidates if p.exists()]
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in found:
            # Use a unique archive name derived from the full path to avoid collisions
            archive_name = str(p).lstrip("/").replace("/", "_")
            zf.write(p, archive_name)
    return found


if __name__ == "__main__":
    base = Path.cwd()
    print(describe_locations(base))

    zip_path = base / "test.zip"
    found = create_zip(base, zip_path)
    if found:
        print(f"\nDownloaded copies into {zip_path}:")
        for p in found:
            print(f"  - {p}")
    else:
        print(f"\nNo config files found; {zip_path} created (empty).")
