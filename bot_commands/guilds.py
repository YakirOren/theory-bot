import discord
from discord.ext import commands

RED = 0xFF0000
CMD_USERS = ["yakirLaptop#4906", "YakirOren#1424"]

class guilds_command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def is_cmd_user(ctx):
        return str(ctx.author) in CMD_USERS
                                        
    @commands.check(is_cmd_user)
    @commands.group()
    async def guilds(self, ctx):
        """"""

        if ctx.invoked_subcommand is None:
            embed = discord.Embed(title="Guilds:", color=0x62fff8)
        
            commands = ['list','members <guild id>','channels <guild id>']

            for command in commands:
                embed.add_field(name=command, value='\u200b', inline=False)
            await ctx.channel.send(embed=embed)



    @guilds.command()
    async def list(self, ctx):
        embed = discord.Embed(title="Guilds:", color=0x62fff8)
        
        for guild in self.bot.guilds:
            embed.add_field(name=guild.name, value=guild.id, inline=False)
        await ctx.channel.send(embed=embed)

    
    @guilds.command()
    async def members(self, ctx, id:int):
        embed = discord.Embed(title=f"Members in {self.bot.get_guild(id)}", color=0x62fff8)

        for member in self.bot.get_guild(id).members:
            embed.add_field(name=member.name, value=f"{member.id} {member.joined_at} " , inline=False)
        await ctx.channel.send(embed=embed)


    
    @guilds.command()
    async def channels(self, ctx, id:int):
        embed = discord.Embed(title=f"Channels in {self.bot.get_guild(id)}", color=0x62fff8)
        
        for channel in self.bot.get_guild(id).channels:
            embed.add_field(name=channel.name, value=channel.id, inline=False)
        
        await ctx.channel.send(embed=embed)


    @guilds.error
    async def guilds_error(self, ctx, error):
        """
        """
        if isinstance(error, commands.CheckFailure):
            error_embed = discord.Embed(title="Missing Permissions!", color=RED)
        else:
            error_embed = discord.Embed(title="ERROR.", description="{0}".format(error), color=RED)
        await ctx.channel.send(embed=error_embed)


def setup(bot):
    bot.add_cog(guilds_command(bot))


