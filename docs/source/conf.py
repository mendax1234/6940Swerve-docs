# Configuration file for the Sphinx documentation builder.

# -- Project information

project = '6940 Swerve Documentation'
copyright = '2022, Wenbo Zhu (mendax1234)'
author = 'Wenbo Zhu (mendax1234)'

release = '1.0'
version = '1.0.0'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx_panels',
    'sphinx_search.extension',
    'sphinx.ext.mathjax',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# List of languages that frc-docs supports
localization_languages = [
    "en",
    "zh_CN",
]

# multi-language docs
language = 'en'
locale_dirs = ['../locales/']   # path is example but recommended.
gettext_compact = False  # optional.
gettext_uuid = True  # optional.

# -- Options for HTML output

html_theme = 'furo'

# Sidebar logo
html_logo = "assets/6940violetz-transparent.png"

# -- Options for EPUB output
epub_show_urls = 'footnote'

# Required to display LaTeX in hover content
hoverxref_mathjax = True

# Use MathJax3 for better page loading times
mathjax_path = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"

html_theme_options = {
    "sidebar_hide_name": True,
}