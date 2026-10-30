import time
import numpy as np
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score


def compute_classification_metrics(y_true, y_pred):
    """
    Computes standard evaluation metrics: Top-1 Accuracy, Weighted F1, Macro F1.

    Args:
        y_true (array-like): Ground truth class labels
        y_pred (array-like): Predicted class labels

    Returns:
        dict: Computed metric values
    """
    y_true = np.asarray(y_true).ravel()
    y_pred = np.asarray(y_pred).ravel()

    acc = float(accuracy_score(y_true, y_pred))
    f1_weighted = float(f1_score(y_true, y_pred, average="weighted", zero_division=0))
    f1_macro = float(f1_score(y_true, y_pred, average="macro", zero_division=0))
    precision_weighted = float(precision_score(y_true, y_pred, average="weighted", zero_division=0))
    recall_weighted = float(recall_score(y_true, y_pred, average="weighted", zero_division=0))

    return {
        "accuracy": acc,
        "f1_weighted": f1_weighted,
        "f1_macro": f1_macro,
        "precision_weighted": precision_weighted,
        "recall_weighted": recall_weighted,
    }


class MetricTracker:
    """
    Tracks training dynamics, convergence velocity, and per-epoch metrics.
    """

    def __init__(self):
        self.history = []
        self.epoch_start_time = None
        self.run_start_time = time.time()

    def start_epoch(self):
        self.epoch_start_time = time.time()

    def end_epoch(self, epoch: int, train_loss: float, test_acc: float, test_f1: float):
        elapsed = time.time() - (self.epoch_start_time if self.epoch_start_time else time.time())
        record = {
            "epoch": epoch,
            "train_loss": float(train_loss),
            "test_accuracy": float(test_acc),
            "test_f1": float(test_f1),
            "epoch_duration_sec": float(elapsed),
        }
        self.history.append(record)
        return record

    def get_summary(self):
        """
        Calculates best metrics and time-to-convergence.
        Convergence criterion: Epoch where accuracy reaches >= 95% of peak accuracy.
        """
        if not self.history:
            return {}

        accuracies = [h["test_accuracy"] for h in self.history]
        best_acc = max(accuracies)
        best_epoch = accuracies.index(best_acc)
        best_f1 = self.history[best_epoch]["test_f1"]

        threshold = 0.95 * best_acc
        convergence_epoch = None
        time_to_convergence = None

        cumulative_time = 0.0
        for h in self.history:
            cumulative_time += h["epoch_duration_sec"]
            if convergence_epoch is None and h["test_accuracy"] >= threshold:
                convergence_epoch = h["epoch"]
                time_to_convergence = cumulative_time

        total_time = sum(h["epoch_duration_sec"] for h in self.history)
        avg_epoch_time = total_time / len(self.history) if self.history else 0.0

        return {
            "best_accuracy": best_acc,
            "best_f1": best_f1,
            "best_epoch": best_epoch + 1,
            "total_train_time_sec": total_time,
            "avg_epoch_time_sec": avg_epoch_time,
            "convergence_epoch": convergence_epoch,
            "time_to_convergence_sec": time_to_convergence,
        }
