import pytest
from csv_processor.utils import (
    parse_aggregation,
    parse_filter,
    parse_sort,
)
from csv_processor.exceptions import (
    InvalidAggregationFormatException,
    InvalidFilterFormatException,
    InvalidSortFormatException,
)


@pytest.mark.parametrize("agg_str, expected", [
    ("price=sum", ("price", "sum")),
    ("price=avg", ("price", "avg")),
    ("price=count", ("price", "count")),
    ("price=min", ("price", "min")),
    ("price=max", ("price", "max")),
    ("  price  =  SUM  ", ("price", "sum")),
])
def test_parse_aggregation_valid_inputs(agg_str, expected):
    assert parse_aggregation(agg_str) == expected


@pytest.mark.parametrize("agg_str", [
    "invalid_format",
    "price=",
    "=sum",
    "price=unknown_func"
])
def test_parse_aggregation_invalid_inputs(agg_str):
    with pytest.raises(InvalidAggregationFormatException):
        parse_aggregation(agg_str)


@pytest.mark.parametrize("filter_str, expected", [
    ("price==100", ("price", "==", "100")),
    ("rating!=5", ("rating", "!=", "5")),
    ("price<1000", ("price", "<", "1000")),
    ("price>500", ("price", ">", "500")),
    ("rating<=4.5", ("rating", "<=", "4.5")),
    ("rating>=4.0", ("rating", ">=", "4.0")),
    ('brand=="apple"', ("brand", "==", "apple")),
    ("name!='iphone'", ("name", "!=", "iphone")),
])
def test_parse_filter_valid_inputs(filter_str, expected):
    assert parse_filter(filter_str) == expected


@pytest.mark.parametrize("filter_str", [
    "invalid_format",
    ">=10",
])
def test_parse_filter_invalid_inputs(filter_str):
    with pytest.raises(InvalidFilterFormatException):
        parse_filter(filter_str)


@pytest.mark.parametrize("sort_str, expected", [
    ("price=desc", ("price", "desc")),
    ("price=asc", ("price", "asc")),
])
def test_parse_sort_valid_inputs(sort_str, expected):
    assert parse_sort(sort_str) == expected


@pytest.mark.parametrize("sort_str", [
    "invalid_format",
    "price=invalid_order",
    "=desc"
])
def test_parse_sort_invalid_inputs(sort_str):
    with pytest.raises(InvalidSortFormatException):
        parse_sort(sort_str)
