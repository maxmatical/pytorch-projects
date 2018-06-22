# pytorch-projects

# TODO

1. train_val_split
- use multiple data loaders for training data and SubsetRandomSampler to create train/val data (https://am207.github.io/2018spring/wiki/ValidationSplits.html)

2. create a way to internally evaluate validation loss during training
- define a function to predict on validation set while training (https://github.com/kuangliu/pytorch-cifar/blob/master/main.py)

3. create early stopping condition in training

4. create model checkpoint condition in training

5. Snapshot ensembles

6. Model initialization


- can look at pytorch ignite (https://pytorch.org/ignite/index.html) for early stopping/model checkpoint
