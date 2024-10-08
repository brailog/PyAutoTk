import sys

sys.path.insert(0, "/home/gabriel/Documents/source_workspace/pyautotk")

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "PyAutoTk"
copyright = "2024, Gabriel Ramos R. Oliveira"
author = "Gabriel Ramos R. Oliveira"
release = "0.3"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosummary",
]

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

autosummary_generate = True

html_sidebars = {
    "**": [
        "globaltoc.html",
        "relations.html",  # links to next/prev documents
        "sourcelink.html",  # link to view the source
        "searchbox.html",  # search box
    ]
}
