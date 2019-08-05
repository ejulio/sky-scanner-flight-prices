from argparse import ArgumentParser
import time

import pandas as pd

import sky_scanner_rapid_api


def parse_args():
    ap = ArgumentParser()

    ap.add_argument('--origin', type=str, required=True,
        help='Origin airports (Sky scanner API, may require "-sky" suffix) separated by comma ",".')

    ap.add_argument('--destination', type=str, required=True,
        help='Destination airports (Sky scanner API, may require "-sky" suffix) separated by comma ",".')

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

    return ap.parse_args()


def build_query_queue(origin, destination):
    for o in origin.split(','):
        for d in destination.split(','):
            yield (o.strip(), d.strip())


if __name__ == '__main__':
    args = parse_args()
    sky_scanner_rapid_api.RAPID_API_KEY = args.api_key
    df = pd.DataFrame(
        columns=['origin', 'destination', 'departure_date', 'return_date', 'price', 'country', 'link']
    )

    query_queue = list(build_query_queue(args.origin, args.destination))
    while query_queue:
        (origin, destination) = query_queue.pop()
        try:
            time.sleep(1)
            offers = list(sky_scanner_rapid_api.get_prices_for(
                origin,
                destination,
                args.departure_date,
                args.return_date,
                args.country
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
