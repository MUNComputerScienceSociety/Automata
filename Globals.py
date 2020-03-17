import os

import motor.motor_asyncio
import sentry_sdk

PRIMARY_GUILD = os.getenv("AUTOMATA_PRIMARY_GUILD", 514110851016556567)
VERIFIED_ROLE = os.getenv("AUTOMATA_VERIFIED_ROLE", 564672793380388873)

mongo_client = motor.motor_asyncio.AsyncIOMotorClient(f"mongodb://mongo/automata")

if os.getenv("SENTRY_DSN", None):
    sentry_sdk.init(os.environ["SENTRY_DSN"])
