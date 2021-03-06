# -*- coding: utf-8 -*-
"""attention_augmented_convnets.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18Ae5yWgmC4MWImY1ogZxMZ9VZ3SIEItU
"""

import torch
import torch.nn as nn
import torch.nn.functional as F

use_cuda = torch.cuda.is_available()
device = torch.device("cuda" if use_cuda else "cpu")

class augmented_conv2d(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, dk, dv, Nh, relative, stride = 1, padding = 1, bias = False):
        super(augmented_conv2d, self).__init__()
    
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size
        self.dk = dk
        self.dv = dv
        self.Nh = Nh
        self.relative = relative
        self.stride = stride
        
        # Input has shape [bs, in_channels, H, W]
        self.conv_out = nn.Conv2d(self.in_channels, self.out_channels - self.dv, kernel_size = self.kernel_size, stride = self.stride, padding = 1)
        
        # used for compute_flat_qkv(inputs, dk,dv, Nh)
        self.qkv_conv = nn.Conv2d(self.in_channels, 2*self.dk+self.dv, kernel_size = self.kernel_size, stride = self.stride, padding = 1)
        
        # used for attn_out
        self.attn_out = nn.Conv2d(self.dv, self.dv, kernel_size = 1, stride = 1, padding = 0)
        
    def forward(self, x):
        # input is [Batch_size, in_channels, H, W]
        conv_out = self.conv_out(x) #output is [bs, out_channels, H, W]

        bs, _, H, W = conv_out.size() # compute sizes used in attn_out (reshaping)

        flat_q, flat_k, flat_v, q, k, v = self.compute_flat_qkv(x, self.dk, self.dv, self.Nh) #q, k, v will be used later
        # output dim for flat_q, flat_k, flat_v: [bs, Nh, H*W or H*dvh or H*dkh]
        # dvh = dv/Nh, dkh = dk/Nh
        # q k v has dim [bs, Nh, H, W or dv or dk for q/k/v]

        logits = torch.matmul(flat_q.transpose(2,3), flat_k)

        if self.relative:
            h_rel_logits, w_rel_logits = self.relative_logits(q)
            logits += h_rel_logits
            logits += w_rel_logits

        weights = F.softmax(logits, dim = -1) # output dim is [bs, Nh, H*W, dvh]

        attn_out = torch.matmul(weights, flat_v.transpose(2, 3))
        attn_out = torch.reshape(attn_out, (bs, self.Nh, self.dv//self.Nh, H, W))
        attn_out = self.combine_heads_2d(attn_out) #output dim is [bs, dv, H, W]
        attn_out = self.attn_out(attn_out)

        # concats the results from conv and attn
        return torch.cat((conv_out, attn_out), dim = 1)


    ###########################
    # helper functions:
    ###########################

    """
    helper functions used:

    compute_flat_qkv(self, dk, dv, Nh)

    relative_logits(self, q)

    combine_heads_2d(self, x)
    """

    def compute_flat_qkv(self, x, dk, dv, Nh):
        qkv = self.qkv_conv(x)
        N, _, H, W = qkv.size() # calculate size of tensor after the qkv_conv
        q, k, v = torch.split(qkv, [dk, dk, dv], dim = 1)
        q = self.split_heads_2d(q, Nh)
        k = self.split_heads_2d(k, Nh)
        v = self.split_heads_2d(v, Nh)

        dkh = dk//Nh
        q *= dkh**(-0.5)
        flat_q = torch.reshape(q, (N, Nh, dk // Nh, H*W))
        flat_k = torch.reshape(k, (N, Nh, dk // Nh, H*W))
        flat_v = torch.reshape(v, (N, Nh, dv // Nh, H*W))
        return flat_q, flat_k, flat_v, q, k, v

    def split_heads_2d(self, x, Nh):
        bs, n_channels, H, W = x.size()
        split = torch.reshape(x, (bs, Nh, n_channels // Nh, H, W))
        return split

    def combine_heads_2d(self, x):
        bs, Nh, dv, H, W = x.size()
        return torch.reshape(x, (bs, Nh * dv, H, W))

    def relative_logits(self, q):
        """
        Compute relative position logits.
        [bs, Nh, dk, H, W]

        """

        bs, Nh, dk, H, W = q.size()
        q = torch.transpose(q, 2, 4).transpose(2, 3)
        key_rel_w = nn.Parameter(torch.randn((2 * W - 1, dk), requires_grad=True)).to(device)
        rel_logits_w = self.relative_logits_1d(q, key_rel_w, H, W, Nh, "w")

        key_rel_h = nn.Parameter(torch.randn((2 * H - 1, dk), requires_grad=True)).to(device)
        rel_logits_h = self.relative_logits_1d(torch.transpose(q, 2, 3), key_rel_h, W, H, Nh, "h")

        return rel_logits_h, rel_logits_w

    def relative_logits_1d(self, q, rel_k, H, W, Nh, case):
        """

        Compute relative logits along one dimension.
        [bs, Nh,H, W, 2*W-1]

        """
        rel_logits = torch.einsum('bhxyd,md->bhxym', q, rel_k)
        rel_logits = torch.reshape(rel_logits, (-1, Nh * H, W, 2 * W - 1))
        rel_logits = self.rel_to_abs(rel_logits)

        rel_logits = torch.reshape(rel_logits, (-1, Nh, H, W, W))
        rel_logits = torch.unsqueeze(rel_logits, dim=3)
        rel_logits = rel_logits.repeat((1, 1, 1, H, 1, 1))

        if case == "w":
            rel_logits = torch.transpose(rel_logits, 3, 4)
        elif case == "h":
            rel_logits = torch.transpose(rel_logits, 2, 4).transpose(4, 5).transpose(3, 5)
        rel_logits = torch.reshape(rel_logits, (-1, Nh, H * W, H * W))
        return rel_logits

    def rel_to_abs(self, x):
        bs, Nh, L, _ = x.size()

        col_pad = torch.zeros((bs, Nh, L, 1)).to(device)
        x = torch.cat((x, col_pad), dim=3)

        flat_x = torch.reshape(x, (bs, Nh, L * 2 * L))
        flat_pad = torch.zeros((bs, Nh, L - 1)).to(device)
        flat_x_padded = torch.cat((flat_x, flat_pad), dim=2)

        final_x = torch.reshape(flat_x_padded, (bs, Nh, L + 1, 2 * L - 1))
        final_x = final_x[:, :, :L, L - 1:]
        return final_x

# tests if implemented correctly

# tmp = torch.randn((16, 3, 32, 32)).to(device)
# a = augmented_conv2d(3, 20, kernel_size=3, dk=40, dv=4, Nh=2, relative=True).to(device)
# print(a(tmp).shape)
# bs, n_channels, H, W = a(tmp).size()
# print(H, W, H*W)

