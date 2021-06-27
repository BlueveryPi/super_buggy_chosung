import discord, asyncio, random
from discord.ext import commands

token="ODIzNzkzOTcyMTQwMDQ4NDA2.YFl_7A.60u1p_STHuyLUmev6_o02Gi1z2c"
game=discord.Game("초성게임")
bot=commands.Bot(command_prefix="!", status=discord.Status.online, activity=game)

player={}
tmp={}
tmpm={}
tmpw={}

@bot.event
async def on_ready():
    print("ready")

async def playerinit(ctx):
    if player!={}:
        if player[ctx.guild.id]!={}:
            if player[ctx.guild.id][ctx.channel.id]!={}:
                pass
            else:
                player[ctx.guild.id][ctx.channel.id]={"isdone":True, "players":[]}
        else:
            player[ctx.guild.id]={}
            player[ctx.guild.id][ctx.channel.id]={"isdone":True, "players":[]}
    else:
        player[ctx.guild.id]={}
        player[ctx.guild.id][ctx.channel.id]={"isdone":True, "players":[]}

@bot.command()
async def 초성(ctx, arg=None):
    if tmpw!={}:
        if tmpw[ctx.guild.id]!={}:
            if tmpw[ctx.guild.id][ctx.channel.id]!={}:
                pass
            else:
                tmpw[ctx.guild.id][ctx.channel.id]=""
        else:
            tmpw[ctx.guild.id]={}
            tmpw[ctx.guild.id][ctx.channel.id]=""
    else:
        tmpw[ctx.guild.id]={}
        tmpw[ctx.guild.id][ctx.channel.id]=""
    if arg!=None:
        if arg=="시작":
            if tmp=={}:
                await ctx.channel.send("아직 아무도 없는 것 같아요..  :cry:")
                return
            elif tmp[ctx.guild.id]=={}:
                await ctx.channel.send("아직 아무도 없는 것 같아요..  :cry:")
                return
            elif tmp[ctx.guild.id][ctx.channel.id]=={}:
                await ctx.channel.send("아직 아무도 없는 것 같아요..  :cry:")
                return

            await playerinit(ctx)
            if player[ctx.guild.id][ctx.channel.id]["isdone"]==True:
                if len(tmp[ctx.guild.id][ctx.channel.id])>0:
                    player[ctx.guild.id][ctx.channel.id]["isdone"]=False
                    player[ctx.guild.id][ctx.channel.id]["players"]=tmp[ctx.guild.id][ctx.message.channel.id]
                    await ctx.channel.send(f"{ctx.channel.mention}에서의 초성게임을 시작할게요!  :partying_face:")
                    await game(ctx)
                    
                else:
                    await ctx.channel.send("아직 혼자인 것 같아요..  :cry:")
            else:
                await ctx.channel.send("아직 이 채널에서의 게임이 끝나지 않았어요!")


        elif arg=="참가":
            try:
                if player[ctx.guild.id][ctx.channel.id]["isdone"]==False:
                    await ctx.channel.send("아직 게임이 끝나지 않았어요! 잠시만 기다려 주세요! :sweat_smile:")
                elif ctx.author in tmp[ctx.guild.id][ctx.channel.id]:
                    await ctx.channel.send("앗! 이미 게임에 참가하고 있어요!")
                else:
                    tmp[ctx.guild.id][ctx.channel.id].append(ctx.author)
                    await ctx.channel.send(f"{ctx.author.mention} 님이 참가하셨습니다!  :wave:")
            except KeyError:
                await playerinit(ctx)
                tmp[ctx.guild.id]={}
                tmp[ctx.guild.id][ctx.channel.id]=[ctx.author]
                await ctx.channel.send(f"{ctx.author.mention} 님이 참가하셨습니다!  :wave:")

        elif arg=="나가기":
            try:
                player[ctx.guild.id][ctx.channel.id]["players"]
            except KeyError:
                await playerinit(ctx)

            if player[ctx.guild.id][ctx.channel.id]["isdone"]==True:
                if tmp!={}:
                    if tmp[ctx.guild.id]!={}:
                        if tmp[ctx.guild.id][ctx.channel.id]!=[]:
                            tmp[ctx.guild.id][ctx.channel.id].remove(ctx.author)
                            await ctx.channel.send(f"{ctx.author.mention}님이 나가셨어요..  :cry:")
                        else:
                            await ctx.channel.send("아직 아무도 없어요!  :confused:")
                    else:
                        await ctx.channel.send("아직 아무도 없어요!  :confused:")
                else:
                    await ctx.channel.send("아직 아무도 없어요!  :confused:")

            else:
                try:
                    if player[ctx.guild.id][ctx.channel.id]["players"]!=[]:
                        player[ctx.guild.id][ctx.channel.id]["players"].remove(ctx.author)
                        await ctx.channel.send(f"{ctx.author.mention}님이 나가셨어요..  :cry:")
                    else:
                        await ctx.channel.send("아직 아무도 없어요!  :confused:")
                        
                except ValueError:
                    await ctx.channel.send(f"{ctx.author.mention}님은 아직 참여하고 있지 않으세요!  :confused:")

                
        else:
            await ctx.channel.send(f"읭? `{arg}`은(는) 명령어가 아니에요!  :confused:")
        
    else:
        await ctx.channel.send("명령이 틀렸어요! `!초성게임 {할것}`의 형태로 적어주세요!  :confused:")
        return

