"""Offline regression checks for portable generation and build-code fingerprints."""
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest


class GeneratorTests(unittest.TestCase):
    def test_output_paths_dates_and_code_versions(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            build = root / 'build'
            build.mkdir()
            shutil.copyfile(Path(__file__).with_name('gen.py'), build / 'gen.py')
            data = {'scraped_at': '2026-09-29', 'icons': {}, 'classes': [
                {'key': 'veteran', 'name': 'Veteran', 'nodes': [
                    {'s': 'root-veteran', 'cat': 'root', 'd': 'Root'},
                    {'s': 'talent', 'cat': 'passive', 'd': 'Original text'},
                ]},
                {'key': 'veteran-sub', 'name': 'Sub-tree', 'parent': 'veteran',
                 'nodes': [{'s': 'sub-root', 'cat': 'root'}]},
            ]}

            def generate():
                (build / 'data.json').write_text(json.dumps(data), encoding='utf-8')
                subprocess.run([sys.executable, str(build / 'gen.py')], cwd=root,
                               check=True, capture_output=True)
                page = (root / 'darktide-skill-trees.html').read_text(encoding='utf-8')
                embedded = json.loads(re.search(r'const DATA = (.*?);\n', page).group(1))
                self.assertIn('2026-09-29', page)
                self.assertNotIn('__DATA__', page)
                self.assertNotIn('__SCRAPED__', page)
                return embedded['classes'][0]['codeVersion']

            version = generate()
            self.assertTrue((root / 'index.html').is_file())
            self.assertTrue((root / 'veteran.html').is_file())
            self.assertFalse((root / 'veteran-sub.html').exists())
            page = (root / 'veteran.html').read_text(encoding='utf-8')
            embedded = json.loads(re.search(r'const DATA = (.*?);\n', page).group(1))
            self.assertEqual(len(embedded['classes']), 2)

            data['classes'][0]['nodes'][1]['d'] = 'Updated wording'
            self.assertEqual(generate(), version)
            data['classes'][0]['nodes'].reverse()
            self.assertNotEqual(generate(), version)


if __name__ == '__main__':
    unittest.main()
