# py-geohex3
Geohex v3.2 python implementation.

[![Build Status](https://travis-ci.org/uncovertruth/py-geohex3.svg?branch=master)](https://travis-ci.org/uncovertruth/py-geohex3)

## Install

### PyPI

```shell
pip install py-geohex3
```

### from source

```shell
git clone https://github.com/uncovertruth/py-geohex3.git

cd py-geohex3
python setup.py install
```


## Usage

```python
import geohex

## retrieve geohex code from latitude / longitude
zone = geohex.get_zone_by_location(35.65858, 139.745433, 11)
print(zone.code)
# 'XM48854457273'

## retrieve location from geohex code
zone = geohex.get_zone_by_code('XM48854457273')
print(zone.lat, zone.lon)
# (35.658618718910624, 139.74540917994662)
```

