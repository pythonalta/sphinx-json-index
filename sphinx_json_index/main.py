import json
import yaml
import os
from sphinx.builders import Builder
from sphinx.config import Config

def read_frontmatter(srcdir, docname):
    for ext in ('.md', '.markdown'):
        fn = os.path.join(srcdir, docname + ext)
        if os.path.isfile(fn):
            with open(fn, encoding='utf-8') as f:
                lines = f.read().splitlines()
            if lines and lines[0].strip() == "---":
                end = None
                for i, line in enumerate(lines[1:], 1):
                    if line.strip() == "---":
                        end = i
                        break
                if end is not None:
                    yml = "\n".join(lines[1:end])
                    try:
                        return yaml.safe_load(yml) or {}
                    except Exception:
                        return {}
    return {}

class JsonIndexBuilder(Builder):
    name = 'jsonindex'
    format = 'json'

    def init(self):
        self.output = []
        self.config.add('jsonindex_filename', 'searchindex.json', 'html', [str])
        self.config.add('jsonindex_add_html_suffix', True, 'html', [bool])


    def get_outdated_docs(self):
        return 'all documents'

    def write(self, *ignored):
        srcdir = self.env.srcdir
        add_html_suffix = self.config.jsonindex_add_html_suffix

        for docname in self.env.found_docs:
            meta = read_frontmatter(srcdir, docname)
            title = meta.get('title')
            tags = meta.get('tags', [])
            category = meta.get('category', '')

            if isinstance(title, dict):
                title = title.get('name') or str(title)
            elif title is None:
                title = ""

            if isinstance(tags, str):
                tags = [tag.strip() for tag in tags.replace(';', ',').split(',') if tag.strip()]
            elif tags is None:
                tags = []

            if not category:
                category = meta.get('categories', '')
            if isinstance(category, list):
                category = ', '.join(map(str, category))
            elif not isinstance(category, str):
                category = str(category)

            if not title:
                if docname in self.env.titles:
                    title = self.env.titles[docname].astext().strip()
            if not title:
                title = "<no title>"

            doctree = self.env.get_doctree(docname)
            text = doctree.astext()

            href = docname
            if add_html_suffix:
                href += (self.config.html_file_suffix or '.html')

            self.output.append({
                'id': docname,
                'title': title,
                'content': text,
                'href': href,
                'tags': tags,
                'category': category,
            })

        out_static_dir = os.path.join(self.outdir, '_static')
        os.makedirs(out_static_dir, exist_ok=True)

        outfname = os.path.join(out_static_dir, self.config.jsonindex_filename)
        with open(outfname, 'w', encoding='utf-8') as f:
            json.dump({'docs': self.output}, f, ensure_ascii=False, indent=2)

def setup(app):
    app.add_builder(JsonIndexBuilder)
