# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# Import the package to get version
import cubeforge

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'CubeForge'
author = 'Teddy van Jerry (Wuqiong Zhao)'
release = cubeforge.__version__
version = cubeforge.__version__

# Copyright text (plain text version for metadata)
copyright = '2025, Teddy van Jerry (Wuqiong Zhao)'

# Custom HTML for footer with link - use Jinja2 Markup to prevent escaping
from markupsafe import Markup
html_context = {
    'display_github': True,
    'github_user': 'Teddy-van-Jerry',
    'github_repo': 'cubeforge',
    'github_version': 'master',
    'copyright_html': Markup('2025, Teddy van Jerry (<a href="https://wqzhao.org" target="_blank" rel="noopener">Wuqiong Zhao</a>)'),
}

# Use raw HTML for copyright in Furo theme
html_show_copyright = True

# Allow raw HTML in configuration values
rst_epilog = ""

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosummary',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
html_title = 'CubeForge'

# Furo theme options
html_theme_options = {
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "top_of_page_button": "edit",
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/Teddy-van-Jerry/cubeforge",
            "html": "",
            "class": "",
        },
    ],
}

# Logo and favicon (optional, uncomment if you add these)
# html_logo = "_static/logo.png"
# html_favicon = "_static/favicon.ico"

# -- Extension configuration -------------------------------------------------

# Napoleon settings for Google-style and NumPy-style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# Intersphinx mapping to link to Python docs
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

# Autosummary settings
autosummary_generate = True
