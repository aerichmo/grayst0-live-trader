"""
Minimal “does-it-start?” smoke test suite.
"""

import importlib

import pytest

MODULES = ["requests", "yaml"]


@pytest.mark.parametrize("module_name", MODULES)
def test_can_import(module_name: str) -> None:
    assert importlib.import_module(module_name)
