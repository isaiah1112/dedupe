# Dedupe Utility
The `dedupe` utility was written in Python to help compare a directory of files, originally just image files,
and determine the duplicates based on an MD5 hash of the file.  SHA1 hashing was later added because, well, it just was.

## Getting Started
To install or update `dedupe`, the `make` command:

### Using make
```commandline
make install
```

If you do not want to use `uv` to install `dedupe`:
```commandline
make install UV_INSTALL=0
```

This will install/update all requirements and enable a `dedupe` command in your environment.
