 #!/bin/bash  
APP_NAME="saucebot"
MAIN_FILE_PATH=saucebot/bot.py
SITE_PACKAGES_PATH=.venv/Lib/site-packages
COGS_DIR="./cogs;./cogs"
ICON_PATH="./res/icon.ico"

py -3 -m PyInstaller --onedir --noconsole \
--icon $ICON_PATH \
--paths $SITE_PACKAGES_PATH \
--add-data=$COGS_DIR \
--hidden-import="saucenao_api" \
-n $APP_NAME \
$MAIN_FILE_PATH

# Create empty .env file
ENV_FILE="./dist/saucebot/.env"
touch $ENV_FILE
echo "DISCORD_TOKEN=" >> $ENV_FILE
echo "NAO_KEY=" >> $ENV_FILE

$SHELL 
