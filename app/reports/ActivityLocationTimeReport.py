import dateutil.parser
from datetime import datetime
import pandas as pd

from app.Director import Director
from app.data.activities import ACTIVITY_NAMES
from app.data.directorActivityNames import DIRECTOR_ACTIVITY_NAMES
from app.reports.ReportBase import Report
import plotly.express as px
import plotly as pl


class ActivityLocationTimeReport(Report):

    def save(self):
        pl.offline.plot(self.fig_sunburst, auto_open=False, filename='%s/%s_sunburst.html' % (Director.GetResultDirectory(self.membershipType, self.membershipId), self.getName()))
        pl.offline.plot(self.fig_treemap, auto_open=False, filename='%s/%s_treemap.html' % (Director.GetResultDirectory(self.membershipType, self.membershipId), self.getName()))

    def getName(self) -> str:
        return "chart_all_activity_location"

    def __init__(self, membershipType, membershipId) -> None:
        super().__init__(membershipType, membershipId)
        self.fig_sunburst = None
        self.fig_treemap = None

    def generate(self, data) -> Report:
        df = self.generateData(data)
        fig = px.sunburst(df, path=["category", "activity", "directorActivityHash"], values='playtime', template="plotly_dark",
                          branchvalues="total", labels=["playtime"])
        fig.update_traces(texttemplate=('%{label}<br>%{value:.2f}h (%{percentParent:.1%})'))
        self.fig_sunburst = fig

        fig = px.treemap(df, path=[px.Constant("all"), "category", "activity", "directorActivityHash"], values='playtime', template="plotly_dark",
                         branchvalues="total", labels=["playtime"])
        fig.update_traces(texttemplate=('%{label}<br>%{value:.2f}h (%{percentParent:.1%})'))
        self.fig_treemap = fig

        return self

    def generateData(self, data):

        category = []
        playtime = []
        activity = []
        subtype = []
        directorActivity = []

        for datapoint in data:
            if "entries" not in datapoint: continue
            timestamp = dateutil.parser.parse(datapoint["period"]).timestamp()
            for entry in datapoint["entries"]:
                if entry["player"]["destinyUserInfo"]["membershipId"] != str(self.membershipId): continue

                starts = entry["values"]["startSeconds"]["basic"]["value"]
                ends = starts + entry["values"]["timePlayedSeconds"]["basic"]["value"]

                start_date = datetime.fromtimestamp(timestamp + starts)

                typus = "PvE"
                if datapoint["activityDetails"]["mode"] in [84, 81, 80, 74, 73, 72, 71, 68, 65, 62, 61, 60, 59, 50, 48, 43, 45, 44, 41, 42, 37, 38, 31, 25, 15]:
                    typus = "PvP"
                elif datapoint["activityDetails"]["mode"] in [75, 63]:
                    typus = "Gambit"
                category.append(typus)
                activity.append(ACTIVITY_NAMES[datapoint["activityDetails"]["mode"]])
                key = str(datapoint["activityDetails"]["directorActivityHash"])
                key2 = str(datapoint["activityDetails"]["referenceId"])
                if key2 in DIRECTOR_ACTIVITY_NAMES:
                    directorActivity.append(DIRECTOR_ACTIVITY_NAMES[key2])
                elif key in DIRECTOR_ACTIVITY_NAMES:
                    directorActivity.append(DIRECTOR_ACTIVITY_NAMES[key])
                else:
                    directorActivity.append(key)
                playtime.append(entry["values"]["timePlayedSeconds"]["basic"]["value"] / 60 / 60)

        df = pd.DataFrame({
            "category": category,
            "activity": activity,
            "directorActivityHash": directorActivity,
            "playtime": playtime,
        })
        return df
