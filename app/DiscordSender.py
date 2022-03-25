import os

import discord

from app.Director import Director


class DiscordSender:
    @staticmethod
    def send(zipPath, membershipType, membershipId):
        # DISCORD WEBHOOK
        webhook = discord.Webhook.partial(935137211285802, 'q64vyCdgFKCdq5pdhfoU95UEKD7vwolUSAb7SKFJyX5iP3pHWJ5G964fp7s3xDlRb', adapter=discord.RequestsWebhookAdapter())  # Your webhook

        with open(zipPath, "rb") as f:
            zipFile = discord.File(f, filename="Report_%d_%d.zip" % (membershipType, membershipId))

            webhook.send("Report for %d_%d" % (membershipType, membershipId), username="Mijago's PgcrReport Generator", file=zipFile)
