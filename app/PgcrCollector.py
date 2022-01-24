import os

from app.Director import Director
from app.bungieapi import BungieApi
import json

from app.internal_timer import Timer


class PGCRCollector:
    def __init__(self, membershipType, membershipId, api: BungieApi, pool) -> None:
        super().__init__()
        self.processPool = pool
        self.membershipType = membershipType
        self.membershipId = membershipId
        self.api = api
        self.characters = None
        self.activities = None

    def getCharacters(self):
        print("> Get Characters")
        account_stats = self.api.getAccountStats(self.membershipType, self.membershipId)
        self.characters = [c["characterId"] for c in account_stats["characters"]]
        print("Found characters: ", len(self.characters))
        return self

    def getActivities(self, limit=None):
        print("> Get Activities")
        assert self.characters is not None
        assert len(self.characters) > 0

        existingPgcrList = [f[5:-5] for f in os.listdir(Director.GetPGCRDirectory(self.membershipType, self.membershipId))]

        self.activities = []
        for k, char_id in enumerate(self.characters):
            page = 0

            def downloadActivityPage(page):
                act = self.api.getActivities(self.membershipType, self.membershipId, char_id, page=page)
                if "activities" not in act:
                    return None
                return [e["activityDetails"]["instanceId"] for e in act["activities"] if e["activityDetails"]["instanceId"] not in existingPgcrList]

            while True:
                steps = 20
                print(k + 1, "/", len(self.characters), "|", char_id, "|", "pages", page + 1, "to", page + steps)
                activityGroups = self.processPool.amap(downloadActivityPage, range(page, page + steps)).get()
                realList = [e for e in activityGroups if e is not None]
                hasNull = len(realList) != steps
                for activityList in realList:
                    self.activities += activityList

                page += steps
                if hasNull:
                    break

                if limit is not None:
                    if len(self.activities) > limit:
                        break

            if limit is not None:
                if len(self.activities) > limit:
                    break
        print("Got ", len(self.activities), " activities that must be downloaded.")

        return self

    def getPGCRs(self, pagesize=1000):
        bungo = self.api

        def downloadPGCR(activity):
            id = activity

            pgcr = bungo.getPGCR(id)
            with open("%s/pgcr_%s.json" % (Director.GetPGCRDirectory(self.membershipType, self.membershipId), pgcr["activityDetails"]["instanceId"]), "w") as f:
                f.write(json.dumps(pgcr))

        stepsize = pagesize
        START_PAGE = 0

        if len(self.activities) == 0:
            print("No activities to grab")
            return self

        for steps in range(START_PAGE, (len(self.activities) + stepsize - 1) // stepsize):
            try:
                with Timer("Get PGCRs %d through %d" % (steps * stepsize + 1, min(len(self.activities), (steps + 1) * stepsize))):
                    # self.processPool.restart(True)
                     self.processPool.amap(downloadPGCR, self.activities[steps * stepsize:(steps + 1) * stepsize]).get()
            except Exception as e:
                print(e)
        return self

    def combineAllPgcrs(self):
        all = self.getAllPgcrs()
        with Timer("Write all PGCRs to one file"):
            with open(Director.GetAllPgcrFilename(self.membershipType, self.membershipId), "w", encoding='utf-8') as f:
                json.dump(all, f, ensure_ascii=False)
        return self

    def getAllPgcrs(self):

        def loadJson(fname):
            with open(fname, "r") as f:
                return json.load(f)

        with Timer("Get all PGCRs from individual files"):
            root = Director.GetPGCRDirectory(self.membershipType, self.membershipId)
            fileList = ["%s/%s" % (root, f) for f in os.listdir(root)]
            pgcrs = self.processPool.amap(loadJson, fileList).get()
            all = pgcrs
        return all
