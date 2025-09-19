import math

import numpy as np


def cos_inf_schedule(n_iterations, n_warmup, div_factor, final_div_factor, n_inf):
    """Cosine annealing with warmup and _constant_ final_lr after cycle ended.
    Args:
        n_iterations: total number of iterations
        n_warmup: number of warmup iterations
        div_factor: initial division factor for warmup
        final_div_factor: final division factor for final lr
        n_inf: number of iterations for the final lr (constant lr after cycle ended)
    Returns:
        schedule: a function that takes the current iteration and
        returns the multiplicative factor for the learning rate
    """
    max_lr = 1.0
    base_lr = max_lr / div_factor
    final_lr = base_lr / final_div_factor

    n_anneal_steps = n_iterations - n_inf

    def schedule(step):
        if step < n_warmup:
            return (step / n_warmup) + (1 - step / n_warmup) / div_factor
        elif step < n_anneal_steps:
            t = (step - n_warmup) / (n_anneal_steps - n_warmup)
            lr = final_lr + 0.5 * (max_lr - final_lr) * (1 + np.cos(np.pi * t))
            return lr
        else:
            return final_lr

    return schedule


def wsd_schedule(
    n_iterations,
    final_lr_factor=0.0,
    n_warmup=1000,
    init_div_factor=100,
    fract_decay=0.1,
    decay_type="linear",
):
    """Warmup, hold, and decay schedule.
    Args:
        n_iterations: total number of iterations
        final_lr_factor: factor by which to reduce max_lr at the end
        warmup_fract: fraction of iterations used for warmup
        init_div_factor: initial division factor for warmup
        fract_decay: fraction of iterations used for decay
    Returns:
        schedule: a function that takes the current iteration and
        returns the multiplicative factor for the learning rate
    """
    n_anneal_steps = int(fract_decay * n_iterations)
    n_hold = n_iterations - n_anneal_steps

    def schedule(step):
        if step < n_warmup:
            return (step / n_warmup) + (1 - step / n_warmup) / init_div_factor
        elif step < n_hold:
            return 1.0
        elif step < n_iterations:
            if decay_type == "linear":
                return final_lr_factor + (1 - final_lr_factor) * (
                    1 - (step - n_hold) / n_anneal_steps
                )
            elif decay_type == "exp":
                return final_lr_factor ** ((step - n_hold) / n_anneal_steps)
            elif decay_type == "cosine":
                return (
                    final_lr_factor
                    + (1 - final_lr_factor)
                    * (1 + math.cos(math.pi * (step - n_hold) / n_anneal_steps))
                    * 0.5
                )
            elif decay_type == "miror_cosine":
                cosine_value = (
                    final_lr_factor
                    + (1 - final_lr_factor)
                    * (1 + math.cos(math.pi * (step - n_hold) / n_anneal_steps))
                    * 0.5
                )
                linear_value = final_lr_factor + (1 - final_lr_factor) * (
                    1 - (step - n_hold) / n_anneal_steps
                )
                return linear_value * 2 - cosine_value
            elif decay_type == "square":
                return final_lr_factor + (1 - final_lr_factor) * (
                    1 - ((step - n_hold) / n_anneal_steps) ** 2
                )

            elif decay_type == "sqrt":
                return final_lr_factor + (1 - final_lr_factor) * (
                    1 - math.sqrt((step - n_hold) / n_anneal_steps)
                )

            else:
                raise ValueError(
                    f"decay type {decay_type} is not in ['cosine','miror_cosine','linear','exp','square','sqrt']"
                )

        else:
            return final_lr_factor

    return schedule
