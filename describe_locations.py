import shutil
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


def copy_to_txt(base: Path, out_dir: Path) -> list:
    """Copy each found config file into out_dir as a uniquely named .txt file."""
    candidates = collect_candidates(base)
    found = [p for p in candidates if p.exists()]
    out_dir.mkdir(parents=True, exist_ok=True)
    for p in found:
        txt_name = str(p).lstrip("/").replace("/", "_") + ".txt"
        shutil.copy2(p, out_dir / txt_name)
    return found


if __name__ == "__main__":
    base = Path.cwd()
    print(describe_locations(base))

    out_dir = base / "artifacts"
    found = copy_to_txt(base, out_dir)
    if found:
        print(f"\nCopied files as .txt into {out_dir}:")
        for p in found:
            txt_name = str(p).lstrip("/").replace("/", "_") + ".txt"
            print(f"  - {out_dir / txt_name}")
    else:
        print(f"\nNo config files found; {out_dir} created (empty).")
