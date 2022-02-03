# gpt2-discord-impersonator
A Conversational Discord Bot built on top of GPT-2 (for now) 
*a.k.a bot to talk to when you're bored*

Still in early prototyping. The code is rough and untested.

Based off of minimaxir's [gpt-2-simple](https://github.com/minimaxir/gpt-2-simple) package. Big thanks to him.

## My Environment

See requirements.txt

## Training

TODO but you can refer to train.py for now.

### Creating a Dataset

You should use a discord chat exporter like [this](https://github.com/Tyrrrz/DiscordChatExporter/releases/tag/2.20) and export it to txt. The format for my dataset was as follows:

```
name1:
conversational message here
maybe another one here
until another user sends a message

name2:
conversational reply here

name1:
reply

name2:
reply reply
blah blah

name3:
blah blah blah
```

You need to train the model to output this format as the bot is coded to expect that. Your model may not output this format is the loss is not low enough.

### Finetuning the model

Unless you have 12GB of VRAM, it's probably very unlikely you will able to load a large model, I recommend using the smaller `124M` model first and seeing how much VRAM it takes.

If you still don't have enough VRAM you may need to clone the [gpt-2-simple](https://github.com/minimaxir/gpt-2-simple) repo directly into this one and modify the .sample() parameter to smaller value in the sample_batch() function within gpt_2.py.

Below is code to finetune a model basically:

```python
import gpt_2_simple as gpt2
from datetime import datetime


file_name = "dataset.txt" # File name of dataset

sess = gpt2.start_tf_sess()

gpt2.finetune(
            sess,
            dataset=file_name,
            model_name='355M', # Model you have already downloaded
            steps=-1, # -1 will do unlimited. Enter number of iterations otherwise
            restore_from='latest', # Also allows 'fresh' which will overwrite old training
            run_name='discord', # The name to pull or create a checkpoint under
            print_every=50, # Print iterations every X numebr
            sample_every=150, # Generate a text sample ever X number of iter.
            save_every=500, # Save a snapshot every X number of iter.
            learning_rate=0.0001, # Lower to 0.00001 if you are not getting massive changes in results
            batch_size=1 # Keep at 1 or 2, will use up more memory if you raise this
)
```

You can run this everytime and it will train your model and pick up from where it left off, or start a new one if you have a new `run_name`. 

Finetune your model until it reaches around 8k-10k iterations.

## The Discord Bot Part

Create a discord bot on the discord site.

First you need to go to the [Applications Section](https://discord.com/developers/applications) of the developer panel. Inside you need to create a new app.

<p align="center">
  <img src="https://i.imgur.com/oiUA5hT.png">
</p>

Add a name and go to the new application's settings. You need to create a Bot User:

<p align="center">
  <img src="https://i.imgur.com/qx3BviW.png">
</p>

Now copy the token for the bot.

## Credits
README modified from https://github.com/M4cs/yourAI
Thank you M4cs for the easy intro and inspiration into this project.
