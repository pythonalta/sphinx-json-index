# About

`sphinx-jsonindex` is a simple sphinx extension to create a custom index of `html` files in the format of a `json` file. It could be used, for example, as the index for a search mechanism.

# Install

With `pip`:
```bash
pip install git+https://github.com/pythonalta/sphinx-jsonindex
```

With [py](https://github.com/ximenesyuri/py):
```bash
py install pythonalta/sphinx-jsonindex --from github
```

# Usage

In your `conf.py` file, add the lib as an extension:

```python
extensions = [ 'sphinx_jsonindex' ]
```

To generate the index, execute after the html build:
      
```bash 
sphinx-build -b jsonindex your_md_dir your_html_dir
```

# Configuration

You can configure the extension with the following variables:

1. `jsonindex-jsonindex_filename`: 
    - **meaning**: define the filename of the generated index file
    - **type**: string 
    - **default**: `index.json`
2. `jsonindex_add_html_suffix`:
    - **meaning**: determine if the `href` field of the index items contains the suffix `.html`
    - **type**: boolean
    - **default**: `True`

# Integration

TBA

# To Do

- improve customization of the fields in the index.
