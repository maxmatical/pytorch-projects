# pytorch-projects

# TODO

# train_val_split
- use multiple data loaders for training data and SubsetRandomSampler to create train/val data (https://am207.github.io/2018spring/wiki/ValidationSplits.html)

- can use sklearn train_test_split

# create a way to internally evaluate validation loss during training
- done (cifar10 another version)
- note, training can be done more easily using fit(model, data, n_epochs, optimizer, loss_fn) from fast.ai

# create early stopping condition in training

# create model checkpoint condition in training
-  Saving/loading model at the end of a specified epoch 
- https://stackoverflow.com/questions/42703500/best-way-to-save-a-trained-model-in-pytorch/43819235
- https://cs230-stanford.github.io/pytorch-getting-started.html#saving-and-loading-models
- can look at pytorch ignite (https://pytorch.org/ignite/index.html) for early stopping/model checkpoint

Alt approach: save model to a different output file after every x epochs (save only the last n models). Load latest model before overfitting and train for a few epochs, stopping just before overfitting

i.e. if (epoch + 1)%10 == 0 and (epoch + 1) >= some number:
        save model

https://www.programcreek.com/python/example/101175/torch.save

# Snapshot ensembles

# Model initialization
https://stackoverflow.com/questions/49433936/how-to-initialize-weights-in-pytorch


# Learning Rate annealing
- lr_finder()
- cosine annealing
- cosine annealing with warm restarts
- snapshot ensembles
- no need to create stopping condition during training. train over full epochs

# Freeze layers/blocks

# multiple inputs/outputs (done)
https://discuss.pytorch.org/t/nn-module-with-multiple-inputs/237/3

