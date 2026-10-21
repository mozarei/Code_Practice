import torch

w = torch.tensor([1.0, 2.0, 3.0])
snapshot = w.detach()

print(w.data_ptr())
print(snapshot.data_ptr())
# 43401562240
# 43401562240

w[0] = 99.0

print(w)
print(snapshot)