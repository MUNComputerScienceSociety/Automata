from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="automata_", env_file=".env")

    token: str

    primary_guild: int = 514110851016556567
    verified_role: int = 564672793380388873
    general_channel: int = 514110851641376809
    executive_docs_channel: int = 773246740002373652
    diary_daily_channel: int = 872217138851614750
    newsline_channel: int = 811433377642446869
    announcement_channel: int = 752914074504790068
    aoc_leaderboard_channel: int = 909857762064871444
    whitelist_http_api_bearer_token: str | None = None
    mongo_host: str = "mongo"
    discord_auth_uri: str = "https://discord.muncompsci.ca"
    weather_api_key: str | None = None
    starboard_channel_id: int = 900883422187253870
    starboard_threshold: int = 5
    sentry_dsn: str | None = None
    member_intents_enabled: bool = True

    enabled_plugins: list[str] = []
    disabled_plugins: list[str] = []

    @property
    def mongo_address(self) -> str:
        return f"mongodb://{self.mongo_host}/automata"


config = Config()  # type: ignore - Pydantic and Pyright don't play nice, but Discord.py doesn't work with Mypy

__all__ = ["config"]
