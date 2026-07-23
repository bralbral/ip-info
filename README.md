
# ip-info-downloader

***Downloads selected IP2Location LITE databases and publishes CSV/MMDB/BIN artifacts.***


Getting Started
-------------

Linux
1. ```git clone https://github.com/bralbral/ip-info-downloader.git```
2. ```cd ip-info-downloader```
3. ```export IP2LOCATION_TOKEN=...```
4. ```bash start.sh```
5. Grab results from `dist`

docker-compose
1. ```git clone https://github.com/bralbral/ip-info-downloader.git```
2. ```cd ip-info-downloader```
3. ```docker-compose up```
5. Set `IP2LOCATION_TOKEN` for the container and grab results from `dist`.


Files
-------------
Downloaded databases

The default download list is DB11 CSV/MMDB/BIN, PX11 CSV/BIN, and ASN CSV/MMDB/BIN. The provider currently offers MMDB for DB11 and ASN; IP2Proxy LITE offers CSV, BIN and CIDR, but not MMDB.

Converted

Release assets are extracted from provider ZIP archives: CSV files are published as `*.csv.gz`; MMDB and BIN files are left intact. ZIP archives themselves are not released.

For every downloaded CSV, the project also creates `cidr_<source>.csv.gz`. It retains `ip_low` and `ip_high` and adds a `cidr` field. One source range can become several rows because not every IP range is exactly one [CIDR](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing) block. ASN CSV already has a CIDR field, so its `cidr_` file is retained as a normalized compressed copy.

GitHub Actions
-------------

`.github/workflows/publish.yml` runs at 05:17 UTC on the third day of each month and can also be started manually. It creates a dated `ip-data-YYYY-MM-DD` release and updates a release when manually re-run on the same day. Published releases are retained.

Before enabling it, configure repository settings:

1. Actions secret `IP2LOCATION_TOKEN` — private IP2Location download token.
The workflow uses the repository `GITHUB_TOKEN` only to publish and remove releases.
