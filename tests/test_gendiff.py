import os
from gendiff.scripts.gendiff import generate_diff
from definitions import ROOT_DIR


def test_gendiff():
    actual_diff = generate_diff(
        os.path.join(ROOT_DIR, 'file1.json'),
        os.path.join(ROOT_DIR, 'file2.json'),
        format='stylish'
    )

    with open(os.path.join(ROOT_DIR, 'tests/fixtures/result.txt'), 'r') as file:
        expected_diff = file.read()

    assert actual_diff == expected_diff
