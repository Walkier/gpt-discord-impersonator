import discord, datetime
import gpt_2_simple as gpt2
import asyncio, random, string


sess = gpt2.start_tf_sess()
run_name = 'perpen-BIGNETWORKr2'
gpt2.load_gpt2(sess, run_name=run_name)#, checkpoint='model-9500') # The name of your checkpoint

pretend_target = "mcmuffinoven"
pretend_target_target = "sup sup"
BOTNAME = 'faceless-t'

client = discord.Client()
running_lock = False

#reply to seen messsage
#masked
#big model, small sample
#increase context
#choose model and personal
#makeconvo (Walkier: )

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    activity = discord.Activity(name="Affirmative, Dave.", type=discord.ActivityType.watching)
    await client.change_presence(status=discord.Status.online, activity=activity)

@client.event
async def on_message(message):
        # if client.user.mention in message.content.replace('<@!', '<@'):
        global running_lock

        if message.author == client.user or message.author.bot:
            return
        elif running_lock:
            print('locked out')
            return
        else:
            if client.is_ready:
                async with message.channel.typing():
                    running_lock = True
                    if "makeconvo" in message.content:
                        print("Gen Convo")
                        results = gpt2.generate(sess, run_name=run_name, temperature=0.9, nsamples=1, batch_size=1, prefix=message.author.name + ":\n" + message.content + "\n\n", length=350, include_prefix=True, return_as_list=True)
                        await message.channel.send("```\n" + str('=' * 20).join(results) + "\n```")
                    else:
                        print("Generating")
                        final = ''
                        prefix = ""
                        last_author = ""
                        old = await message.channel.history(limit=9).flatten()
                        old.reverse()
                        for msg in old:
                            if last_author == msg.author.name:
                                if len(msg.mentions) > 0:
                                    for mention in msg.mentions:
                                        msg.content.replace("<@!" + str(mention.id) + ">", "@" + mention.name)
                                prefix = prefix + msg.content + "\n"
                            else:
                                if len(msg.mentions) > 0:
                                    for mention in msg.mentions:
                                        msg.content.replace("<@!" + str(mention.id) + ">", "@" + mention.name)
                                last_author = msg.author.name

                                auth = msg.author.name 
                                if msg.author.name == 'faceless-t':
                                    auth = pretend_target
                                if msg.author.name == pretend_target:
                                    auth = pretend_target_target

                                prefix = prefix + "\n" + auth + ":\n" + msg.content + "\n"

                        print('prompt:\n'+prefix + f'\n{pretend_target}:\n')
                        print('--EOP--')

                        while True:
                            results = gpt2.generate(sess, run_name=run_name, temperature=0.9, nsamples=3, batch_size=3, prefix=prefix + f'\n{pretend_target}:\n', length=250, truncate="\n\n", return_as_list=True, include_prefix=False)
                            res_split = random.choice(results).split('\n')
                            ok = []
                            for r in res_split:
                                if not r.endswith(":") and len(r) > 2 and "http" not in r:
                                    ok.append(r)
                            if len(ok) > 0:
                                break
                        
                        #sends generated messages
                        for i, msg in enumerate(ok):
                            if i == (len(ok) -1):
                                await asyncio.sleep(random.randint(0,1))
                                await message.channel.send(msg)
                            else:
                                async with message.channel.typing():
                                    await message.channel.send(msg)
                                    await asyncio.sleep(random.randint(1, 3))
                    running_lock = False
            else:
                return



client.run('OTMwMTAyNTMwNDkzNTM0MjM5.Ydw_ew.CxXcGLkcqswLBSXuGd20x1v0gAM')
