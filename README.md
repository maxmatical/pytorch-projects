# pytorch-projects

# Future projects

- Residual Network + inception (inception v4/inception-resnet)
- SEnet https://github.com/miraclewkf/SENet-PyTorch
- variational autoencoders
- language model (word level)
- language model (character level)
- transformer model 
- Attention Augmented convnets (https://github.com/leaderj1001/Attention-Augmented-Conv2d)
        - can use base AAconv layer as base for future archs (resnets, densenets etc)
# TODO

### structured data models
https://yashuseth.blog/2018/07/22/pytorch-neural-network-for-tabular-data-with-categorical-embeddings/

### train_val_split
- use multiple data loaders for training data and SubsetRandomSampler to create train/val data (https://am207.github.io/2018spring/wiki/ValidationSplits.html)

- can use sklearn train_test_split for numpy data


### create early stopping condition in training

### create model checkpoint condition in training
-  Saving/loading model at the end of a specified epoch 
- https://stackoverflow.com/questions/42703500/best-way-to-save-a-trained-model-in-pytorch/43819235
- https://cs230-stanford.github.io/pytorch-getting-started.html#saving-and-loading-models
- can look at pytorch ignite (https://pytorch.org/ignite/index.html) for early stopping/model checkpoint

Alt approach: save model to a different output file after every x epochs (save only the last n models). Load latest model before overfitting and train for a few epochs, stopping just before overfitting

i.e. if (epoch + 1)%10 == 0 and (epoch + 1) >= some number:
        save model

https://www.programcreek.com/python/example/101175/torch.save


### Learning Rate annealing
- lr_finder()
- no need to create stopping condition during training. train over full epochs

### Freeze layers/blocks
https://medium.com/@14prakash/almost-any-image-classification-problem-using-pytorch-i-am-in-love-with-pytorch-26c7aa979ec4

Transfer learning tutorial: https://github.com/pytorch/tutorials/blob/master/beginner_source/transfer_learning_tutorial.py

- freezing individual layers:https://raberrytv.wordpress.com/2017/10/28/pytorch-freezing-weights-of-pre-trained-layers/
        - set param.requires_grad = True to unfreeze individual layers (gradual unfreezing of layers)
- freezing blocks of layers: https://discuss.pytorch.org/t/how-the-pytorch-freeze-network-in-some-layers-only-the-rest-of-the-training/7088/3?u=maxmatical
- freeze full model:  
        for param in model.parameters():
                param.requires_grad = False

### differential/discriminative learning rates
- https://pytorch.org/docs/master/optim.html#per-parameter-options

### adding/removing layers from pretrained models
- adding layers: https://discuss.pytorch.org/t/how-to-perform-finetuning-in-pytorch/419/12?u=maxmatical
- removing last layer: https://discuss.pytorch.org/t/remove-a-layer-from-inception-model/11472

# Completed

### create a way to internally evaluate validation loss during training
- done (cifar10 another version)
- note, training can be done more easily using fit(model, data, n_epochs, optimizer, loss_fn) from fast.ai


### using global(adaptive) average/max pooling to flatten conv layers
- https://discuss.pytorch.org/t/global-average-pooling-in-pytorch/6721/11
- https://discuss.pytorch.org/t/global-average-pooling-misunderstanding/18272


### Model initialization (done)
https://stackoverflow.com/questions/49433936/how-to-initialize-weights-in-pytorch
- https://discuss.pytorch.org/t/questions-about-global-average-pooling/20615

### multiple inputs/outputs (done)
https://discuss.pytorch.org/t/nn-module-with-multiple-inputs/237/3

### learnign rate scheduling
- cosine annealing
- cosine annealing with warm restarts (https://jsideas.net/python/2018/03/14/snapshot_ensemble.html)
- reduce LR on plateau (https://discuss.pytorch.org/t/problem-with-reducelronplateau/10499/2)'
        - when using LR scheduler (don't use optimizer.step)
- snapshot ensembles

