#Importation de modules (discord)
import discord #2.3.2
from discord.ext import commands

#Importations cogs
from cogs import games

#################################################################################################################

TOKEN = "TOKEN"
ID = "SERVEUR_ID"

#Paramètrage du bot
intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', description = 'GeoQuiz by Arthur_Lfbvr', intents=intents)
MY_GUILD = discord.Object(id=ID)

@bot.event
async def on_ready():
    print(f'Connecte en tant que {bot.user} (ID: {bot.user.id})')

    await bot.add_cog(games.Games(bot), override = True)

    bot.tree.copy_global_to(guild=MY_GUILD)
    await bot.tree.sync(guild=MY_GUILD)


#################################################################################################################

class Help(commands.HelpCommand):

    #Commande d'aide globale
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title=f"Help {bot.user.name}", description = f"*{bot.user.name} by Arthur_Lfbvr*", color = 0x4DA8F8)
        embed.set_thumbnail(url=bot.user.display_avatar)
        for cog, commands in mapping.items():
            if cog != None :
                #filtered = await self.filter_commands(commands, sort=True)
                cog_name = getattr(cog, "qualified_name")
                embed.add_field(name="", value=f"**• {cog_name}** -> `{bot.command_prefix}help {cog_name}`", inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

    #Partie aide spécifique aux cogs
    async def send_cog_help(self, cog):
        embed = discord.Embed(title=f"Catégorie {cog.qualified_name} ({len(cog.get_commands())})" or "No Category", description = cog.description, color = 0x4DA8F8)
        filtered_commands = await self.filter_commands(cog.get_commands())
        for command in filtered_commands:
            embed.add_field(name="", value=f"**• {command.brief}** -> `{bot.command_prefix}{command.name}`", inline=False)
        embed.set_footer(text = f"Pour plus d'infos sur une commande spécifique -> {bot.command_prefix}help [COMMANDE]")

        channel = self.get_destination()
        await channel.send(embed=embed)

    #Partie aide spécifique aux commandes
    async def send_command_help(self, command):
        embed = discord.Embed(title=command.brief, color = 0x4DA8F8)

        embed.add_field(name="", value = f"{command.help}", inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

    #Gestion des erreurs
    async def send_error_message(self, error):
        embed = discord.Embed(title="⚠ ERREUR ⚠", description=error, color=discord.Color.red())
        channel = self.get_destination()

        await channel.send(embed=embed)

bot.help_command = Help()

#################################################################################################################

#Gestion des erreurs

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        error = f"Commande inconnue. Faite **{bot.command_prefix}help** pour voir la liste des commandes."
    elif isinstance(error, commands.MissingRequiredArgument):
        error = "Vous avez oublié un argument."
    elif isinstance(error, commands.BotMissingPermissions):
        error = "Je ne dispose pas des permissions nécessaires pour exécuter cette commande."
    elif isinstance(error, commands.MissingPermissions):
        error = "Vous n'avez pas les autorisations nécessaires pour exécuter cette commande."
    elif isinstance(error, commands.CheckFailure):
        error = "Vous êtes dans le mauvais salon et/ou vous ne disposez pas des autorisations nécessaires pour utiliser cette commande."
    embed = discord.Embed(title="⚠ ERREUR ⚠", description=error, color=discord.Color.red())
    await ctx.send(embed=embed)

#################################################################################################################

#Token
bot.run(TOKEN)