from pathlib import Path
import tempfile
import os
import projdir
import pytest

from projdir.core import MarkerNotFound

MARKER_NAME = "marker-file-funny-name-not-reasonably-found-on-test-machine"


def test_find_file_standing_in_projdir(tmp_path: Path):
    os.chdir(tmp_path)
    (tmp_path / MARKER_NAME).touch()
    result = projdir.find(MARKER_NAME)
    assert result.exists()
    assert result == tmp_path


def test_no_file_found_file_not_found_error(tmp_path: Path):
    os.chdir(tmp_path)
    with pytest.raises(FileNotFoundError):
        projdir.find(MARKER_NAME)


def test_no_file_found_custom_error(tmp_path: Path):
    os.chdir(tmp_path)
    with pytest.raises(projdir.MarkerNotFound):
        projdir.find(MARKER_NAME)


def test_find_file_standing_in_subdir(tmp_path: Path):
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    os.chdir(subdir)
    (tmp_path / MARKER_NAME).touch()
    result = projdir.find(MARKER_NAME)
    assert result == tmp_path


def test_find_nested_marker(tmp_path: Path):
    subdir = tmp_path / "nested" / "directories"
    subdir.mkdir(parents=True)
    marker_path = subdir / MARKER_NAME
    marker_path.touch()
    os.chdir(tmp_path)
    result = projdir.find(marker_path)
    assert result == tmp_path


def test_find_only_file_finds_file(tmp_path: Path):
    os.chdir(tmp_path)
    (tmp_path / MARKER_NAME).touch()
    result = projdir.find(MARKER_NAME, dir_ok=False)
    assert result == tmp_path


def test_find_only_file_does_not_accept_dir(tmp_path: Path):
    os.chdir(tmp_path)
    (tmp_path / MARKER_NAME).mkdir()

    with pytest.raises(MarkerNotFound):
        projdir.find(MARKER_NAME, dir_ok=False)


def test_find_only_dir_finds_dir(tmp_path: Path):
    os.chdir(tmp_path)
    (tmp_path / MARKER_NAME).mkdir()
    result = projdir.find(MARKER_NAME, file_ok=False)
    assert result == tmp_path


def test_find_only_dir_does_not_accept_file(tmp_path: Path):
    os.chdir(tmp_path)
    (tmp_path / MARKER_NAME).touch()

    with pytest.raises(MarkerNotFound):
        projdir.find(MARKER_NAME, file_ok=False)


def test_find_only_file_is_not_fooled_by_dir(tmp_path: Path):
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    os.chdir(subdir)

    real_marker_path = tmp_path / MARKER_NAME
    real_marker_path.touch()

    confusing_directory = subdir / MARKER_NAME
    confusing_directory.mkdir()

    result = projdir.find(MARKER_NAME, dir_ok=False)
    assert result == real_marker_path.parent


def test_find_only_dir_is_not_fooled_by_file(tmp_path: Path):
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    os.chdir(subdir)

    real_marker_path = tmp_path / MARKER_NAME
    real_marker_path.mkdir()

    confusing_file = subdir / MARKER_NAME
    confusing_file.touch()

    result = projdir.find(MARKER_NAME, file_ok=False)
    assert result == real_marker_path.parent


def test_find_file_standing_in_subdir(tmp_path: Path):
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    os.chdir(subdir)
    (tmp_path / MARKER_NAME).touch()
    result = projdir.find(MARKER_NAME)
    assert result.is_absolute()
