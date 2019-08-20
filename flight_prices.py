import time
from argparse import ArgumentParser
from itertools import product

import pandas as pd
import sky_scanner_rapid_api


def parse_args():
    ap = ArgumentParser()

    ap.add_argument('--origin', type=str, required=True,
        help='Origin airports separated by comma ",".')

    ap.add_argument('--destination', type=str, required=True,
        help='Destination airports separated by comma ",".')

    ap.add_argument('--departure-date', type=str, required=True,
        help='Departure date formatted as YYYY-MM-DD.')
    
    ap.add_argument('--return-date', type=str, required=True,
        help='Return date formatted as YYYY-MM-DD.')

    ap.add_argument('--country', type=str, required=True,
        help='Country 2 digit Code. For example: "BR" for Brazil.')

    ap.add_argument('--api-key', type=str, required=True,
        help='Rapid API key.')

    ap.add_argument('--output', type=str, required=True,
        help='Output CSV file.')

    ap.add_argument('--output-summary', type=str, required=False,
        help='Output CSV file.')

    return ap.parse_args()


def build_query_queue(origin, destination, country):
    travels = product(origin.split(','), destination.split(','))
    for origin, destination in travels:
        origin_country = country
        try:
            temp = origin.split("/")
            origin, origin_country = temp
        except:
            pass

        if origin == destination:
            print(f'Skipping same location ({origin} -> {destination}).')
            continue

        yield (f"{origin.strip()}-sky", origin_country, f"{destination.strip()}-sky")


if __name__ == '__main__':
    args = parse_args()
    sky_scanner_rapid_api.RAPID_API_KEY = args.api_key
    df = pd.DataFrame(
        columns=['origin', 'destination', 'departure_date', 'return_date', 'price', 'country', 'link']
    )

    query_queue = list(build_query_queue(args.origin, args.destination, args.country))
    while query_queue:
        (origin, country, destination) = query_queue.pop()

        try:
            time.sleep(1)
            offers = list(sky_scanner_rapid_api.get_prices_for(
                origin,
                destination,
                args.departure_date,
                args.return_date,
                country
            ))
            if offers:
                df = df.append(offers)
            else:
                print(f'No offers found for {query}')
        except Exception as e:
            print(f'EXCEPTION while processing {origin} -> {destination} (Enqueing again):: {e}.')
            query_queue.append((origin, destination))
            time.sleep(2)

    print(f'Writing offers to {args.output}')
    df.to_csv(args.output)

    if args.output_summary:
        print(f'Writing summary to {args.output_summary}')
        prices = df.groupby(by=['origin', 'destination'])['price'].nsmallest(30)
        prices = prices.groupby(by=['origin', 'destination'])
        prices = prices.median().unstack()
        prices.to_csv(args.output_summary)
