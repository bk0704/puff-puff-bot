# bot.py
import os
import discord
from discord.ext import commands
from discord import app_commands
import requests
import random
import httpx
from dotenv import load_dotenv

load_dotenv()
#load the token and guild from the .env file
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CAT_API = os.getenv('CAT_API_URL')
DOG_API = os.getenv('DOG_API_URL')
NASA_API = os.getenv('NASA_API_KEY')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

@client.event
async def on_ready():
    # This event is called when the bot has successfully connected to Discord
    # and is ready to start receiving events. This is a good place to perform
    # any setup or synchronization tasks.

    # Sync the command tree to the Discord guild (server) specified by the GUILD ID.
    # This makes sure that all the commands registered using the tree.command decorator
    # are updated in the guild and available to use as slash commands.
    await tree.sync(guild=discord.Object(id=GUILD))

    # Log a message to the console including the bot's user name to indicate
    # that the bot is logged in and on_ready event has been triggered.
    print(f'We have logged in as {client.user}')

    # Define an activity status for the bot to display. In this case, it's set to
    # a game with the name "I'm fucking vaping and smoking". Type 1 refers to a
    # 'Game' activity type.
    activity = discord.Game(name="I'm fucking vaping and smoking", type=1)

    # Change the bot's presence status to 'do not disturb' and set the activity
    # to the one defined above. This will show up in Discord as the bot's current
    # status and activity, letting users know what the bot is 'doing'.
    await client.change_presence(status=discord.Status.do_not_disturb, activity=activity)

@tree.command(name="hello", description="test the bot slash commands")
@app_commands.checks.cooldown(1, 10)  # Set a cooldown of 60 seconds on the command to prevent spam.
# This is a test command to check that the slash command functionality is working properly.
async def slash_command(interaction: discord.Interaction):
    # This asynchronous function is called when a user invokes the /hello slash command.
    
    # The function takes one argument, 'interaction', which is an instance of discord.Interaction.
    # This object contains data about the interaction, including the user who invoked the command.
    
    # Respond to the interaction by sending a message back to the channel where the command was used.
    # The message "sup bro you're all good to go!" is sent as the response to the user.
    await interaction.response.send_message("sup bro you're all good to go!")

@tree.command(name = "streetcarts", description = "Why you should avoid streetcarts", guild=discord.Object(id=GUILD))
@app_commands.checks.cooldown(1, 10)  # Cooldown decorator to limit command usage to once per minute per user.
async def street_carts(interaction):
  # This is an asynchronous function that is called when the user invokes the /streetcarts command in Discord.
  
  # 'interaction' is an object representing the interaction with the Discord bot,
  # containing data such as the user who invoked the command and the channel where it was invoked.

  # The bot responds to the command by sending a message to the channel.
  # The message explains the risks associated with street carts (cannabis oil cartridges sold on the street),
  # which unlike other forms of cannabis, can be adulterated with harmful substances for profit.
  
  # The message emphasizes that street carts can be dangerous due to potential cuts with vitamin E, nicotine, or spice
  # and advises against their use if cannabis is legal in the user's area, suggesting that users should go to a dispensary instead.
  
  # It also mentions that more information about adulterated cannabis can be found by using the /laced command.
  await interaction.response.send_message(
    "While weed is rarely ever laced with any other substance as it's not profitable to do so, "
    "there is one form of weed that you need to be careful of while are street carts\n\n"
    "why should you avoid them? well unlike normal weed they can sometimes be cut for profit "
    "with things such as vitamin E, nicotine, or spice. The same can also apply to pre-rolls as well.\n\n"
    "**if weed is legal where you live go to the dispensary, otherwise just stick to flower it's not worth it**\n\n"
    "more on cuts in weed can be found in the /laced command"
  )

