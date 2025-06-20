import csv
from typing import List, Dict, Any, Tuple, Union
from tabulate import tabulate
from exceptions import (
    InvalidFilterFormatException,
    InvalidSortFormatException,
    InvalidAggregationFormatException,
    NonNumericAggregationException
)


def read_csv(file_path: str) -> List[Dict[str, Any]]:
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]


def parse_filter(filter_str: str) -> Tuple[str, str, str]:
    operators = ['==', '!=', '<', '>', '<=', '>=']

    for op in operators:
        if op in filter_str:
            key, value = filter_str.split(op, 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            return key, op, value

    raise InvalidFilterFormatException(f"Invalid filter format: {filter_str}")


def parse_sort(sort_str: str) -> Tuple[str, str]:
    if '=' not in sort_str:
        raise InvalidSortFormatException(f"Invalid sort format: {sort_str}")
    key, order = sort_str.split('=', 1)
    key = key.strip()
    order = order.strip().lower()
    if order not in ['asc', 'desc']:
        raise InvalidSortFormatException(f"Invalid sort order: {order}")
    return key, order


def parse_aggregation(agg_str: str) -> Tuple[str, str]:
    if '=' not in agg_str:
        raise InvalidAggregationFormatException(
            f"Invalid aggregation format: {agg_str}"
        )
    column, operation = agg_str.split('=', 1)
    column = column.strip()
    operation = operation.strip().lower()
    if operation not in ['sum', 'avg', 'count', 'min', 'max']:
        raise InvalidAggregationFormatException(
            f"Invalid aggregation function: {operation}"
        )
    return column, operation


def try_convert(val: Any) -> Union[float, str]:
    try:
        return float(val)
    except (ValueError, TypeError):
        return str(val)


def apply_filter(
        data: List[Dict['str', Any]],
        filter_str: str
        ) -> List[Dict['str', Any]]:
    key, operator, value = parse_filter(filter_str)
    converted_value = try_convert(value)

    operators = {
        '==': lambda x: x == converted_value,
        '!=': lambda x: x != converted_value,
        '<': lambda x: x < converted_value,
        '>': lambda x: x > converted_value,
        '<=': lambda x: x <= converted_value,
        '>=': lambda x: x >= converted_value
    }

    try:
        return [
            row for row in data
            if operators[operator](try_convert(row[key]))
        ]
    except Exception as e:
        raise InvalidFilterFormatException(
            f"Error applying filter '{filter_str}': {e}"
        )


def apply_sort(
        data: List[Dict[str, Any]],
        sort_str: str) -> List[Dict[str, Any]]:
    column, order = parse_sort(sort_str)
    reverse = order == 'desc'
    return sorted(data, key=lambda x: try_convert(x[column]), reverse=reverse)


def apply_aggregation(
        data: List[Dict['str', Any]],
        agg_str: str) -> List[Dict[str, float]]:

    column, operation = parse_aggregation(agg_str)

    try:
        numeric_values = [float(row[column]) for row in data]
    except ValueError:
        raise NonNumericAggregationException(
            f"Column '{column}' contains non-numeric values"
        )

    operations = {
        'avg': lambda x: sum(x) / len(x),
        'min': lambda x: min(x),
        'max': lambda x: max(x),
        'sum': lambda x: sum(x),
        'count': lambda x: len(x)
    }
    result = operations[operation](numeric_values)
    return [{operation: result}]


def display_results(
    data: List[Dict[str, Any]],
):
    print(tabulate(data, headers="keys", tablefmt="grid"))
