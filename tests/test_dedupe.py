import hashlib

from blake3 import blake3
from click.testing import CliRunner

from dedupe import cli, hash_file


def test_hashes(tmp_path):
    p = tmp_path / "hello.txt"
    p.write_text("hello world")

    assert hash_file(str(p), algorithm='md5') == hashlib.md5(b"hello world").hexdigest()
    assert hash_file(str(p), algorithm='sha1') == hashlib.sha1(b"hello world").hexdigest()

    # new: verify sha256 and blake3
    assert hash_file(str(p), algorithm='sha256') == hashlib.sha256(b"hello world").hexdigest()

    h = blake3()
    h.update(b"hello world")
    assert hash_file(str(p), algorithm='blake3') == h.hexdigest()


def test_cli_no_duplicates(tmp_path):
    (tmp_path / "a.txt").write_text("one")
    (tmp_path / "b.txt").write_text("two")

    runner = CliRunner()
    result = runner.invoke(cli, ["--debug", str(tmp_path)])

    assert result.exit_code == 0
    assert "No duplicate files found" in result.output


def test_cli_moves_duplicates(tmp_path):
    # two different filenames with identical contents
    f1 = tmp_path / "one.txt"
    f2 = tmp_path / "two.txt"
    f1.write_text("same")
    f2.write_text("same")

    runner = CliRunner()
    result = runner.invoke(cli, ["--debug", str(tmp_path)])

    assert result.exit_code == 0
    assert "Found 1 duplicate file(s)!" in result.output
    assert "Duplicate files moved to:" in result.output

    duplicates_dir = tmp_path / "duplicates"
    assert duplicates_dir.exists()
    # exactly one of the two files should be in the duplicates directory
    moved = list(duplicates_dir.iterdir())
    assert len(moved) == 1
    moved_name = moved[0].name
    assert moved_name in {"one.txt", "two.txt"}

    # the other file should still exist in the original folder
    remaining = {p.name for p in tmp_path.iterdir() if p.is_file()}
    assert len(remaining.intersection({"one.txt", "two.txt"})) == 1


def test_cli_remove_duplicates(tmp_path):
    f1 = tmp_path / "keep.txt"
    f2 = tmp_path / "remove.txt"
    f1.write_text("same")
    f2.write_text("same")

    runner = CliRunner()
    result = runner.invoke(cli, ["--debug", "--remove", str(tmp_path)])

    assert result.exit_code == 0
    assert "Found 1 duplicate file(s)!" in result.output
    assert "Duplicate files removed!" in result.output

    # duplicates dir should not exist
    assert (tmp_path / "duplicates").exists() is False

    # only one file should remain
    remaining_files = [p for p in tmp_path.iterdir() if p.is_file()]
    assert len(remaining_files) == 1


def test_cli_sha1_option(tmp_path):
    f1 = tmp_path / "a1.txt"
    f2 = tmp_path / "a2.txt"
    f1.write_text("same")
    f2.write_text("same")

    runner = CliRunner()
    result = runner.invoke(cli, ["--debug", "--hash", "sha1", str(tmp_path)])

    assert result.exit_code == 0
    assert "Found 1 duplicate file(s)!" in result.output


def test_cli_blake3_option(tmp_path):
    f1 = tmp_path / "a1.txt"
    f2 = tmp_path / "a2.txt"
    f1.write_text("same")
    f2.write_text("same")

    runner = CliRunner()
    result = runner.invoke(cli, ["--debug", "--hash", "blake3", str(tmp_path)])

    assert result.exit_code == 0
    assert "Found 1 duplicate file(s)!" in result.output


def test_hidden_files_ignored(tmp_path):
    # create a visible file and a hidden file with the same contents; hidden should be ignored
    (tmp_path / "visible.txt").write_text("same")
    (tmp_path / ".hidden.txt").write_text("same")

    runner = CliRunner()
    result = runner.invoke(cli, ["--debug", str(tmp_path)])

    assert result.exit_code == 0
    # since the hidden file is ignored there should be no duplicates
    assert "No duplicate files found" in result.output