@tree.command(name="laced", description="Here's why if you're buying dry flower weed then your stuff will probably not be laced", guild=discord.Object(id=GUILD))
@app_commands.checks.cooldown(1, 10)  # This sets a cooldown on the command, limiting users to invoke it once per minute.
async def laced(interaction):
    """
    When the '/laced' command is used in Discord, this asynchronous function gets called.
    It sends a detailed message explaining why dry flower cannabis is unlikely to be laced with other substances.

    Parameters:
    interaction : discord.Interaction
        An object representing the interaction with the Discord bot.

    The message sent to the user includes information about common misconceptions regarding laced cannabis.
    It provides various facts to reassure the user and educates them on what to avoid and how to detect contaminants.
    """

    # Prepare the message content with the informative text regarding laced cannabis.
    message_content = (
        "**Here's why if you're buying dry flower weed then your stuff will probably not be laced**\n"
        "On the news, you might hear stories about weed being laced with substances such as fentanyl, crack, meth, heroin, "
        "and angel dust.\nHere are the facts though:\n"
        "- Unless you are buying edibles, pre-rolls, carts, and ground bud illegally, it is more profitable to just give you "
        "the weed than it is to lace it.\n"
        "- If you do buy street edibles, then just know that you're not getting 500mg; 500mg, if you aren't enzyme deficient, "
        "will send you into a coma.\n"
        "- Pre-rolls, carts, and ground bud all come with the risk of being laced with spice, so do not buy those if you "
        "live in an illegal state/country; just stick to bud or make your own concentrate.\n"
        "- Now hypothetically (with bud, this is extremely rare, and isn't meant to fear-monger), if the person giving you "
        "the bud is malicious, then the most likely adulterants would be some sort of liquid spice or angel dust. Both of "
        "which would make it cheaper to just sell the weed on its own.\n"
        "- One common risk with bud, used to increase profits, is that you get bud with pesticides. Pesticides can harm your "
        "lungs and should not be smoked; make sure you buy the weed from a dealer who you know doesn't use pesticides or "
        "buy your weed legally.\n"
        "- This isn't a cut, but important to mention: if you find mold/fungus on your bud then do not smoke it. You can get "
        "spores in your lungs which can cause the fungus to grow there and it can kill you. IF THERE IS MOLD ON YOUR WEED, "
        "THEN DO NOT SMOKE IT.\n"
        "- An easy test to see if your weed is cut with pesticides is to place a nug on a paper clip and set it on fire; if it "
        "ignites quickly, it's likely sprayed with harmful chemicals (this tip was copied from triplethreat)."
    )

    # Send the prepared message as a response to the interaction.
    await interaction.response.send_message(message_content)

@tree.command(name = "rules", description = "in case you're too lazy to go to #rules", guild=discord.Object(id=GUILD))
@app_commands.checks.cooldown(1, 10)
async def rules(interaction: discord.Interaction) -> None:
    """
    Sends the server rules as a message in response to the '/rules' command invocation.

    Parameters:
    interaction : discord.Interaction
        The interaction object containing details of the command invocation.
    
    Returns:
    None
    """
    await interaction.response.send_message("Welcome to **Puff Palace**, here are some of the rules that must be followed\n\n1. 18+ (we will not ask for your age, and we will not ban you if you do not tell us your age)\n\n2. Follow the discord TOS as well as the law\n\n3. This server values freedom of speech highly however there are some limits(such as no spamming, no spamming, etc).\n\n4. There are rules to sourcing on this server which are officially listed on the announcements channel\n\n5. Audit logs are always open for everyone to prevent mod/admin abuse. If you witness any admin/mod abuse, call it out. There will be roles for users to inspect mod channels as well to audit it for mod abuse\n\n6. We allow anyone to add emojis here however do not ruin this privilege for others. NSFW emojis and vandalism will result in a ban\n\n7. idc about y’all’s beef but keep that shit in DMs(or ya know just block)\n\n8. Pingable names, it gets god damn annoying when you use special characters\n\n9. This is it for now but it may be subject to change")

@tree.command(name="bully", description="why tf am i getting bullied", guild=discord.Object(id=GUILD))
@app_commands.checks.cooldown(1, 10)
async def bully(interaction):
    # The 'bully' command is a slash command registered to the bot's command tree.
    # It is associated with the guild (server) identified by the variable 'GUILD'.
    # The command has a cooldown decorator to prevent abuse, limiting its use to once per minute.

    # Construct the message that will be sent in response to the command.
    # The message contains a mix of serious content about bullying and a quote from Tyler, the Creator
    # suggesting a nonchalant attitude towards cyberbullying. It is followed by a disclaimer that comedy
    # is not considered extreme behavior.
    message = (
        '**Why tf am I getting bullied**\n'
        'ha get wrecked bitch, take the L and keep getting bullied.\n\n'
        'Jokes aside, this server has one mentality when it comes to being "bullied". '
        'Unless it’s something extreme such as doxxing, swatting or sexual harassment, '
        'then as Tyler the creator said **"Hahahahahahahaha How The Fuck Is Cyber Bullying Real Hahahaha '
        'Nigga Just Walk Away From The Screen Like Nigga Close Your Eyes Haha"**\n\n'
        'Also side note, comedy does not count ever with extreme'
    )

    # Send the prepared message as a response to the interaction.
    await interaction.response.send_message(message)



@tree.command(name="cat", description="Sends a random image of a very cute cat", guild=discord.Object(id=GUILD))
@app_commands.checks.cooldown(1, 10)
async def cat(interaction):
    #command which sends a random image of a cute cat when /cat is used
    try:
        #trys to request cat api for an image of a cat
        response = requests.get(CAT_API)
        data = response.json()
        cat_image_url = data[0]["url"]

        await interaction.response.send_message(f"Awwwww 🥺😻 that's such a cute cat:\n\n {cat_image_url}")

    except Exception as e:
        print(f"Error: {e}")

