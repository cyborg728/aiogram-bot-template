# aiogram-bot-template

**DO NOT TOUCH** the `template` folder.

Some presets are configurable in `bot/__init__.py` file

<!-- TODO: write that presets -->

create custom role in bot.constants.role

create custom models in bot.models. Every model with table=true will create automatically

import rules:

bot.template: relative imports

bot: absolute imports

use relative import inside module

versions: x.y.z
x - can have breaking changes
y - files in /bot/ folder can be modified
z -  files in /bot/template/ folder can be modified

locales in /bot/locales/$LOCALE/messages.ftl

* HOW TO INIT PROJECT *

1) Rename project in "/pyproject.toml"
2) Install dependencies. "poetry install"
- "poetry update --with redis"
- "poetry update --with redis"