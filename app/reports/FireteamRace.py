import pandas as pd

from app.Director import Director
from app.reports.ReportBase import Report
import bar_chart_race as bcr
from dateutil import parser


class FireteamRaceReport(Report):
    def save(self):
        super().save()

    def getName(self) -> str:
        return "[ALL] race - fireteam playtime"

    def __init__(self, membershipType, membershipId, video_type="gif") -> None:
        super().__init__(membershipType, membershipId)
        self.video_type = video_type

    def save(self):
        pass

    def generate(self, data) -> Report:
        df = self.generateData(data)

        bcr.bar_chart_race(
            df=df,
            filename=Director.GetResultDirectory(self.membershipType, self.membershipId) + "/" + self.getName() + "." + self.video_type,
            orientation='h',
            sort='desc',
            n_bars=20,
            fixed_order=False,
            fixed_max=True,
            steps_per_period=10,
            period_length=200,
            interpolate_period=False,
            perpendicular_bar_func='median',
            title='Top 20 Fireteam Members over Time, in Minutes',
            bar_size=.95,
            shared_fontdict=None,
            scale='linear',
            fig=None,
            writer=None,
            bar_kwargs={'alpha': .7},
            filter_column_colors=False
        )

        return self

    def generateData(self, datap):
        eps = []
        displayNames = dict()
        displayNameTimes = dict()

        for data in datap:
            if "entries" not in data: continue
            # find own user entry
            entry = [e for e in data["entries"] if e["player"]["destinyUserInfo"]["membershipId"] == str(self.membershipId)][0]
            fireteamId = entry["values"]["fireteamId"]["basic"]["value"]
            date = parser.parse(data["period"])

            res = [
                (
                    # datetime.strptime(data["period"]), # 2022-03-08T14:59:02Z
                    date,

                    e["player"]["destinyUserInfo"]["membershipId"],
                    # (e["player"]["destinyUserInfo"]["membershipType"],            e["player"]["destinyUserInfo"]["membershipId"]),
                    e["values"]["timePlayedSeconds"]["basic"]["value"] / 60
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
                    displayNames[name[0]] = name[1]
                    displayNameTimes[name[0]] = date

            eps += res

        df = pd.DataFrame(eps, columns=["date", "name", "minutes"])
        df2 = df.groupby([df.date.dt.to_period('W'), "name"]).sum().reset_index()
        df2["cumsum"] = df2.groupby(["name"]).cumsum()
        df3 = df2.pivot(index="date", columns="name", values="cumsum")

        df3 = df3.fillna(method='ffill')
        df3 = df3.rename(columns=displayNames)
        return df3