## Automated IP2Location LITE download

This release is automatically produced by GitHub Actions from the current [IP2Location LITE](https://lite.ip2location.com/) databases. Source archives are downloaded directly from IP2Location using the repository owner's token, and CSV files are additionally converted to a CIDR representation.

| Release files | Contents |
| --- | --- |
| `IP2LOCATION-LITE-DB11.CSV.gz` | IP geolocation: country, region, city, coordinates, ZIP code, and time zone. |
| `cidr_IP2LOCATION-LITE-DB11.CSV.gz` | DB11 with CIDR; original `ip_low` and `ip_high` values are retained. One range may require multiple CIDR rows. |
| `IP2PROXY-LITE-PX11.CSV.gz` | Proxy data: type, country, region, city, ISP, domain, ASN, and threat indicators. |
| `cidr_IP2PROXY-LITE-PX11.CSV.gz` | PX11 with CIDR and retained original range boundaries. |
| `IP2LOCATION-LITE-ASN.CSV.gz` | ASN, autonomous system name, and source CIDR. |
| `cidr_IP2LOCATION-LITE-ASN.CSV.gz` | Normalized compressed ASN CSV copy; CIDR is already present in the source. |
| `*.MMDB` | MaxMind DB files for DB11 and ASN. Binary format; not gzip-compressed. |
| `*.BIN` | Binary databases for DB11, PX11, and ASN. Not gzip-compressed. |

The update runs monthly. Published releases are retained.

Use of this data is governed by the IP2Location LITE terms, including their attribution requirement.
