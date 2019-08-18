# Plex Ratings Sync

A simple personal script for uploading track ratings to Plex.

Written in Python 3 using [PlexAPI][plexapi].

[plexapi]: https://python-plexapi.readthedocs.io/en/latest/introduction.html

## Installation

Use `pipenv` to set up the environment and install dependencies:

```bash
pipenv install
```

## Usage

Copy the `config.example.ini` file to `config.ini` and fill in the configuration as described in the [PlexAPI documentation][plexapi].

Then run the script using `pipenv`:

```bash
cp config.example.ini config.ini # Modify config to include server details
pipenv run ./plexratingssync.py
```
