# Dedupe Utility

[![Python Tests](https://github.com/isaiah1112/dedupe/actions/workflows/python-tests.yml/badge.svg)](https://github.com/isaiah1112/dedupe/actions/workflows/python-tests.yml)

The `dedupe` utility was written in Python to help compare a directory of files, originally just image files,
and determine the duplicates based on different hashing algorithms.

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

## Usage Examples ✅

After installation, the `dedupe` command will be available in your environment.

### Find duplicates (default: md5)
```commandline
# Scan a folder and report duplicates (default algorithm: md5)
dedupe ~/Pictures/Wallpapers
```
Possible output:
```
No duplicate files found
```
or
```
Found 1 duplicate file(s)!
Duplicate files moved to: /Users/you/Pictures/Wallpapers/duplicates/
```

### Use a different hash algorithm (sha1, sha256, blake3)
```commandline
# Use SHA-256 for comparisons
dedupe --hash sha256 ~/Videos

# Use BLAKE3 (fast modern hash)
dedupe --hash blake3 ~/Videos
```
Possible output when duplicates exist:
```
Found 2 duplicate file(s)!
Duplicate files moved to: ~/Videos/duplicates/
```

### Remove duplicates instead of moving them
```commandline
# Permanently remove duplicate files
# (use with caution!)
dedupe --remove ~/MyFolder
```
Possible output:
```
Found 1 duplicate file(s)!
Duplicate files removed!
```

### Debug / verbose mode
```commandline
dedupe --debug ~/SomeFolder
```
This enables additional logging for troubleshooting.