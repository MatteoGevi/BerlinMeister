# Berlin Apartment Finder 🏠

![Berlin](https://img.shields.io/badge/Berlin-DE--BE-red?style=flat&logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA2NDAgNDgwIj48cGF0aCBmaWxsPSIjREUwMDAyIiBkPSJNMCAwaDY0MHY0ODBIMHoiLz48L3N2Zz4=)

An automated tool to help find and track Berlin apartment listings. This tool monitors various real estate websites and sends notifications when new apartments matching your criteria are found.

## Features

- 🔍 Monitors multiple real estate websites (ImmobilienScout24, WG-Gesucht, etc.)
- ⚙️ Customizable search criteria (size, price, location)
- 📧 Automated email notifications for new listings
- 🎯 Filtering capabilities to avoid duplicates
- 🏙️ Support for popular Berlin neighborhoods

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   poetry install
   ```
3. Create a `.env` file with your configuration:
   ```env
   EMAIL=your@email.com
   MAX_PRICE=2000
   MIN_ROOMS=2
   PREFERRED_AREAS=Mitte,Prenzlauer Berg,Friedrichshain
   ```
4. Run the script:
   ```bash
   poetry run python berlin_apartment_finder/main.py
   ```

## Supported Websites

- ImmobilienScout24
- WG-Gesucht
- ImmoWelt
- eBay Kleinanzeigen

## Contributing

Feel free to contribute by adding more website scrapers or improving the existing functionality.
