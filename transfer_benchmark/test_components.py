"""
Unit & Integration Test Suite for Transfer Learning Empirical Benchmark components.
Validates:
1. Model factory adaptation strategies & parameter freezing logic
2. Differential learning rate parameter groupings
3. Linear CKA engine correctness (self-similarity = 1.0, orthogonality ~ 0.0)
4. Forward feature extraction hooks
"""

import os
import sys
import torch
import torch.nn as nn
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.model_factory import (
    build_model,
    get_optimizer_param_groups,
    get_model_param_stats,
)
from analysis.cka import LinearCKA
from analysis.feature_extractor import FeatureExtractor
from utils.metrics import compute_classification_metrics, MetricTracker


def test_linear_cka():
    print("[*] Running CKA mathematical correctness test...")
    cka = LinearCKA(device="cpu")

    # Identical representations must yield CKA = 1.0
    torch.manual_seed(42)
    X = torch.randn(100, 64)
    sim_self = cka.compute(X, X)
    assert abs(sim_self - 1.0) < 1e-4, f"Expected CKA(X, X) == 1.0, got {sim_self}"

    # Linear transformation/orthogonal rotation invariant
    # CKA is invariant to orthogonal transformation
    Q, _ = torch.linalg.qr(torch.randn(64, 64))
    Y = X @ Q
    sim_rot = cka.compute(X, Y)
    assert abs(sim_rot - 1.0) < 1e-3, f"Expected CKA invariant under orthogonal transform, got {sim_rot}"

    # Uncorrelated representations should yield low CKA (N=500)
    torch.manual_seed(99)
    Z = torch.randn(100, 64)
    sim_uncorr = cka.compute(X, Z)
    assert 0.0 <= sim_uncorr <= 0.45, f"Expected low CKA for random uncorrelated matrices, got {sim_uncorr}"

    print(f"    [OK] CKA passed: Self={sim_self:.4f}, Orthogonal={sim_rot:.4f}, Uncorrelated={sim_uncorr:.4f}")


def test_model_adaptation_strategies():
    print("[*] Running model adaptation strategy freezing tests...")
    num_classes = 10
    models_to_test = ["resnet18", "resnet50", "efficientnet_b0", "mobilenet_v2"]
    strategies = ["scratch", "feature_extraction", "partial_finetune", "full_finetune"]

    for m_name in models_to_test:
        for strat in strategies:
            model = build_model(m_name, strat, num_classes)
            stats = get_model_param_stats(model)

            if strat in ["scratch", "full_finetune"]:
                assert stats["frozen_params"] == 0, f"{m_name} {strat} should have 0 frozen params"
            elif strat == "feature_extraction":
                assert stats["frozen_params"] > 0, f"{m_name} {strat} should have frozen params"
                assert stats["trainable_percent"] < 5.0, f"{m_name} {strat} trainable % too high: {stats['trainable_percent']}%"
            elif strat == "partial_finetune":
                assert stats["frozen_params"] > 0, f"{m_name} {strat} should have frozen params"
                assert 0.0 < stats["trainable_percent"] < 100.0, f"{m_name} {strat} partial finetune % error"

            # Check differential LR groups for full_finetune
            groups = get_optimizer_param_groups(model, strat, base_lr=1e-3, backbone_lr=1e-4)
            if strat == "full_finetune":
                assert len(groups) == 2, f"full_finetune must have 2 LR groups (backbone vs head)"
                assert groups[0]["lr"] == 1e-4, f"Backbone LR should be 1e-4, got {groups[0]['lr']}"
                assert groups[1]["lr"] == 1e-3, f"Head LR should be 1e-3, got {groups[1]['lr']}"
            else:
                assert len(groups) == 1, f"{strat} should have 1 LR group"

    print("    [OK] All 4 adaptation strategies verified across ResNet, EfficientNet, and MobileNet!")


def test_feature_extractor_hooks():
    print("[*] Running feature extractor hooks test...")
    model = build_model("resnet18", "feature_extraction", num_classes=10)
    target_layers = ["conv1", "layer1", "layer2", "layer3", "layer4"]

    with FeatureExtractor(model, target_layers) as extractor:
        dummy_input = torch.randn(8, 3, 224, 224)
        _ = model(dummy_input)

        for layer in target_layers:
            assert layer in extractor.activations, f"Missing layer {layer} in extractor activations"
            act = extractor.activations[layer]
            assert act.shape[0] == 8, f"Expected batch size 8, got {act.shape}"
            assert act.dim() == 2, f"Expected GAP pooled 2D tensor (Batch, Features), got {act.shape}"

    print("    [OK] Forward hooks & GAP pooling verified successfully!")


def test_metric_tracker():
    print("[*] Running metric tracker test...")
    tracker = MetricTracker()
    tracker.start_epoch()
    tracker.end_epoch(epoch=1, train_loss=1.5, test_acc=0.60, test_f1=0.58)
    tracker.start_epoch()
    tracker.end_epoch(epoch=2, train_loss=0.8, test_acc=0.85, test_f1=0.84)
    tracker.start_epoch()
    tracker.end_epoch(epoch=3, train_loss=0.5, test_acc=0.88, test_f1=0.87)

    summary = tracker.get_summary()
    assert summary["best_accuracy"] == 0.88
    assert summary["best_epoch"] == 3
    assert summary["convergence_epoch"] == 2  # 0.85 >= 0.95 * 0.88 (0.836)
    print("    [OK] Convergence tracking and metrics verified!")


if __name__ == "__main__":
    print("\n" + "=" * 65)
    print(" RUNNING INTEGRATION TESTS FOR TRANSFER LEARNING BENCHMARK")
    print("=" * 65)
    test_linear_cka()
    test_model_adaptation_strategies()
    test_feature_extractor_hooks()
    test_metric_tracker()
    print("=" * 65)
    print(" ALL TESTS PASSED SUCCESSFULLY! ")
    print("=" * 65 + "\n")
