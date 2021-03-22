# MyClassScrape
Discord bot to scrape class schedule using [discord.py](https://github.com/Rapptz/discord.py) library with
[MongoDB](https://cloud.mongodb.com/) database.

Feel free to [invite me](https://discord.com/api/oauth2/authorize?client_id=775903023821881374&permissions=522304&scope=bot) to your server.

You can invite me at http://mrmiss.wtf/MyClassScrape.

If you are interested to contribute feel free to send a `pull request` or get in [touch](https://discordapp.com/users/789424141778288670) with me. 

# Setup
To setup this Bot you just need to set the configuration first with the `config.env` file.
This file should be placed on the root folder of this bot. This is where the bot token an others
variables are loaded. It's recomended to import from `sample_config.env` to ensure the bot contains all default
variables

An example `config.env` file could be:

```dosini
BOT_TOKEN = ""  # Your Bot token
BOT_PREFIX = "!"  # A handler that bot react with
DATABASE_URL = "mongodb+srv://username:password@host.port.mongodb.net/db_name"
KEY = "AbcDeFGhiJkl="  # Fernet key to encrypt
```

## Dependencies
Install the necessary Python dependencies by moving to the project directory and running:

`pip3 install -r requirements.txt`.

This will install all the necessary python packages.

## Starting the bot
Once you've set up your database and your configuration is complete, simply run:

`python3 -m bot`

# License
This work is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)

You may copy, distribute and modify the software under the terms of the GNU General Public License.