from nextcord import Interaction

import nextcord
from datetime import datetime

def dropdown(defOptions, defPlaceholder):

    # defOptions is a list of options to be displayed in the dropdown menu


    class Dropdown(nextcord.ui.Select):

        votes = {}

        def __init__(self, votes=votes):



            selectOption = []

            for idx, opt in enumerate(defOptions):
                votes[f"{idx}"] = {}
                selectOption.append(nextcord.SelectOption(label=f"{opt}",value=f"{idx}"))

            super().__init__(placeholder=f"select your vote", min_values=1, max_values=1, options=selectOption)




        async def callback(self, interaction: nextcord.Interaction, votes=votes):

            totalVotesCount = 0

            embed = nextcord.Embed(title=f"{defPlaceholder}", description="vote results :")
            embed.timestamp = datetime.now()

            for idx,_ in enumerate(votes):
                if f"{interaction.user.id}" in votes[f"{idx}"].keys():
                    del votes[f"{idx}"][f"{interaction.user.id}"]



            votes[self.values[0]][f"{interaction.user.id}"] = 1

            for idx,v in enumerate(votes):
                totalVotesCount += len(votes[f"{idx}"])



            for idx,v in enumerate(votes):
                mentions = ""
                for idx2, v2 in enumerate(votes[f"{idx}"]):
                    if type(v2) == str:
                        mentions += " " + interaction.guild.get_member(int(v2)).mention


                if(mentions != ""):
                    embed.add_field(name=defOptions[idx] + " (" + str(round((len(votes[f"{idx}"])/totalVotesCount)*100)) + "%):", value= mentions, inline=False)
                else:
                    embed.add_field(name=defOptions[idx] + " (0%):", value="no votes",inline=False)




            await interaction.message.edit("poll :", embed=embed)




    class DropdownView(nextcord.ui.View):


        def __init__(self):

            super().__init__()

            self.timeout = 43200

            self.add_item(Dropdown())






    ret = DropdownView()

    return ret

