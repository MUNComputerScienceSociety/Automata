# **Automata**

![Deploy to GHCR](https://github.com/MUNComputerScienceSociety/Automata/workflows/Deploy%20to%20GHCR/badge.svg)
[![Code scanning - action](https://github.com/MUNComputerScienceSociety/Automata/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/MUNComputerScienceSociety/Automata/actions/workflows/codeql-analysis.yml)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Discord bot handling the management of the [MUN Computer Science Society](https://muncompsci.ca/) Discord server

For feature requests / help getting the bot running, don't fret to ask questions in the `#automata` channel in the guild!

---

## Running locally

1. Clone the project by running `https://github.com/MUNComputerScienceSociety/Automata.git`, and change into the directory by running `cd ./Automata`
2. Copy `.env.dist` to `.env`
3. Fill out the required information in the `.env`

   - At the moment, the required environment variables are:

     - `AUTOMATA_TOKEN`: A Discord token, which you can see how to get [here](https://discordpy.readthedocs.io/en/latest/discord.html)
     - `AUTOMATA_PRIMARY_GUILD`: The ID of the Discord server you will be testing in. You can find this by following the instructions [here](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID).
     - `AUTOMATA_EXECUTIVE_DOCS_CHANNEL`: The ID of the channel to post executive docs notifications to. This can be any channel in your primary guild, with the warning that it'll be a bit noisy on first start. You can find this by following the instructions [here](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID).

> [!NOTE]
> Note about running locally and avoiding spam:
>
> When this bot was smaller, it wasn't so bad to run all the plugins; but since we have 10+, and some of them do some data fetching / loading on startup, the logs can get a bit loud.
>
> If you're working on a plugin, you can add its name to the `AUTOMATA_ENABLED_PLUGINS` env. var (like `AUTOMATA_ENABLED_PLUGINS=["PluginName"]`), and it will be the _only_ plugin that will be loaded.
>
> This env. var is a JSON-encoded list, so you can enable multiple plugins at once.

Once done, follow the instructions under either of the headings below, depending on how you wish to run the bot.

### With Docker

Start the containers by running `docker-compose up -d`

### Without Docker

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and Python 3.12 or above.
2. Run MongoDB

   - You can use Docker for running MongoDB (recommended), by starting only the `mongo` container with `docker-compose up -d mongo`
   - Alternatively, you can install Mongo via whatever means is recommended for your OS

3. Install the dependencies with `uv sync`
4. Run the bot using `uv run python -m automata`

---

## Developing your own plugins

Features are provided to the bot via plugins - if you wish to add your own functionality, you should build your own plugin. To do so:

1. Create a new file in `automata/plugins` for your plugin
2. Add to your file the code for your plugin
   - This plugin will be a [discord.py cog](https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html) - you can refer to their docs for examples of the things you can do and how to do them
   - You can use `lmgtfy.py` as a simple example
3. In `automata/plugins/__init__.py`, import your plugin and add it to the `all_plugins` list
   - Once again, you can copy this from the `lmgtfy.py` example

Once done, you can run your plugin locally by following the instructions under [Running your changes locally](#running-your-changes-locally).

---

## Running your changes locally

### Using Docker

1. Edit the `docker-compose.yml`, replacing the `image: ghcr.io/muncomputersciencesociety/automata` line for the automata container with `build: .`
2. Edit the bot core or the plugins as you wish
3. Start the container, forcing a rebuild of the image using `docker-compose up -d --build`

### Without Docker

If you do not want to run the bot in Docker, you can just start the bot using the instructions from [Running locally](#running-locally) - no special steps required.

---

## Pushing changes to GitHub

1. Fork this repository, clone your fork, and commit your changes to a branch on your fork
2. Create a PR to merge your branch into the `master` branch here, and make sure to tag an executive / mention the PR in Discord so we see it
3. We'll likely request some changes before it is merged
4. Once it's good, a few minutes after the PR is merged the feature should be live, since Automata uses CI/CD :)

---

## Container responsibilities

Automata is comprised of a number of containers, each with distinct responsibilities. Their responsibilities are as follows:

| Container | Responsibilities                                                                     |
| --------- | ------------------------------------------------------------------------------------ |
| automata  | The Discord bot itself                                                               |
| mongo     | A MongoDB server used to provide persistent data storage to the `automata` container |
