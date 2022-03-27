import json, urllib.request

from app.data.activities import ACTIVITY_NAMES

BUNGIE_BASE = "https://bungie.net/"
BUNGIE_API_BASE = "https://bungie.net/Platform/"


class DestinyManifest():
    def __init__(self):
        self.ActivityNames = None
        self.ActivityTypeNames = None
        self.ItemDefinitions = None

    def update(self):
        self.ActivityTypeNames = GetActivityTypeNames()
        self.ItemDefinitions = GetInventoryItemDefinitions()
        self.ActivityNames = GetActivityNames()

        return self


def GetManifestDefinitions(definition):
    print("Get %s" % definition)
    manifestPaths = json.loads(urllib.request.urlopen(BUNGIE_API_BASE + "/Destiny2/Manifest/").read())["Response"]
    manifestPath = manifestPaths["jsonWorldComponentContentPaths"]["en"][definition]
    print("Get %s from '%s'" % (definition, BUNGIE_BASE + manifestPath))
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
    return result


def GetActivityTypeNames():
    # data = GetManifestDefinitions("DestinyActivityTypeDefinition")
    #result = {str(data[k]["index"]): data[k]["displayProperties"]["name"] for k in data.keys() if "name" in data[k]["displayProperties"]}
    return ACTIVITY_NAMES
