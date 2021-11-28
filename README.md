# Typical usage

1. Place a file named `.marker-file` somewhere in your file system.
2. From the directory containing the `.marker-file`, or any (nested) subdirectory, you can now use use `projdir` to find the path of the directory containing `.marker-file`:

```python
import projdir
import whatever_package

base_dir = projdir.find(".marker-file")  # returns a pathlib.Path object

indata_path = base_dir / "indata"
output_path = base_dir / "result.csv"

whatever_package.create_output_file(indata_path, output_path)
```

# Motivation

- Let's say you are building a Python application (script, command-line tool, whatever) that relies on file system inputs or outputs.
- The expected file inputs or outputs do not have a fixed path compared to the Python script, and you don't want to hard-code an absolute path to the working directory.
- This is similar to Git's `.git` directory, which not only contains the repository database but also marks the root directory of the repository.

# More examples

## Match only files or only directories

```python
base_dir = projdir.find(".marker-file", dir_ok=False)  # Match only files
base_dir = projdir.find(".marker-dir", file_ok=False)  # Match only dirs
```

## Find a config file

Simple rule: `projdir.find()` always returns the containing directory. If you want the matching file or directory, this is easily done:

```python
CONFIG_FILE_NAME = ".myappconfig"
base_dir = projdir.find(".myappconfig", dir_ok=False)
config_path = base_dir / CONFIG_FILE_NAME
```

## Use a nested marker file or directory

`projdir.find(marker_relpath)` always returns a directory `base_dir` such that `base_dir / marker_relpath` exists. This holds even if `marker_relpath` is a nested relative path.

```python
# This will return the outer directory, the one that contains `subdirectory`
base_dir = projdir.find("subdirectory/with/marker-file")
```

# Some technical details

- `projdir.find()` always searches from the current working directory.
- If the marker cannot be found in the current working directory, the search continues step by step up the directory tree until the drive root, i.e. "/marker_relpath" on Unix or something like "C:\marker_relpath" on Windows.
- If the marker is not found, the custom `projdir.MarkerNotFound` exception is raised. `MarkerNotFound` is a subclass of `FileNotFoundError`.
- `projdir.find()` always returns an absolute path. Finding the result relative to the current working directory, without resolving symlinks, would be a little more complicated. I cannot see a use case for relative paths, but if you do, feel free to get in touch.
