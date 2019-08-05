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
    --origin "NVT-sky" --destination "RIOA-sky" --country="BR" \
    --departure-date "2019-09-17" --return-date "2019-09-21" \
    --api-key "YOUR API KEY" --output "nvt-rio-flight-prices.csv"
```

Please note the suffix `-sky` in `origin` and `destination`.
This is required because of Sky Scanner's API.
`country` is the country to look for offers.
This is usually the country of `origin` airport.

To get a list of airports, this might help https://rapidapi.com/skyscanner/api/skyscanner-flight-search?endpoint=5a9c9edde4b084deb4ea6195