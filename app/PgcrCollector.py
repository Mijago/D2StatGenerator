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
        for char_id in self.characters:
            page = 0
            while True:
                print(char_id, "page", page)
                act = self.api.getActivities(self.membershipType, self.membershipId, char_id, page=page)
                if "activities" not in act:
                    break
                page += 1
                self.activities += [e["activityDetails"]["instanceId"] for e in act["activities"] if e["activityDetails"]["instanceId"] not in existingPgcrList]
                if limit is not None:
                    if len(self.activities) > limit:
                        return self
        print("Got ",len(self.activities), " activities that must be downloaded.")

        return self

    def getPGCRs(self):
        bungo = self.api

        def downloadPGCR(activity):
            id = activity
            return bungo.getPGCR(id)

        stepsize = 1000
        START_PAGE = 0
        for steps in range(START_PAGE, (len(self.activities) + stepsize - 1) // stepsize):
            try:
                with Timer("get pgcrs for step %d" % steps):
                    self.processPool.restart(True)
                    pgcrs = self.processPool.amap(downloadPGCR, self.activities[steps * stepsize:(steps + 1) * stepsize]).get()
                    for pgcr in pgcrs:
                        with open("%s/pgcr_%s.json" % (Director.GetPGCRDirectory(self.membershipType, self.membershipId), pgcr["activityDetails"]["instanceId"]), "w") as f:
                            f.write(json.dumps(pgcr))
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
        all = []
        with Timer("Get all PGCRs from individual files"):
            for fname in os.listdir(Director.GetPGCRDirectory(self.membershipType, self.membershipId)):
                with open(Director.GetPGCRDirectory(self.membershipType, self.membershipId) + "/" + fname, "r") as f:
                    all.append(json.load(f))
        return all
