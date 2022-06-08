## Kalman filter for one dimension

from numpy import product


def predict(mean0, var0, mean1, var1):
    new_mean = mean0 + mean1
    new_var = var0 + var1
    return [new_mean, new_var]

def update(mean0, var0, mean1, var1):
    sum_var = var0 + var1
    pr_s = mean0*var1 + mean1*var0
    new_mean = 1/(sum_var) * pr_s
    product_var = var0*var1
    new_var = product_var / sum_var
    return [new_mean, new_var]