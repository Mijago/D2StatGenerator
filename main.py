from app.Director import Director
from app.InventoryItem import GetInventoryItemDefinitions
from app.PgcrCollector import PGCRCollector
from app.Zipper import Zipper
from app.bungieapi import BungieApi
from app.reports.ActivityLocationTimeReport import ActivityLocationTimeReport
from app.reports.KDReport import KDReport
from app.reports.KillsDeathsAssistsReport import KillsDeathsAssistsReport
from app.reports.LightLevelReport import LightLevelReport
from app.reports.PlaytimeReport import PlaytimeReport
from app.reports.WeaponReport import WeaponReport
from app.reports.WeekdayReport import WeekdayReport

if __name__ == '__main__':
    import pathos
    from pathos.multiprocessing import ProcessPool

    pathos.helpers.freeze_support()
    pool = ProcessPool(15)

    MEMBERSHIP_MIJAGO = (3, 4611686018482684809)
    USED_MEMBERSHIP = MEMBERSHIP_MIJAGO

    api = BungieApi("API-KEY")

    Director.CreateDirectoriesForUser(*USED_MEMBERSHIP)
    Director.ClearResultDirectory(*USED_MEMBERSHIP)
    Director.CreateDirectoriesForUser(*USED_MEMBERSHIP)
    pc = PGCRCollector(*USED_MEMBERSHIP, api, pool)
    pc.getCharacters().getActivities(limit=None).getPGCRs(pagesize=1000)  # .combineAllPgcrs()
    data = pc.getAllPgcrs()

    inventoryItemDefs = GetInventoryItemDefinitions()

    KDReport(*USED_MEMBERSHIP).generate(data).save()
    KillsDeathsAssistsReport(*USED_MEMBERSHIP).generate(data).save()
    WeaponReport(*USED_MEMBERSHIP, inventoryItemDefs).generate(data).save()
    LightLevelReport(*USED_MEMBERSHIP).generate(data).save()
    PlaytimeReport(*USED_MEMBERSHIP).generate(data).save()
    WeekdayReport(*USED_MEMBERSHIP).generate(data).save()
    ActivityLocationTimeReport(*USED_MEMBERSHIP).generate(data).save()

    Zipper.zip_directory(Director.GetResultDirectory(*USED_MEMBERSHIP), Director.GetZipPath(*USED_MEMBERSHIP))
    print("Generated ZIP:", Director.GetZipPath(*USED_MEMBERSHIP))
