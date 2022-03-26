import json, urllib.request

BUNGIE_BASE = "https://bungie.net/"
BUNGIE_API_BASE = "https://bungie.net/Platform/"


def GetManifestDefinitions(definition):
    print("Get %s" % definition)
    manifestPaths = json.loads(urllib.request.urlopen(BUNGIE_API_BASE + "/Destiny2/Manifest/").read())["Response"]
    manifestPath = manifestPaths["jsonWorldComponentContentPaths"]["en"][definition]
    InventoryItemDefinitions = urllib.request.urlopen(BUNGIE_BASE + manifestPath).read()
    print("Unpack and parse %s" % definition)

    InventoryItemDefinitions = json.loads(InventoryItemDefinitions)
    print("Json'd %s" % definition)
    return InventoryItemDefinitions


def GetInventoryItemDefinitions():
    return GetManifestDefinitions("DestinyInventoryItemDefinition")


def GetActivityNames():
    data = GetManifestDefinitions("DestinyActivityDefinition")

    result = {str(data[k]["hash"]): data[k]["displayProperties"]["name"] for k in data.keys()}
    print(result)
    return result
