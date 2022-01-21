from app.Director import Director
from app.InventoryItem import GetInventoryItemDefinitions
from app.PgcrCollector import PGCRCollector
from app.bungieapi import BungieApi
from app.reports.KDReport import KDReport
from app.reports.LightLevelReport import LightLevelReport
from app.reports.PlaytimeReport import PlaytimeReport
from app.reports.WeaponReport import WeaponReport

if __name__ == '__main__':
    from pathos.multiprocessing import ProcessPool

    pool = ProcessPool(nodes=40)

    MEMBERSHIP_MIJAGO = (3, 4611686018482684809)
    USED_MEMBERSHIP = MEMBERSHIP_MIJAGO

    api = BungieApi("API-KEY")

    Director.CreateDirectoriesForUser(*USED_MEMBERSHIP)
    pc = PGCRCollector(*USED_MEMBERSHIP, api, pool)
    pc.getCharacters().getActivities(limit=None).getPGCRs()#.combineAllPgcrs()
    data = pc.getAllPgcrs()

    inventoryItemDefs = GetInventoryItemDefinitions()

    KDReport(*USED_MEMBERSHIP).generate(data).save()
    WeaponReport(*USED_MEMBERSHIP, inventoryItemDefs).generate(data).save()
    LightLevelReport(*USED_MEMBERSHIP).generate(data).save()
    PlaytimeReport(*USED_MEMBERSHIP).generate(data).save()

