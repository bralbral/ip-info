"""Publish compressed source files and CIDR-expanded CSV files."""

import csv
import gzip
import ipaddress
import os
from pathlib import Path
import zipfile


HEADERS = {
    "DB11LITECSV": ["ip_low", "ip_high", "country_code", "country_name", "region_name", "city_name", "latitude", "longitude", "zip_code", "time_zone"],
    "PX11LITECSV": ["ip_low", "ip_high", "proxy_type", "country_code", "country_name", "region_name", "city_name", "internet_service_provider", "domain", "usage_type", "autonomous_system_number", "autonomous_system", "last_seen", "security_threat", "provider"],
    "DBASNLITE": ["ip_low", "ip_high", "cidr", "autonomous_system_number", "autonomous_system"],
}


def cidrs(ip_low: str, ip_high: str) -> list[str]:
    """Represent the whole inclusive range; a range may need several CIDRs."""
    start, end = ipaddress.ip_address(int(ip_low)), ipaddress.ip_address(int(ip_high))
    if start.version != end.version or int(start) > int(end):
        raise ValueError(f"Invalid IP range: {ip_low}..{ip_high}")
    return [str(network) for network in ipaddress.summarize_address_range(start, end)]


def convert_csv(archive: Path, member: str, header: list[str], output_dir: Path) -> Path:
    source_name = Path(member).name
    output = output_dir / f"cidr_{source_name}.gz"
    has_cidr = "cidr" in header
    output_header = header if has_cidr else ["cidr", *header]
    with zipfile.ZipFile(archive) as source, gzip.open(output, "wt", encoding="latin1", newline="") as compressed:
        with source.open(member) as raw:
            reader = csv.reader((line.decode("latin1") for line in raw))
            writer = csv.writer(compressed, lineterminator="\n", quoting=csv.QUOTE_ALL)
            writer.writerow(output_header)
            for row_number, row in enumerate(reader, start=1):
                if len(row) != len(header):
                    raise ValueError(f"{archive}:{member}:{row_number}: expected {len(header)} columns, got {len(row)}")
                if has_cidr:
                    writer.writerow(row)
                else:
                    for network in cidrs(row[0], row[1]):
                        writer.writerow([network, *row])
    return output


def publish_originals(archive: Path, output_dir: Path) -> list[Path]:
    """Extract data files. CSV is gzip-compressed; binary formats stay intact."""
    published: list[Path] = []
    supported = {".csv", ".mmdb", ".bin"}
    with zipfile.ZipFile(archive) as source:
        for member in source.namelist():
            source_name = Path(member).name
            suffix = Path(source_name).suffix.lower()
            if not source_name or suffix not in supported:
                continue
            destination = output_dir / (source_name if suffix in {".bin", ".mmdb"} else f"{source_name}.gz")
            with source.open(member) as raw:
                if suffix in {".bin", ".mmdb"}:
                    with destination.open("wb") as target:
                        target.write(raw.read())
                else:
                    with gzip.open(destination, "wb") as target:
                        target.write(raw.read())
            published.append(destination)
    return published


def main() -> None:
    output_dir = Path(os.environ.get("OUTPUT_DIR", "dist"))
    input_dir = Path(os.environ.get("DOWNLOAD_DIR", "downloads"))
    output_dir.mkdir(parents=True, exist_ok=True)
    converted: list[Path] = []
    originals: list[Path] = []
    for archive in sorted(input_dir.glob("*.zip")):
        originals.extend(publish_originals(archive, output_dir))
        header = HEADERS.get(archive.stem)
        if not header:  # MMDB/BIN archives have no CSV ranges to convert.
            continue
        with zipfile.ZipFile(archive) as source:
            members = [name for name in source.namelist() if name.lower().endswith(".csv")]
        if not members:
            raise RuntimeError(f"{archive} does not contain a CSV file")
        converted.extend(convert_csv(archive, member, header, output_dir) for member in members)
    print("Published:", ", ".join(str(path) for path in [*originals, *converted]))


if __name__ == "__main__":
    main()
