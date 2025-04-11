#Importation de modules (discord)
import discord #2.3.2
from discord.ext import commands

import asyncio, time, os, json
from typing import Literal

from random import randint


#################################################################################################################

def supprime_accent(ligne):
    """ supprime les accents du texte source """
    accents = { 'a': ['à', 'ã', 'á', 'â'],
                'e': ['é', 'è', 'ê', 'ë'],
                'i': ['î', 'ï'],
                'u': ['ù', 'ü', 'û'],
                'o': ['ô', 'ö'],
                ' ': ['-', "'"] }
    for char, accented_chars in accents.items():
        for accented_char in accented_chars:
            ligne = ligne.replace(accented_char, char)
    return ligne


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.hybrid_command(name= 'quiz', description = "Quiz géographie", brief = 'Quiz géographie 🌍')
    async def quiz(self, ctx, category: Literal['flag'] = 'flag', nbr_question: int= 15, time_answer: int = 15):
        """
        QUIZ : Le Quiz Ultime de Géographie. Le but du jeu est de répondre aux questions posées par le bot. 
        Mais attention, vous disposez d'un temps limité pour répondre et vous êtes en compétition avec les autres joueurs. 
        À la fin de la partie, un classement des joueurs ayant répondu correctement au plus grand nombre de questions sera affiché.

        Catégorie :
        • `flag` [par défaut] : Le bot vous montre un drapeau et vous devez deviner le pays.
        
        `!quiz [catégorie] [nombre de questions] [temps pour répondre]`
        ou
        `/quiz`
        """

        with open(os.getcwd() + f'/games/states.json', encoding="utf-8") as quiz_file:
            data = json.load(quiz_file)

        flag_removed = []
        nbr_flags = len(data)
        leaderboard = []
        for i in range(nbr_question):

            n = randint(0, nbr_flags-1)
            while n in flag_removed:
                n = randint(0, nbr_flags-1)

            flag_removed.append(n)

            file=discord.File(os.getcwd() + f'/games/images/flag/{data[n]["code"]}.png')

            embed = discord.Embed(title=f"GEO QUIZ 🌍")

            embed.set_image(url = f'attachment://{data[n]["code"]}.png')
            embed.add_field(name = "Quel est-ce pays ?", value="", inline = True)
            embed.set_footer(text = f"Question {i+1}/{nbr_question} | Temps pour répondre: {time_answer}s | Catégorie: {category}")

            message = await ctx.send(embed=embed, file = file)

            answered_correctly = False
            start_time = time.time()

            while not answered_correctly and time.time() - start_time < time_answer:

                try:
                    response = await self.bot.wait_for("message", timeout=(time_answer - (time.time() - start_time)), check=lambda m: m.channel == ctx.channel)
                    if supprime_accent(response.content.lower()) == supprime_accent(data[n]['answer'].lower()):
                            
                        await ctx.send(f"GG <@{response.author.id}>! La pays était: {data[n]['answer']}")
                        answered_correctly = True

                        Verif = False

                        for i in range(0, len(leaderboard)):

                            if leaderboard[i]["id"] == response.author.id:
                                leaderboard[i]["score"] +=1
                                Verif = True
                                    
                        if Verif == False:
                            leaderboard.append({"id": response.author.id, "score": 1})

                except asyncio.TimeoutError:
                    await ctx.send("Le temps est écoulé!")
                    await asyncio.sleep(1)
                    await ctx.send(f"Le pays était: {data[n]['answer']}")
                    break

            await asyncio.sleep(1)

        await asyncio.sleep(1)
        await ctx.send("Partie terminée")

        message = ''
        data_sorted = sorted(leaderboard, key=lambda x: x['score'], reverse=True)
        for i in range(0, len(leaderboard)):
            message += f"\n#{i+1} | <@{data_sorted[i]['id']}> Score: {data_sorted[i]['score']}"

        embed = discord.Embed(title=f"LEADERBOARD GEO QUIZ 🌍")

        embed.add_field(name="Classement :", value=message, inline = True)
        await ctx.send(embed=embed)