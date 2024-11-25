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
release = "0.4.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosummary",
    "sphinx_autodoc_typehints",
]

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
language = "en"
locale_dirs = ['locale/']  # Diretório para arquivos de tradução
gettext_compact = False   # Melhor para ferramentas de tradução

autosummary_generate = True

html_sidebars = {
    "**": [
        "globaltoc.html",
        "relations.html",  # links to next/prev documents
        "sourcelink.html",  # link to view the source
        "searchbox.html",  # search box
    ]
}

html_theme_options = {
    "navigation_depth": 3,  # Número de níveis exibidos no menu lateral
    "collapse_navigation": False,  # Expande todas as seções do menu
    "sticky_navigation": True,  # Fixa o menu lateral ao rolar a página
}

autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "private-members": False,  # Defina como True se quiser incluir membros privados
    "special-members": "__init__",  # Inclui métodos especiais como __init__
    "inherited-members": True,
    "show-inheritance": True,
}