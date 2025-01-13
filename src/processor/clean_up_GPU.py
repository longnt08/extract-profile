import gc
import torch

gc.collect()
if torch.cuda.is_available():
    torch.cuda.empty_cache()
    