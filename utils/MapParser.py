from yandex_geocoder import Client as YaMap

from data.config import MAP_TOKEN

yaMap = YaMap(api_key=MAP_TOKEN)


def getCoordsByAddress(address: str) -> tuple:
    lon, lat = yaMap.coordinates(address)
    # print(lon, lat)
    return (float(lat), float(lon))


def getAddressByCoords(lat: float, lon: float) -> str:
    return yaMap.address(latitude=lat, longitude=lon)

# print(getAddressByCoords(lat=59.993536, lon=30.357344))
