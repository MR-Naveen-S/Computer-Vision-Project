import torch
import torch.nn as nn
from typing import List, Dict


class FeatureExtractor:
    """
    Extracts intermediate layer activations from PyTorch models via forward hooks.
    Applies Global Average Pooling on convolutional feature maps to standardize
    representations to [Batch_Size, Channel_Dimension].
    """

    def __init__(self, model: nn.Module, target_layers: List[str]):
        self.model = model
        self.target_layers = target_layers
        self.activations: Dict[str, torch.Tensor] = {}
        self.hooks = []
        self._register_hooks()

    def _register_hooks(self):
        matched = set()
        for name, module in self.model.named_modules():
            if name in self.target_layers:
                hook = module.register_forward_hook(self._get_hook(name))
                self.hooks.append(hook)
                matched.add(name)

        missing = set(self.target_layers) - matched
        if missing:
            print(f"[!] Warning: Target layers not found in model: {missing}")

    def _get_hook(self, name: str):
        def hook(module, input, output):
            # Global Average Pooling on conv activation maps: (B, C, H, W) -> (B, C)
            if output.dim() == 4:
                pooled = torch.mean(output, dim=[2, 3])
            elif output.dim() == 3:
                pooled = torch.mean(output, dim=1)
            else:
                pooled = output
            self.activations[name] = pooled.detach().cpu()
        return hook

    def extract_dataset_features(
        self, loader, max_samples: int = 1000, device: torch.device = None
    ) -> Dict[str, torch.Tensor]:
        """
        Runs forward pass over data loader up to max_samples, concatenating layer activations.

        Args:
            loader: PyTorch DataLoader
            max_samples: Target number of samples to accumulate (e.g. 1000)
            device: torch.device to run model on

        Returns:
            dict: {layer_name: Tensor of shape [N, Features]}
        """
        if device is None:
            device = next(self.model.parameters()).device

        self.model.eval()
        accumulated: Dict[str, List[torch.Tensor]] = {l: [] for l in self.target_layers}
        total_samples = 0

        with torch.no_grad():
            for images, _ in loader:
                batch_size = images.size(0)
                images = images.to(device)

                _ = self.model(images)

                for layer in self.target_layers:
                    if layer in self.activations:
                        accumulated[layer].append(self.activations[layer])

                total_samples += batch_size
                if total_samples >= max_samples:
                    break

        concatenated = {}
        for layer in self.target_layers:
            if accumulated[layer]:
                cat_tensor = torch.cat(accumulated[layer], dim=0)
                concatenated[layer] = cat_tensor[:max_samples]

        return concatenated

    def remove_hooks(self):
        for h in self.hooks:
            h.remove()
        self.hooks.clear()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.remove_hooks()