@bot.command()
async def 정답(ctx):
    if ctx.guild.id in player.keys():
        if ctx.channel.id in player[ctx.guild.id].keys():
            if player[ctx.guild.id][ctx.channel.id]["isdone"]==False and ctx.message.content!="!정답":
                arg=ctx.message.content[4:]
                if arg==tmpw[ctx.guild.id][ctx.channel.id]:
                    await ctx.channel.send(f"{ctx.author.mention}님, 축하드립니다! 정답은 ` {arg} ` 이었습니다!  :partying_face:")
                    await asyncio.sleep(1)
                    await ctx.channel.send(f"{ctx.channel.mention}에서의 게임을 종료합니다!")
                    await playerinit(ctx)
                    print(player[ctx.guild.id][ctx.channel.id])
                else:
                    acc=0
                    s=-1
                    for i in tmpw[ctx.guild.id][ctx.channel.id]:
                        s+=1
                        if i != " " and i==arg[s:s+1]:
                            acc+=1/len(tmpw[ctx.guild.id][ctx.channel.id])*100

                    if acc>80:
                        await ctx.reply(f"오!! {round(acc, 2)}%까지 맞췄어요!!  :partying_face:")
                    elif acc>40 and acc<79:
                        await ctx.reply(f"{round(acc, 2)}%까지 맞췄어요!  :grinning:")
                    elif acc>0 and acc<39:
                        await ctx.reply(f"{round(acc, 2)}%!  :open_mouth:")
            else:
                await ctx.channel.send("아직 게임이 시작하지 않았어요!  :confused:")
        else:
            await ctx.channel.send("아직 게임이 시작하지 않았어요!  :confused:")
    else:
        await ctx.channel.send("아직 게임이 시작하지 않았어요!  :confused:")

async def game(ctx):
    players=player[ctx.guild.id][ctx.channel.id]["players"]
    chooser=random.choice(players)
    guesser=players
    guesser.remove(chooser)

    if tmpw!={}:
        if tmpw[ctx.guild.id]!={}:
            if tmpw[ctx.guild.id][ctx.channel.id]!={}:
                pass
            else:
                tmpw[ctx.guild.id][ctx.channel.id]=""
        else:
            tmpw[ctx.guild.id]={}
            tmpw[ctx.guild.id][ctx.channel.id]=""
    else:
        tmpw[ctx.guild.id]={}
        tmpw[ctx.guild.id][ctx.channel.id]=""

    k = await chooser.send(f"{chooser.mention}님이 ` {ctx.guild.name} ` 의 출제자입니다! 이 메시지에 출제 단어로 답장해주세요!  :smile:")
    tmpm[k.id]=[ctx.guild.id, ctx.channel.id]
    await ctx.channel.send(f"{chooser.mention}님이 출제자이십니다!  :partying_face:")
    await ctx.channel.send("문제 정하는 중....")
    while tmpm[k.id][0]!=True:
        await asyncio.sleep(0.5)

    word=tmpm[k.id][1]
    tmpw[ctx.guild.id][ctx.channel.id]=word
    tmpm.pop(k.id)

    wordsplt=[]
    for a in word:
        if ord('가') <= ord(a) <= ord('힣'):
            wordsplt.append(await gc(a))
        else:
            wordsplt.append(a+" ")

    prced=""
    for a in wordsplt:
        prced+=a

    await ctx.channel.send(f"문제가 정해졌습니다!")
    await ctx.channel.send(f"문제는\n` {prced} `\n입니다!")
    
    
async def gc(text):
    CHOSUNG_START_LETTER = 4352
    JAMO_START_LETTER = 44032
    JAMO_END_LETTER = 55203
    JAMO_CYCLE = 588

    def isHangul(ch):
        return ord(ch) >= JAMO_START_LETTER and ord(ch) <= JAMO_END_LETTER

    result = ""

    for ch in text:
        result += chr(int((ord(ch) - JAMO_START_LETTER)/JAMO_CYCLE + CHOSUNG_START_LETTER))      

    return result


@bot.event
async def on_message(ctx):
    if ctx.channel.type == discord.ChannelType.private:
        if ctx.reference!=None:
            if ctx.reference.message_id in tmpm.keys():
                tmpm[ctx.reference.message_id]=[True, ctx.content]

    await bot.process_commands(ctx)


bot.run(token)

