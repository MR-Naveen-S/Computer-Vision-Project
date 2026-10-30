import torch
import numpy as np


class LinearCKA:
    """
    Computes unbiased Linear Centered Kernel Alignment (CKA) between activation representations.

    CKA(K, L) = HSIC(K, L) / sqrt(HSIC(K, K) * HSIC(L, L))
    where K = X @ X.T and L = Y @ Y.T with centering matrix H = I - 1/n * 1 1^T.
    """

    def __init__(self, device=None):
        if device is None:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device(device)

    def _centering(self, K: torch.Tensor) -> torch.Tensor:
        """
        Applies double centering: H @ K @ H = (I - 1/n) K (I - 1/n)
        """
        n = K.shape[0]
        unit = torch.ones((n, n), device=self.device)
        I = torch.eye(n, device=self.device)
        H = I - unit / n
        return H @ K @ H

    def _hsic(self, A: torch.Tensor, B: torch.Tensor) -> torch.Tensor:
        """
        Computes Hilbert-Schmidt Independence Criterion between two representations.
        A: (N, D1), B: (N, D2)
        """
        K = A @ A.T
        L = B @ B.T
        K_c = self._centering(K)
        L_c = self._centering(L)
        return torch.sum(K_c * L_c)

    def compute(self, X: torch.Tensor, Y: torch.Tensor) -> float:
        """
        Computes Linear CKA between activation matrices X and Y.

        Args:
            X (torch.Tensor or np.ndarray): Activations matrix of shape [N, D1]
            Y (torch.Tensor or np.ndarray): Activations matrix of shape [N, D2]

        Returns:
            float: Linear CKA similarity score between 0.0 and 1.0
        """
        if isinstance(X, np.ndarray):
            X = torch.from_numpy(X)
        if isinstance(Y, np.ndarray):
            Y = torch.from_numpy(Y)

        X = X.to(self.device).float()
        Y = Y.to(self.device).float()

        # Center activations along batch dimension
        X = X - X.mean(dim=0, keepdim=True)
        Y = Y - Y.mean(dim=0, keepdim=True)

        hsic_xy = self._hsic(X, Y)
        hsic_xx = self._hsic(X, X)
        hsic_yy = self._hsic(Y, Y)

        denom = torch.sqrt(hsic_xx) * torch.sqrt(hsic_yy) + 1e-8
        similarity = hsic_xy / denom

        return float(torch.clamp(similarity, 0.0, 1.0).item())

    def compute_pairwise_matrix(self, dict_a: dict, dict_b: dict, layer_order: list) -> np.ndarray:
        """
        Computes full pairwise layer-by-layer CKA similarity matrix.

        Args:
            dict_a (dict): {layer_name: activation_tensor [N, D]}
            dict_b (dict): {layer_name: activation_tensor [N, D]}
            layer_order (list): List of layer names to evaluate in sequence

        Returns:
            np.ndarray: [len(layer_order), len(layer_order)] matrix of CKA values
        """
        n_layers = len(layer_order)
        matrix = np.zeros((n_layers, n_layers))

        for i, l_a in enumerate(layer_order):
            for j, l_b in enumerate(layer_order):
                act_a = dict_a[l_a]
                act_b = dict_b[l_b]
                matrix[i, j] = self.compute(act_a, act_b)

        return matrix
