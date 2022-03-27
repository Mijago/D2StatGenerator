import dateutil.parser
import pandas as pd
from app.Director import Director
from app.reports.ReportBase import Report


class FireteamActivityReport(Report):

    def save(self):
        with open("%s/%s.csv" % (Director.GetResultDirectory(self.membershipType, self.membershipId), "[ALL] table - fireteam member activities"), "w", encoding='utf-8') as f:
            self.df.to_csv(f, index=False, line_terminator='\n')
        print("Report> Generated %s" % self.getName())

    def getName(self) -> str:
        return "[ALL] table - fireteam member activities"

    def __init__(self, membershipType, membershipId, manifest) -> None:
        super().__init__(membershipType, membershipId, manifest)
        self.df = None

    def generate(self, data) -> Report:
        self.df = self.generateListDataframe(data)
        return self

    def generateListDataframe(self, datap):
        eps = []
        displayNames = dict()
        displayNameTimes = dict()
        for data in datap:
            if "entries" not in data: continue
            # find own user entry
            entry = [e for e in data["entries"] if e["player"]["destinyUserInfo"]["membershipId"] == str(self.membershipId)][0]
            fireteamId = entry["values"]["fireteamId"]["basic"]["value"]
            date = dateutil.parser.parse(data["period"])

            res = [
                (
                    e["player"]["destinyUserInfo"]["membershipId"],
                    e["player"]["destinyUserInfo"]["membershipId"],
                    date,
                    self.manifest.ActivityTypeNames[data["activityDetails"]["mode"]],
                    entry["values"]["activityDurationSeconds"]["basic"]["value"] / 60
                )
                for e in data["entries"]
                if e["values"]["fireteamId"]["basic"]["value"] == fireteamId
                   and e["player"]["destinyUserInfo"]["membershipId"] != str(self.membershipId)]

            # update names
            names = [(e["player"]["destinyUserInfo"]["membershipId"],
                      e["player"]["destinyUserInfo"]["displayName"]
                      if "displayName" in e["player"]["destinyUserInfo"] else "UNKNOWN"
                      )
                     for e in data["entries"]
                     if e["values"]["fireteamId"]["basic"]["value"] == fireteamId
                     and e["player"]["destinyUserInfo"]["membershipId"] != str(self.membershipId)
                     ]
            for name in names:
                if name[0] not in displayNameTimes or displayNameTimes[name[0]] < date:
                    displayNames[name[0]] = name[1].replace("$", "S")
                    displayNameTimes[name[0]] = date

            eps += res

        eps = [[
            e[0], displayNames[e[1]], e[2], e[3], e[4]
        ] for e in eps]

        df = pd.DataFrame(eps, columns=["membershipId", "name", "date", "activity", "minutes"])
        df = df.sort_values(["name", "date"])

        return df
