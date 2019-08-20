# Sky Scanner Flight Prices

This is a simple Command Line Interface (CLI) to fetch flight prices from multiple origins/destinations.

This is handy to estimate flight prices for groups leaving from different places or to find a place
cheaper for all!

## Setup

Go to https://rapidapi.com/ and login/signup for an API KEY

```
git clone
cd sky-scanner-flight-prices
python3 -m venv .venv  # or any virtual environment you like
pip install -r requirements.txt
```

## Running

```
python flight_prices.py \
    --origin "NVT/BR" \
    --country="BR" \
    --destination "RIOA" \
    --departure-date "2019-09-17" \
    --return-date "2019-09-21" \
    --api-key "YOUR API KEY" \
    --output "flight-prices.csv" \
    --output "summary.csv" \
```

Please note the suffix `/BR` in `origin` is only required if you are booking flights from different origin countries.
`country` is the country to look for offers.
This is usually the country of `origin` airport.
If no specified on `origin` this value will be used.

To get a list of airports, this might help https://rapidapi.com/skyscanner/api/skyscanner-flight-search?endpoint=5a9c9edde4b084deb4ea6195