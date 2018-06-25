# pytorch-projects

# TODO

1. train_val_split
- use multiple data loaders for training data and SubsetRandomSampler to create train/val data (https://am207.github.io/2018spring/wiki/ValidationSplits.html)

- can use sklearn train_test_split

2. create a way to internally evaluate validation loss during training
- done (cifar10 another version)

3. create early stopping condition in training

4. create model checkpoint condition in training

5. Snapshot ensembles

6. Model initialization

7. Learning Rate annealing
- lr_finder()
- cosine annealing
- cosine annealing with warm restarts
- snapshot ensembles
- no need to create stopping condition during training. train over full epochs

8. Freeze layers/blocks

- can look at pytorch ignite (https://pytorch.org/ignite/index.html) for early stopping/model checkpoint
