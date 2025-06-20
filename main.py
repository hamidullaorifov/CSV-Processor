import argparse
from utils import (
    read_csv,
    apply_aggregation,
    apply_filter,
    apply_sort,
    display_results
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Process CSV files with filtering, sorting and aggregation"
    )

    parser.add_argument(
        '--file',
        type=str,
        help='path to csv file'
    )

    parser.add_argument(
        '--where',
        type=str,
        help='Condition in format "col>val" or similar (>,<,>=,<=,==,!=)'
    )

    parser.add_argument(
        '--order-by',
        type=str,
        help='Order by column in format "column=asc" or "column=desc"'
    )

    parser.add_argument(
        '--aggregate',
        type=str,
        help='Aggregation in format "column=operation" (avg,min,max,sum,count)'
    )

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    try:
        data = read_csv(args.file)

        if args.where:
            data = apply_filter(data, args.where)

        if args.order_by:
            data = apply_sort(data, args.order_by)

        aggregation_result = None
        if args.aggregate:
            aggregation_result = apply_aggregation(data, args.aggregate)
            display_results(aggregation_result)
        else:
            display_results(data)
    except Exception as e:
        print(f'Error: {e}')
        exit(1)


if __name__ == '__main__':
    main()
