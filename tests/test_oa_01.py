import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parent.parent / 'oa-01.py'
SPEC = importlib.util.spec_from_file_location('oa_01', MODULE_PATH)
oa_01 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(oa_01)


class Oa01Tests(unittest.TestCase):
    def test_candidate_paths_include_workspace_and_user_locations(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp) / 'repo'
            (repo_root / '.git').mkdir(parents=True)
            start_dir = repo_root / 'nested'
            start_dir.mkdir(parents=True)

            candidates = oa_01.candidate_mcp_paths(start_dir)

            self.assertIn(start_dir / '.github/mcp.json', candidates)
            self.assertIn(repo_root / '.github/mcp.json', candidates)
            self.assertIn(start_dir / '.mcp.json', candidates)
            self.assertIn(start_dir / '.vscode/mcp.json', candidates)
            self.assertIn(oa_01.USER_MCP_PATH, candidates)
            self.assertNotIn(Path(tmp) / '.github/mcp.json', candidates)

    def test_describe_locations_downloads_found_configs(self):
        with tempfile.TemporaryDirectory() as tmp:
            start_dir = Path(tmp)
            source_dir = start_dir / '.github'
            source_dir.mkdir(parents=True)
            source_file = source_dir / 'mcp.json'
            source_file.write_text('{"mcpServers": {}}', encoding='utf-8')

            description = oa_01.describe_locations(start_dir)
            downloaded_file = start_dir / oa_01.DOWNLOAD_DIR / 'mcp-1-github-mcp.json'

            self.assertIn(str(source_file), description)
            self.assertTrue(downloaded_file.is_file())
            self.assertEqual(source_file.read_text(encoding='utf-8'), downloaded_file.read_text(encoding='utf-8'))

    def test_downloads_do_not_overwrite_existing_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root_dir = Path(tmp)
            source_dir = root_dir / 'source'
            destination_dir = root_dir / 'downloads'
            source_dir.mkdir()
            destination_dir.mkdir()
            source_file = source_dir / 'mcp.json'
            source_file.write_text('{"first": true}', encoding='utf-8')

            first_download = oa_01.download_mcp_files([source_file], destination_dir)[0]
            second_download = oa_01.download_mcp_files([source_file], destination_dir)[0]

            self.assertNotEqual(first_download, second_download)
            self.assertTrue(first_download.name.startswith('mcp-1-source-mcp'))
            self.assertTrue(second_download.name.startswith('mcp-1-source-mcp-2'))


if __name__ == '__main__':
    unittest.main()
