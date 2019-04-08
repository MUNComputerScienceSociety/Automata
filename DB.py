import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient(
    f"mongodb://mongo/automata"
)
