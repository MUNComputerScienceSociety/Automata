from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="automata_", env_file=".env")

    discord_auth_uri: str = "https://discord.muncompsci.ca"
    executive_docs_channel: int = 773246740002373652
    member_intents_enabled: bool = True
    mongo_host: str = "localhost"
    primary_guild: int = 514110851016556567
    sentry_dsn: str | None = None
    starboard_channel_id: int = 900883422187253870
    starboard_threshold: int = 5
    token: str
    verified_role: int = 564672793380388873

    enabled_plugins: list[str] = []
    disabled_plugins: list[str] = []

    @property
    def mongo_address(self) -> str:
        return f"mongodb://{self.mongo_host}/automata"

    def should_enable_plugin(self, plugin: type) -> bool:
        if self.enabled_plugins:
            return plugin.__name__ in self.enabled_plugins
        return plugin.__name__ not in self.disabled_plugins


config = Config()  # type: ignore - Pydantic and Pyright don't play nice, but Discord.py doesn't work with Mypy

__all__ = ["config"]
