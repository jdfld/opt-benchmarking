#!/bin/bash

torchrun --nproc_per_node=1 ./src/main.py --config_format base --model llama --distributed_backend nccl \
    --n_embd 2048 --n_head 16 --n_layer 12 \
    --batch_size 62 --sequence_length 512 --acc_steps 32 \
    --dataset fineweb --iterations 48000 \
    --dropout 0.0 --warmup_steps 2000 --grad_clip 0.1 --seed 0 \
    --opt ademamix --lr 1e-3 --weight_decay 0.1 --scheduler cos \
    --beta1 0.9 --beta2 0.999 \
    --adema_beta3 0.999 --adema_alpha 8.0 \
    --adema_beta3_warmup 48000 --adema_alpha_warmup 48000 \
    --wandb --wandb_project YOUR_WANDB-PROJECT --wandb_entity YOUR-WANDB-ENTITY \
    --eval_interval 200 --permanent_ckpt_interval 2000 \