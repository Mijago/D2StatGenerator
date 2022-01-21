import json, urllib.request

BUNGIE_BASE = "https://bungie.net/"
BUNGIE_API_BASE = "https://bungie.net/Platform/"


def GetInventoryItemDefinitions():
    print("Get InventoryItemDefinitions")
    manifestPaths = json.loads(urllib.request.urlopen(BUNGIE_API_BASE + "/Destiny2/Manifest/").read())["Response"]
    manifestPath = manifestPaths["jsonWorldComponentContentPaths"]["en"]["DestinyInventoryItemDefinition"]
    InventoryItemDefinitions = urllib.request.urlopen(BUNGIE_BASE + manifestPath).read()
    print("Unpack and parse InventoryItemDefinitions")

    InventoryItemDefinitions = json.loads(InventoryItemDefinitions)
    print("Json'd InventoryItemDefinitions")

    return InventoryItemDefinitions
