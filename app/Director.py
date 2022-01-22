import shutil
from pathlib import Path


class Director:

    @staticmethod
    def ClearResultDirectory(membershipType, membershipId):
        path = Director.GetResultDirectory(membershipType, membershipId)
        shutil.rmtree(path)

    @staticmethod
    def GetZipPath(membershipType, membershipId):
        return "./data/%d_%d/charts_%d_%d.zip" % (membershipType, membershipId, membershipType, membershipId)

    @staticmethod
    def GetResultDirectory(membershipType, membershipId):
        return "./data/%d_%d/result/" % (membershipType, membershipId)

    @staticmethod
    def GetPGCRDirectory(membershipType, membershipId):
        return "./data/%d_%d/pgcr/" % (membershipType, membershipId)

    @staticmethod
    def GetAllPgcrFilename(membershipType, membershipId):
        return "./data/%d_%d/pgcr.json" % (membershipType, membershipId)

    @staticmethod
    def CreateDirectoriesForUser(membershipType, membershipId):
        Path(Director.GetResultDirectory(membershipType, membershipId)).mkdir(parents=True, exist_ok=True)
        Path(Director.GetPGCRDirectory(membershipType, membershipId)).mkdir(parents=True, exist_ok=True)
