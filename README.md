# **Automata**

![Deploy to Docker Hub](https://github.com/MUNComputerScienceSociety/Automata/workflows/Deploy%20to%20Docker%20Hub/badge.svg)
[![Build Size](https://images.microbadger.com/badges/image/muncs/automata.svg)](https://microbadger.com/images/muncs/automata)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

Discord bot handling the management of the MUN Computer Science Society Discord server

For feature requests / help getting the bot running, don't fret to ask questions in the `#automata` channel in the guild!

---

## **Running locally**

1. Clone the project by running `https://github.com/MUNComputerScienceSociety/Automata.git`, and change into the directory by running `cd ./Automata`
2. Copy `.env.dist` to `.env`
3. Fill out the required information in the `.env`
   - At the moment, the only required environment variable required is `AUTOMATA_TOKEN`, which is a Discord token, which you can see how to get [here](https://discordpy.readthedocs.io/en/latest/discord.html)

> Note about running locally and avoiding spam:
>
> When this bot was smaller, it wasn't so bad to run all the plugins; but since we have 40+, and some of them do some data fetching / loading on startup, so the logs can get a bit loud.
>
> If you're working on a plugin, you can add its name to the `AUTOMATA_ENABLED_PLUGINS` env. var (like AUTOMATA_ENABLED_PLUGINS=PluginName), and it will be the _only_ plugin that will be loaded.
>
> This is a comma-delimited list as well, so you can enable multiple plugins at once.

### Using Docker

1. Create the directory `mounted_plugins` within the project by running `mkdir ./mounted_plugins`
2. Start the containers by running `docker-compose up -d`

### Without Docker

1. Run MongoDB

   > You can use Docker for running MongoDB (recommended), just add the following to the `docker-compose.yml` file to expose it to your local machine
   >
   > ```yml
   >   ...
   >   mongo:
   >     ...
   >     ports:
   >       - "127.0.0.1:27017:27017"
   >   ...
   > ```
   >
   > And start it _only_ by running `docker-compose up -d mongo`

2. Install the requirements found in the `requirements.txt` file using `pip install -r requirements.txt`

   - Using a virtual environment is highly recommended, [this section of the Flask documentation explains this well](https://flask.palletsprojects.com/en/1.1.x/installation/#virtual-environments).

3. Run the bot using `python Bot.py`

---

## **Developing your own plugins**

- Automata is built around the [discord.py](https://discordpy.readthedocs.io/en/latest/) framework, therefore the plugins make heavy use of its decorators to abstract most of the complexity behind the scenes.

### Using Docker

1. Create the folder `mounted_plugins` if it doesn't already exist
   - `plugins` is baked into the image when it is built, so editing files there won't have an effect
2. Create a new plugin within the `mounted_plugins` folder
   1. Create a new [Jigsaw plugin manifest](https://jigsaw.readthedocs.io/en/latest/plugin.json.html)
      - You can use `plugins/Ping/plugin.json` as an example
   2. Create a new plugin
      - You can use `plugins/Ping/__init__.py` as an example
3. Start the bot using the instructions from [Running locally](#running-locally)

When you make changes to your plugins, restart the Automata container using `docker-compose restart automata`

### Without Docker

1. Create a new plugin, following the directions above within 'Using Docker', but within the `plugins` folder instead
2. Start the bot using the instructions from [Running locally](#running-locally)

---

## **Developing the bot core and built-in plugins**

### Using Docker

1. Edit the `docker-compose.yml`, replacing the `image: muncs/automata` line for the automata container with `build: .`
2. Edit the bot core or the plugins as you wish
3. Start the container, forcing a rebuild of the image using `docker-compose up -d --build`

### Without Docker

1. Just edit the core files / plugins directly :)
2. Start the bot using the instructions from [Running locally](#running-locally)

---

## **Pushing changes to GitHub**

1. Fork this repository, clone your fork, and commit your changes to a branch on your fork
2. Create a PR to merge your branch into the `master` branch here, and make sure to tag an executive / mention the PR in Discord so we see it
3. We'll likely request some changes before it is merged
4. Once it's good, a few minutes after the PR is merged the feature should be live, since Automata uses CI/CD :)

---

## **Container responsibilities**

Automata is comprised of a number of containers, each with distinct responsibilities. Their responsibilities are as follows:

| Container | Responsibilities |
| --- | --- |
| automata | The Discord bot itself |
| mongo | A MongoDB server used to provide persistent data storage to the `automata` container |
