from sphinx.builders import Builder
import json
import os

class JsonIndexBuilder(Builder):
    name = 'jsonindex'
    format = 'json'

    def init(self):
        self.output = []

    def get_outdated_docs(self):
        return 'all documents'

    def write(self, *ignored):
        for docname in self.env.found_docs:
            doctree = self.env.get_doctree(docname)
            title = self.env.titles[docname].astext() if docname in self.env.titles else ""
            text = doctree.astext()
            href = self.app.builder.get_relative_uri(self.config.master_doc, docname)
            self.output.append({
                'id': docname,
                'title': title,
                'content': text,
                'href': href,
            })
        outfname = os.path.join(self.outdir, 'searchindex.json')
        with open(outfname, 'w', encoding='utf-8') as f:
            json.dump({'docs': self.output}, f, ensure_ascii=False)

def setup(app):
    app.add_builder(JsonIndexBuilder)
