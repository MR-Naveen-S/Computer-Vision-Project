import torch
import torch.nn as nn
from torchvision import models


def build_model(model_name: str, strategy: str, num_classes: int) -> nn.Module:
    """
    Builds a vision backbone configured with one of four transfer learning adaptation strategies.

    Args:
        model_name (str): 'resnet50', 'resnet18', 'efficientnet_b0', or 'mobilenet_v2'
        strategy (str): Adaptation strategy:
            - 'scratch': Random initialization, all layers trained end-to-end
            - 'feature_extraction': ImageNet pre-trained, backbone frozen, only classification head trained
            - 'partial_finetune': ImageNet pre-trained, initial stages frozen, final stage + head trained
            - 'full_finetune': ImageNet pre-trained, all layers trained end-to-end with differential LR
        num_classes (int): Number of target classes for the new classification task

    Returns:
        nn.Module: Configured PyTorch neural network model
    """
    model_name = model_name.lower().strip()
    valid_strategies = ["scratch", "feature_extraction", "partial_finetune", "full_finetune"]
    if strategy not in valid_strategies:
        raise ValueError(f"Unknown strategy: '{strategy}'. Supported: {valid_strategies}")

    weights = "DEFAULT" if strategy != "scratch" else None

    if model_name in ["resnet50", "resnet18"]:
        model_builder = models.resnet50 if model_name == "resnet50" else models.resnet18
        model = model_builder(weights=weights)
        in_features = model.fc.in_features
        model.fc = nn.Linear(in_features, num_classes)

        if strategy == "feature_extraction":
            for name, param in model.named_parameters():
                if "fc" not in name:
                    param.requires_grad = False

        elif strategy == "partial_finetune":
            # Freeze all stages except layer4 (deepest residual block) and fc
            for name, param in model.named_parameters():
                if "layer4" not in name and "fc" not in name:
                    param.requires_grad = False

    elif model_name == "efficientnet_b0":
        model = models.efficientnet_b0(weights=weights)
        in_features = model.classifier[1].in_features
        model.classifier[1] = nn.Linear(in_features, num_classes)

        if strategy == "feature_extraction":
            for name, param in model.features.named_parameters():
                param.requires_grad = False

        elif strategy == "partial_finetune":
            # Freeze features except final stages (blocks 6, 7, and 8)
            for name, param in model.features.named_parameters():
                if not any(block_id in name for block_id in ["6.", "7.", "8."]):
                    param.requires_grad = False

    elif model_name == "mobilenet_v2":
        model = models.mobilenet_v2(weights=weights)
        in_features = model.classifier[1].in_features
        model.classifier[1] = nn.Linear(in_features, num_classes)

        if strategy == "feature_extraction":
            for name, param in model.features.named_parameters():
                param.requires_grad = False

        elif strategy == "partial_finetune":
            # Freeze features except the final inverted residual blocks (stages 15+)
            for name, param in model.features.named_parameters():
                if not any(f"features.{i}." in name for i in range(15, 19)):
                    param.requires_grad = False

    else:
        raise ValueError(f"Unsupported model: '{model_name}'. Supported: 'resnet50', 'resnet18', 'efficientnet_b0', 'mobilenet_v2'")

    return model


def get_optimizer_param_groups(
    model: nn.Module,
    strategy: str,
    base_lr: float = 1e-3,
    backbone_lr: float = 1e-4,
    weight_decay: float = 1e-4,
):
    """
    Constructs optimizer parameter groups. For 'full_finetune', applies a differential learning
    rate (lower LR on pre-trained backbone, higher LR on task classification head) as specified
    in the research blueprint.
    """
    if strategy == "full_finetune":
        backbone_params = []
        head_params = []
        for name, param in model.named_parameters():
            if not param.requires_grad:
                continue
            if "fc" in name or "classifier" in name:
                head_params.append(param)
            else:
                backbone_params.append(param)

        param_groups = [
            {"params": backbone_params, "lr": backbone_lr, "weight_decay": weight_decay},
            {"params": head_params, "lr": base_lr, "weight_decay": weight_decay},
        ]
        return param_groups
    else:
        trainable = [p for p in model.parameters() if p.requires_grad]
        return [{"params": trainable, "lr": base_lr, "weight_decay": weight_decay}]


def get_model_param_stats(model: nn.Module):
    """
    Returns counts of total parameters and trainable parameters.
    """
    total = sum(p.numel() for p in model.parameters())
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    frozen = total - trainable
    return {
        "total_params": total,
        "trainable_params": trainable,
        "frozen_params": frozen,
        "trainable_percent": (trainable / total) * 100.0 if total > 0 else 0.0,
    }
