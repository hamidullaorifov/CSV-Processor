import pytest
import sys
from main import main


CSV_CONTENT = """name,brand,price,rating
iphone 15 pro,apple,999,4.9
galaxy s23 ultra,samsung,1199,4.8
redmi note 12,xiaomi,199,4.6
poco x5 pro,xiaomi,299,4.4
"""


@pytest.fixture
def csv_file(tmp_path):
    file = tmp_path / "sample.csv"
    file.write_text(CSV_CONTENT)
    return str(file)


def run_main_with_args(monkeypatch, args):
    monkeypatch.setattr(sys, "argv", ["main.py"] + args)
    main()


def test_main_filter_only(csv_file, monkeypatch, capsys):
    run_main_with_args(
        monkeypatch,
        ["--file", csv_file, "--where", "price>1000"]
    )
    out, _ = capsys.readouterr()
    assert "galaxy s23 ultra" in out
    assert "redmi note 12" not in out


def test_main_sort_only(csv_file, monkeypatch, capsys):
    run_main_with_args(
        monkeypatch,
        ["--file", csv_file, "--order-by", "price=asc"]
    )
    out, _ = capsys.readouterr()
    assert "redmi note 12" in out.splitlines()[3]


def test_main_aggregate_only(csv_file, monkeypatch, capsys):
    run_main_with_args(
        monkeypatch,
        ["--file", csv_file, "--aggregate", "price=sum"]
    )
    out, _ = capsys.readouterr()
    assert "sum" in out
    assert "2696" in out


def test_main_filter_and_aggregate(csv_file, monkeypatch, capsys):
    run_main_with_args(
        monkeypatch,
        [
            "--file",
            csv_file,
            "--where",
            "brand==xiaomi",
            "--aggregate",
            "price=avg"
        ]
    )
    out, _ = capsys.readouterr()
    assert "avg" in out
    assert "249" in out  # (199+299)/2


def test_main_invalid_filter(csv_file, monkeypatch, capsys):
    with pytest.raises(SystemExit):
        run_main_with_args(
            monkeypatch,
            ["--file", csv_file, "--where", "price<>999"]
        )
    out, err = capsys.readouterr()
    assert "Error" in out
    assert "Invalid filter format" in out