@tree.command(name="dog", description="Sends a random image of a very cute dog", guild=discord.Object(id=GUILD))
@app_commands.checks.cooldown(1, 10)
async def dog(interaction):
    #command which sends a random image of a cute dog when /dog is used
    try:
        #trys to request dog api for an image of a dog
        response = requests.get(DOG_API)
        data = response.json()
        dog_image_url = data[0]["url"]

        await interaction.response.send_message(f"Awwwww 🥺🐕 that's such a cute dog:\n\n {dog_image_url}")

    except Exception as e:
        print(f"Error: {e}")

@tree.command(name="breakingbad", description="sends a random quote from Breaking Bad", guild=discord.Object(id=GUILD))
@app_commands.checks.cooldown(1, 10)
async def breakingbad(interaction):
    #command which sends a random quote from Breaking Bad when /breakingbad is used
    try:
        #trys to request Breaking Bad api for a quote
        response = requests.get("https://api.breakingbadquotes.xyz/v1/quotes")
        data = response.json()
        quote = data[0]["quote"]
        author = data[0]["author"]

        await interaction.response.send_message(f"\"{quote}\" - {author}")

    except Exception as e:
        print(f"Error: {e}")

@tree.command(name="randomfacts", description="sends a random fact", guild=discord.Object(id=GUILD))
@app_commands.checks.cooldown(1, 10)
async def randomfacts(interaction):
    #command which sends a random fact when /randomfacts is used
    try:
        #trys to request useless facts api for a random fact
        response = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random")
        data = response.json()
        fact = data["text"]

        await interaction.response.send_message(f"{fact}")

    except Exception as e:
        print(f"Error: {e}")

@tree.command(name="quran", description="sends a random quran verse", guild=discord.Object(id=GUILD))
@app_commands.checks.cooldown(1, 10)
async def quran(interaction):
    #command which sends a random quran verse when /quran is used
    verse_num = random.randint(1, 6236)
    try:
        #trys to request quran api for a random quran verse
        response = requests.get("http://api.alquran.cloud/ayah/" + str(verse_num) + "/editions/quran-uthmani,en.pickthall")
        data = response.json()
        ar_verse = data["data"][0]["text"]
        en_verse = data["data"][1]["text"]
        surah = data["data"][0]["surah"]["englishName"]
        aya = data["data"][0]["numberInSurah"]

        await interaction.response.send_message(f"{ar_verse}\n\n{en_verse} - {surah}, {aya}")

    except Exception as e:
        print(f"Error: {e}")

@tree.command(name="currency", description="converts currency", guild=discord.Object(id=GUILD))
@app_commands.checks.cooldown(1, 10)
async def currency(interaction, amount: int, from_currency: str, to_currency: str):
    #command which converts currency when /currency is used
    try:
        #trys to request currency api for a converted currency
        response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{from_currency}")
        data = response.json()
        rate = data["rates"][to_currency]
        converted_amount = amount * rate

        await interaction.response.send_message(f"{amount} {from_currency} is equal to {converted_amount} {to_currency}")
    except Exception as e:
        await interaction.response.send_message("Invalid currency code")
        print(f"Error: {e}")

@tree.command(name="isitdown", description="Is the website up", guild=discord.Object(id=GUILD))
@app_commands.checks.cooldown(1, 10)
async def is_it_up(interaction, site: str):
    if not site.startswith(("https://", "http://")):
        if site.startswith("www."):
            site = "https://" + site
        else:
            site = "https://www." + site
    try:
        r = httpx.get(site, timeout=5)
        if r.status_code == 200:
            await interaction.response.send_message(f"{site} is up :)")
        else:
            await interaction.response.send_message(f"{site} is down 😦 - Status Code: {r.status_code}")
    except Exception as e:
        await interaction.response.send_message(f"{site} is down 😦 - Error: {e}")
@client.event
async def on_member_join(member):
    #when a member joins the server it sends a welcome message
    channel = client.get_channel(1224807171078885377)
    await channel.send(f"Welcome {member.mention} to Puff Palace. Whether you want to chill, VC or send some shisha pics. You're welcome for all, sit back, relax and vibe.")

@client.event
async def on_member_remove(member):
    #when a member leaves the server volunatrily, then it sends a goodbye message
    channel = client.get_channel(1224807171078885377)
    await channel.send(f"Awwwww {member.mention} left 😢, RIP")

@client.event
async def on_member_ban(guild, member):
    #when a member is banned it sends a message
    channel = client.get_channel(1224807171078885377)
    await channel.send("haaaaaa, someone got banned Get fucking wrecked mothafucka")

client.run(TOKEN)