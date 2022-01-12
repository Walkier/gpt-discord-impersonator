import gpt_2_simple as gpt2
import os

file_name = "chats-in-text-format-2022.txt" # File name of dataset

model_name = "355M"
if not os.path.isdir(os.path.join("models", model_name)):
	print(f"Downloading {model_name} model...")
	gpt2.download_gpt2(model_name=model_name)   # model is saved into current directory under /models/124M/

sess = gpt2.start_tf_sess()

gpt2.finetune(
            sess,
            dataset=file_name,
            model_name=model_name, # Model you have already downloaded
            steps=100, # -1 will do unlimited. Enter number of iterations otherwise
            restore_from='latest', # Also allows 'fresh' which will overwrite old training
            run_name='perpen-BIGNETWORKr2', # The name to pull or create a checkpoint under
            print_every=1, # Print iterations every X numebr
            sample_every=1000000, # Generate a text sample ever X number of iter.
            save_every=5, # Save a snapshot every X number of iter.
            learning_rate=0.0001, # Lower to 0.00001 if you are not getting massive changes in results
            sample_token_Len = 64+16,
            batch_size=1, # Keep at 1 or 2, will use up more memory if you raise this
            max_checkpoints=5,
            only_train_transformer_layers=True,
            accumulate_gradients=1,
)
