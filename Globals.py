import os

import motor.motor_asyncio
import sentry_sdk

mongo_client = motor.motor_asyncio.AsyncIOMotorClient(
    f"mongodb://mongo/automata"
)

sentry_sdk.init(os.environ["SENTRY_DSN"])
