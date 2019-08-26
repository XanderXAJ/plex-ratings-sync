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

The ratings data needs to be in one of the following formats:

-   Google Play Music JSON format, as dumped by [Google Music Ratings Sync][google-sync] (`google_play_json`).
-   Double-colon-delimited data in the following format (`double_colon`):

        title :: artist :: album :: track number :: disc number :: rating

    In foobar2000, use the Text Tools plugin to export data for all rated tracks with the following template:

        %title% :: $meta(artist,0) :: %album% :: [%tracknumber%] :: [%discnumber%] :: $if2([%rating%],0)

[google-sync]: https://github.com/XanderXAJ/google-music-ratings-sync

Then run the script using `pipenv`:

```bash
cp config.example.ini config.ini # Modify config to include server details
pipenv run ./plexratingssync.py --input_format google_play_json downloaded_ratings.json
```
