"""Download selected IP2Location archives into a working directory."""

import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen


# DB11 and ASN have MMDB editions. IP2Proxy LITE currently does not.
DEFAULT_CODES = (
    "DB11LITECSV",
    "PX11LITECSV",
    "DBASNLITE",
    "DB11LITEMMDB",
    "DBASNLITEMMDB",
    "DB11LITEBIN",
    "PX11LITEBIN",
    "DBASNLITEBIN",
)


def download(code: str, output_dir: Path, token: str) -> Path:
    destination = output_dir / f"{code}.zip"
    temporary = destination.with_suffix(".zip.part")
    url = "https://www.ip2location.com/download?" + urlencode({"token": token, "file": code})
    try:
        with urlopen(url, timeout=60 * 60) as response, temporary.open("wb") as file:
            while chunk := response.read(1024 * 1024):
                file.write(chunk)
    except (HTTPError, URLError) as error:
        temporary.unlink(missing_ok=True)
        raise RuntimeError(f"IP2Location download failed for {code}: {error}") from error
    if temporary.stat().st_size == 0:
        temporary.unlink(missing_ok=True)
        raise RuntimeError(f"Downloaded empty archive for {code}")
    temporary.replace(destination)
    return destination


def main() -> None:
    token = os.environ.get("IP2LOCATION_TOKEN")
    if not token:
        raise RuntimeError("IP2LOCATION_TOKEN must be set")
    output_dir = Path(os.environ.get("DOWNLOAD_DIR", "downloads"))
    output_dir.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=len(DEFAULT_CODES)) as executor:
        downloaded = list(executor.map(lambda code: download(code, output_dir, token), DEFAULT_CODES))
    print("Downloaded:", ", ".join(str(path) for path in downloaded))


if __name__ == "__main__":
    main()
