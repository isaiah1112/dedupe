# Dedupe Utility
The `dedupe` utility was written in Python to help compare a directory of files, originally just image files,
and determine the duplicates based on an MD5 hash of the file.  SHA1 hashing was later added because, well, it just was.

## Getting Started
To install or update `dedupe`, simply use `pip` or the `make` command:

### Using pip
```commandline
python -m pip install -U .
```

### Using make
```commandline
make install
```

This will install/update all requirements and enable a `dedupe` command in your environment.
