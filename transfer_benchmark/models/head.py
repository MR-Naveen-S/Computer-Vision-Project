import torch
import torch.nn as nn


class ClassificationHead(nn.Module):
    """
    Standardized classification head for deep CNN backbones.
    Provides standard linear or dropout-regularized classification projection.

    Args:
        in_features (int): Dimensionality of input feature embedding
        num_classes (int): Number of target task classes
        dropout_rate (float): Dropout probability for regularization (default: 0.2)
        hidden_dim (int, optional): Hidden layer dimension for MLP head (default: None, linear)
    """

    def __init__(
        self,
        in_features: int,
        num_classes: int,
        dropout_rate: float = 0.2,
        hidden_dim: int = None,
    ):
        super().__init__()
        self.in_features = in_features
        self.num_classes = num_classes

        if hidden_dim is not None:
            self.head = nn.Sequential(
                nn.Dropout(p=dropout_rate),
                nn.Linear(in_features, hidden_dim),
                nn.ReLU(inplace=True),
                nn.Dropout(p=dropout_rate),
                nn.Linear(hidden_dim, num_classes),
            )
        else:
            if dropout_rate > 0:
                self.head = nn.Sequential(
                    nn.Dropout(p=dropout_rate),
                    nn.Linear(in_features, num_classes),
                )
            else:
                self.head = nn.Linear(in_features, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.head(x)
