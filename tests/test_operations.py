import os
import tempfile
import pytest
from csv_processor.utils import (
    read_csv,
    apply_aggregation,
    apply_filter,
    apply_sort
)
from csv_processor.exceptions import (
    InvalidFilterFormatException,
    InvalidSortFormatException,
    InvalidAggregationFormatException,
    NonNumericAggregationException
)


@pytest.fixture
def sample_csv():
    content = '''name,brand,price,rating
iphone 15 pro,apple,999,4.9
galaxy s23 ultra,samsung,1199,4.8
redmi note 12,xiaomi,199,4.6
poco x5 pro,xiaomi,299,4.4'''
    f = tempfile.NamedTemporaryFile(mode='w', delete=False)
    f.write(content)
    f.close()
    yield f.name
    os.unlink(f.name)


def test_read_csv(sample_csv):
    data = read_csv(sample_csv)
    assert len(data) == 4
    assert data[0]['name'] == 'iphone 15 pro'
    assert data[1]['brand'] == 'samsung'


@pytest.mark.parametrize("agg_str, expected", [
        ("price=sum", [{"sum": 2696}]),
        ("price=avg", [{"avg": 674}]),
        ("price=count", [{"count": 4}]),
        ("rating=min", [{"min": 4.4}]),
        ("price=max", [{"max": 1199}])
    ])
def test_apply_aggregation(sample_csv, agg_str, expected):
    data = read_csv(sample_csv)
    result = apply_aggregation(data, agg_str)
    assert result == expected


def test_apply_aggregation_non_numeric(sample_csv):
    data = read_csv(sample_csv)
    with pytest.raises(NonNumericAggregationException):
        apply_aggregation(data, "brand=sum")


@pytest.mark.parametrize("agg_str", [
    "invalid_format", "price=",
    "=sum",
    "price=unknown_func"
    ])
def test_apply_aggregation_invalid(sample_csv, agg_str):
    data = read_csv(sample_csv)
    with pytest.raises(InvalidAggregationFormatException):
        apply_aggregation(data, agg_str)


@pytest.mark.parametrize("filter_str, expected_rows", [
        ("price == 999", [0]),
        ("brand != xiaomi", [0, 1]),
        ("rating < 4.5", [3]),
        ("price > 300", [0, 1]),
        ("rating <= 4.6", [2, 3]),
        ("rating >= 4.4", [0, 1, 2, 3]),
        ('brand == "apple"', [0]),
        ("name != 'redmi note 12'", [0, 1, 3]),
    ]
)
def test_apply_filter(sample_csv, filter_str, expected_rows):
    data = read_csv(sample_csv)
    result = apply_filter(data, filter_str)
    assert result == [data[i] for i in expected_rows]


@pytest.mark.parametrize("filter_str", [
        "invalid_format",
        ">=10",
        "price < 1000 and brand == 'apple'",
        "rating > 4.5 or price < 300"
        "nonexistent_column == 'value'",
    ])
def test_apply_filter_invalid_input(sample_csv, filter_str):
    data = read_csv(sample_csv)
    with pytest.raises(InvalidFilterFormatException):
        apply_filter(data, filter_str)


@pytest.mark.parametrize("sort_str, expected_order", [
        ("price=desc", [1, 0, 3, 2]),
        ("price=asc", [2, 3, 0, 1]),
        ("rating=asc", [3, 2, 1, 0]),
        ("rating=desc", [0, 1, 2, 3]),
        ("name=asc", [1, 0, 3, 2]),
        ("name=desc", [2, 3, 0, 1]),
    ])
def test_apply_sort(sample_csv, sort_str, expected_order):
    data = read_csv(sample_csv)
    result = apply_sort(data, sort_str)
    assert [data.index(row) for row in result] == expected_order


@pytest.mark.parametrize("sort_str", [
    "invalid_format",
    "price=invalid_order",
    "nonexistent_column=desc"
])
def test_apply_sort_invalid_input(sample_csv, sort_str):
    data = read_csv(sample_csv)
    with pytest.raises(InvalidSortFormatException):
        apply_sort(data, sort_str)
