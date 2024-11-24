from typing import Any

import motor.motor_asyncio

from automata.config import config

mongo = motor.motor_asyncio.AsyncIOMotorClient[Any](config.mongo_address)

__all__ = ["mongo"]
