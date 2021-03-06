from app.Director import Director
from app.bungiemanifest import DestinyManifest
from app.PgcrCollector import PGCRCollector
from app.Zipper import Zipper
from app.bungieapi import BungieApi
from app.reports.ActivityCountReport import ActivityCountReport
from app.reports.ActivityLocationTimeReport import ActivityLocationTimeReport
from app.reports.ActivityLocationWeaponReport import ActivityLocationWeaponReport
from app.reports.ActivityTypeRaceReport import ActivityTypeRaceReport
from app.reports.ActivityWinrateReport import ActivityWinrateReport
from app.reports.FireteamActivityReport import FireteamActivityReport
from app.reports.FireteamRace import FireteamRaceReport
from app.reports.KDReport import KDReport
from app.reports.KillsDeathsAssistsReport import KillsDeathsAssistsReport
from app.reports.LightLevelReport import LightLevelReport
from app.reports.PlaytimeCharacterReport import PlaytimeCharacterReport
from app.reports.PlaytimeReport import PlaytimeReport
from app.reports.WeaponKillTreeReport import WeaponKillTreeReport
from app.reports.WeaponRaceReport import WeaponRaceReport
from app.reports.WeaponReport import WeaponReport
from app.reports.WeekdayReport import WeekdayReport
# from app.DiscordSender import DiscordSender

if __name__ == '__main__':
    import pathos
    from pathos.multiprocessing import ProcessPool
    pathos.helpers.freeze_support()  # required for windows
    manifest = DestinyManifest().update()

    pool = ProcessPool(25)
    # You could also specify the amount of threads. Not that this DRASTICALLY speeds up the process, but takes serious computation power
    # pool = ProcessPool(60)

    MEMBERSHIP_MIJAGO = (3, 4611686018482684809)
    USED_MEMBERSHIP = MEMBERSHIP_MIJAGO

    api = BungieApi("API-KEY")
    VIDEO_TYPE = "gif" # you can also use "mp4" if you installed ffmpeg; see README.d

    Director.CreateDirectoriesForUser(*USED_MEMBERSHIP)
    Director.ClearResultDirectory(*USED_MEMBERSHIP)
    Director.CreateDirectoriesForUser(*USED_MEMBERSHIP)
    pc = PGCRCollector(*USED_MEMBERSHIP, api, pool)
    pc.getCharacters().getActivities(limit=None).getPGCRs(pagesize=1000)  # .combineAllPgcrs()
    data = pc.getAllPgcrs()

    pool.close()

    reports = [
        KDReport(*USED_MEMBERSHIP, manifest),
        KillsDeathsAssistsReport(*USED_MEMBERSHIP, manifest),
        WeaponReport(*USED_MEMBERSHIP, manifest),
        LightLevelReport(*USED_MEMBERSHIP, manifest),
        PlaytimeReport(*USED_MEMBERSHIP, manifest),
        PlaytimeCharacterReport(*USED_MEMBERSHIP, manifest),
        ActivityCountReport(*USED_MEMBERSHIP, manifest),
        WeekdayReport(*USED_MEMBERSHIP, manifest),
        ActivityLocationTimeReport(*USED_MEMBERSHIP, manifest),
        ActivityLocationWeaponReport(*USED_MEMBERSHIP, manifest),
        ActivityWinrateReport(*USED_MEMBERSHIP, manifest),
        WeaponKillTreeReport(*USED_MEMBERSHIP, manifest),
        FireteamRaceReport(*USED_MEMBERSHIP, manifest, video_type=VIDEO_TYPE),
        WeaponRaceReport(*USED_MEMBERSHIP, manifest, video_type=VIDEO_TYPE),
        ActivityTypeRaceReport(*USED_MEMBERSHIP, manifest, video_type=VIDEO_TYPE),
        FireteamActivityReport(*USED_MEMBERSHIP, manifest)
    ]
    for report in reports:
        report.generate(data).save()

    Zipper.zip_directory(Director.GetResultDirectory(*USED_MEMBERSHIP), Director.GetZipPath(*USED_MEMBERSHIP))
    print("Generated ZIP:", Director.GetZipPath(*USED_MEMBERSHIP))

    # DiscordSender.send(Director.GetZipPath(*USED_MEMBERSHIP), *USED_MEMBERSHIP)
    # print("Sent ZIP:", Director.GetZipPath(*USED_MEMBERSHIP))
