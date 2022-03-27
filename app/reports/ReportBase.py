from app.Director import Director
import abc

from app.bungiemanifest import DestinyManifest


class Report:

    def __init__(self, membershipType, membershipId, manifest: DestinyManifest) -> None:
        super().__init__()
        self.membershipType = membershipType
        self.membershipId = membershipId
        self.manifest = manifest
        self.fig = None

    @abc.abstractmethod
    def generate(self, data):
        pass

    @abc.abstractmethod
    def getName(self) -> str:
        return "unnamed"

    def save(self):
        assert self.fig is not None
        filename = '%s/%s.html' % (Director.GetResultDirectory(self.membershipType, self.membershipId), self.getName())
        with open(filename, "w") as f:
            f.write(self.fig.to_html(full_html=False, include_plotlyjs='cdn'))

        print("Report> Generated %s" % self.getName())
