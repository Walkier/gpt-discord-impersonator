class Pipeline():
    pass

import asyncio
import random
import gpt_2_simple as gpt2

class ConversationPipeline(Pipeline):
    def __init__(self, run_name, command_prefix, bot_name, pretend_target, pretend_target_target, checkpoint='latest', *args):
        super().__init__()

        self.__sess = gpt2.start_tf_sess()
        self._run_name = None
        self._checkpoint = None
        self.__load_model(run_name, checkpoint)

        self._bot_name = bot_name
        self._pretend_target = pretend_target
        self._pretend_target_target = pretend_target_target
        self._command_prefix = command_prefix

        self._make_convo_len = 256
        self._reply_len = 128

        self._running = False

        self._buffer_secs = 3
        self.__msg_stack = []
        self._inf_flag = False
        self._msg_history_len = 16

    def __load_model(self, run_name, checkpoint='latest'):
        gpt2.load_gpt2(self.__sess, run_name=run_name, checkpoint=checkpoint)

        self._run_name = run_name
        self._checkpoint = checkpoint

    async def buffer(self, message):
        if not self._inf_flag:
            self.__msg_stack.append(message)
        else:
            print('blocked')

        if not self._running:
            self._running = True

            print('waiting')
            await asyncio.sleep(self._buffer_secs)
            print('done wait')

            self._inf_flag = True

            await self.reply(self.__msg_stack[-1])
            print('replied')

            self._inf_flag = False
            
            self.__msg_stack = []
            self._running = False

    async def reply(self, message):
        pretend_target = self._pretend_target
        pretend_target_target = self._pretend_target_target
        BOTNAME = self._bot_name
        
        run_name = self._run_name

        if "genconvo" in message.content:
            print("Gen Convo (make this into a command pls)")
            results = gpt2.generate(self.__sess, run_name=run_name, temperature=0.9, nsamples=1, batch_size=1, prefix=pretend_target + ":\n", length=self._make_convo_len, include_prefix=True, return_as_list=True)
            await message.channel.send(".```\n" + str('=' * 20).join(results) + "\n```")
        else:
            print("Generating")
            prefix = ""
            last_author = ""
            old = await message.channel.history(limit=self._msg_history_len).flatten()
            old.reverse()
            for msg in old:
                if msg.content.startswith(self._command_prefix) or msg.content.startswith(self._command_prefix+'```'):
                    continue

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

            prompt = prefix + f'\n{pretend_target}:\n'
            print('prompt:\n'+prefix + f'\n{pretend_target}:\n')
            print('--EOP--')

            async with message.channel.typing():
                results = gpt2.generate(self.__sess, run_name=run_name, temperature=0.9, nsamples=1, batch_size=1, prefix=prompt, length=self._reply_len, truncate="\n\n", return_as_list=True, include_prefix=False)
                res_split = results[0].split('\n')
                ok = []
                for r in res_split:
                    if len(r) > 2:
                        ok.append(r)
                if len(ok) <= 0:
                    return                    
            
            print('inf done')
            
            #sends generated messages
            
            await message.reply(ok[0])
            if len(ok) > 1:
                async with message.channel.typing():
                    for msg in ok[1:]:
                        await asyncio.sleep(random.randint(1, 3))
                        await message.channel.send(msg)
            