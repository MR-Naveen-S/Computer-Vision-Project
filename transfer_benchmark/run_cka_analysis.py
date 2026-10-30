import os
import sys
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import torch
from torchvision import models

# Ensure local imports work whether run from transfer_benchmark/ or root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.dataset_loader import get_dataloaders
from models.model_factory import build_model
from analysis.cka import LinearCKA
from analysis.feature_extractor import FeatureExtractor
from utils.plotting import set_plot_style, plot_cka_heatmap


def get_calibration_loader(dataset_name: str, n_samples: int = 1000, batch_size: int = 64, data_cache: str = "./data_cache"):
    """
    Creates a fixed, deterministic calibration DataLoader of exactly n_samples.
    """
    _, test_loader, num_classes = get_dataloaders(
        dataset_name=dataset_name,
        batch_size=batch_size,
        data_cache=data_cache,
        max_test_samples=n_samples,
        seed=12345,
    )
    return test_loader, num_classes


def run_cka_layer_diagnosis(
    dataset_name: str = "cifar10",
    model_name: str = "resnet50",
    n_calibration: int = 1000,
    checkpoints_dir: str = "./results/checkpoints",
    results_dir: str = "./results",
    device: torch.device = None,
):
    """
    Performs layer-wise Linear CKA representation drift analysis for ResNet-50 comparing:
      1. Pretrained ImageNet Baseline vs Full Fine-Tuned Model
      2. Pretrained ImageNet Baseline vs Model Trained from Scratch
    """
    if device is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    print(f"\n{'='*75}")
    print(f"[*] RUNNING CKA REPRESENTATION DRIFT ANALYSIS")
    print(f"[*] Dataset: {dataset_name.upper()} | Model: {model_name} | Calibration N: {n_calibration}")
    print(f"[*] Device: {device}")
    print(f"{'='*75}\n")

    loader, num_classes = get_calibration_loader(
        dataset_name=dataset_name,
        n_samples=n_calibration,
        batch_size=64,
    )

    target_layers = ["conv1", "layer1", "layer2", "layer3", "layer4"]

    # 1. Instantiate Pretrained Baseline Model
    print("[*] Instantiating Baseline Pre-trained ImageNet Model...")
    baseline_model = build_model(model_name, strategy="feature_extraction", num_classes=num_classes).to(device)

    # 2. Instantiate or Load Full Fine-Tuned Model
    print("[*] Instantiating / Loading Full Fine-Tuned Model...")
    finetune_model = build_model(model_name, strategy="full_finetune", num_classes=num_classes).to(device)
    ft_ckpt = os.path.join(checkpoints_dir, f"{dataset_name}_{model_name}_full_finetune_best.pt")
    if os.path.exists(ft_ckpt):
        print(f"    [+] Loading weights from {ft_ckpt}")
        ckpt_data = torch.load(ft_ckpt, map_location=device)
        finetune_model.load_state_dict(ckpt_data["state_dict"])
    else:
        print(f"    [!] Note: No checkpoint found at {ft_ckpt}. Using initialized model for CKA demonstration.")

    # 3. Instantiate or Load Model Trained From Scratch
    print("[*] Instantiating / Loading Scratch Model...")
    scratch_model = build_model(model_name, strategy="scratch", num_classes=num_classes).to(device)
    scratch_ckpt = os.path.join(checkpoints_dir, f"{dataset_name}_{model_name}_scratch_best.pt")
    if os.path.exists(scratch_ckpt):
        print(f"    [+] Loading weights from {scratch_ckpt}")
        ckpt_data = torch.load(scratch_ckpt, map_location=device)
        scratch_model.load_state_dict(ckpt_data["state_dict"])
    else:
        print(f"    [!] Note: No checkpoint found at {scratch_ckpt}. Using initialized scratch model.")

    # Extract Activations
    print(f"[*] Extracting activations across layers {target_layers} for {n_calibration} samples...")
    with FeatureExtractor(baseline_model, target_layers) as ext_base:
        acts_base = ext_base.extract_dataset_features(loader, max_samples=n_calibration, device=device)

    with FeatureExtractor(finetune_model, target_layers) as ext_ft:
        acts_ft = ext_ft.extract_dataset_features(loader, max_samples=n_calibration, device=device)

    with FeatureExtractor(scratch_model, target_layers) as ext_scratch:
        acts_scratch = ext_scratch.extract_dataset_features(loader, max_samples=n_calibration, device=device)

    # Compute CKA Matrices
    cka_engine = LinearCKA(device=device)

    print("[*] Computing Pretrained vs Full Fine-Tuned CKA Matrix...")
    matrix_base_vs_ft = cka_engine.compute_pairwise_matrix(acts_base, acts_ft, target_layers)

    print("[*] Computing Pretrained vs Scratch CKA Matrix...")
    matrix_base_vs_scratch = cka_engine.compute_pairwise_matrix(acts_base, acts_scratch, target_layers)

    # Save Heatmaps
    os.makedirs(results_dir, exist_ok=True)
    domain_label = "Near-Domain (Natural)" if "cifar" in dataset_name.lower() else "Far-Domain (Histopathology)"

    ft_heatmap_path = os.path.join(results_dir, f"cka_{dataset_name}_pretrained_vs_finetuned.png")
    plot_cka_heatmap(
        matrix_base_vs_ft,
        target_layers,
        title=f"Linear CKA: Pretrained ImageNet vs Full Fine-Tuned ({dataset_name.upper()})",
        subtitle=f"Domain: {domain_label} | Backbone: {model_name.upper()}",
        save_path=ft_heatmap_path,
        cmap="magma",
    )

    scratch_heatmap_path = os.path.join(results_dir, f"cka_{dataset_name}_pretrained_vs_scratch.png")
    plot_cka_heatmap(
        matrix_base_vs_scratch,
        target_layers,
        title=f"Linear CKA: Pretrained ImageNet vs Scratch ({dataset_name.upper()})",
        subtitle=f"Domain: {domain_label} | Backbone: {model_name.upper()}",
        save_path=scratch_heatmap_path,
        cmap="viridis",
    )

    # Save combined side-by-side heatmap if needed
    combined_heatmap_path = os.path.join(results_dir, f"cka_{dataset_name}_combined_heatmap.png")
    set_plot_style()
    fig, axes = plt.subplots(1, 2, figsize=(16, 6.5), dpi=300)

    sns.heatmap(
        matrix_base_vs_ft,
        xticklabels=target_layers,
        yticklabels=target_layers,
        vmin=0.0,
        vmax=1.0,
        cmap="magma",
        annot=True,
        fmt=".2f",
        square=True,
        ax=axes[0],
        linewidths=0.5,
    )
    axes[0].set_title(f"Pretrained ImageNet vs Fine-Tuned\n({dataset_name.upper()} - {domain_label})", fontweight="bold")
    axes[0].set_xlabel("Fine-Tuned Layers")
    axes[0].set_ylabel("Pretrained Layers")

    sns.heatmap(
        matrix_base_vs_scratch,
        xticklabels=target_layers,
        yticklabels=target_layers,
        vmin=0.0,
        vmax=1.0,
        cmap="viridis",
        annot=True,
        fmt=".2f",
        square=True,
        ax=axes[1],
        linewidths=0.5,
    )
    axes[1].set_title(f"Pretrained ImageNet vs Scratch\n({dataset_name.upper()} - {domain_label})", fontweight="bold")
    axes[1].set_xlabel("Scratch Layers")
    axes[1].set_ylabel("Pretrained Layers")

    plt.suptitle(f"Layer-by-Layer Representational Drift Analysis: {dataset_name.upper()}", fontsize=15, fontweight="bold")
    plt.tight_layout()
    plt.savefig(combined_heatmap_path, bbox_inches="tight")
    plt.close()

    # Diagonal layer alignment
    diag_ft = [matrix_base_vs_ft[i, i] for i in range(len(target_layers))]
    diag_scratch = [matrix_base_vs_scratch[i, i] for i in range(len(target_layers))]

    print(f"\n[+] Layer-wise Diagonal CKA Alignment for {dataset_name.upper()}:")
    for idx, lyr in enumerate(target_layers):
        print(f"    - Layer {lyr:7s}: Pretrained vs Fine-Tuned = {diag_ft[idx]:.3f} | Pretrained vs Scratch = {diag_scratch[idx]:.3f}")

    return {
        "dataset": dataset_name,
        "layers": target_layers,
        "matrix_base_vs_ft": matrix_base_vs_ft.tolist(),
        "matrix_base_vs_scratch": matrix_base_vs_scratch.tolist(),
        "diag_ft": diag_ft,
        "diag_scratch": diag_scratch,
    }


def compare_domain_drift(cifar_results: dict, pathmnist_results: dict, save_path: str = "./results/cka_drift_comparison.png"):
    """
    Plots the diagonal CKA layer similarity comparing Near-Domain (CIFAR-10) vs Far-Domain (PathMNIST).
    Visualizes how representational drift increases in deeper layers when transferring to far domains.
    """
    set_plot_style()
    layers = cifar_results["layers"]

    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
    x = np.arange(len(layers))

    ax.plot(x, cifar_results["diag_ft"], marker="o", linewidth=2.5, color="#2ecc71", label="CIFAR-10 (Near-Domain: Pretrained vs Fine-Tuned)")
    ax.plot(x, pathmnist_results["diag_ft"], marker="s", linewidth=2.5, color="#e67e22", label="PathMNIST (Far-Domain: Pretrained vs Fine-Tuned)")
    ax.plot(x, cifar_results["diag_scratch"], marker="^", linestyle="--", color="#95a5a6", label="Pretrained vs Scratch Baseline")

    ax.set_xticks(x)
    ax.set_xticklabels(layers)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("Layer Depth (Early $\\rightarrow$ Deep)", labelpad=10)
    ax.set_ylabel("Linear CKA Similarity", labelpad=10)
    ax.set_title("Representational Drift Across Layers: Near-Domain vs Far-Domain", fontweight="bold", pad=15)
    ax.legend(loc="lower left")

    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    print(f"[*] Multi-domain drift comparison saved to: {save_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Linear CKA Representation Drift Diagnostic Runner")
    parser.add_argument("--dataset", type=str, default="all", help="Dataset: 'cifar10', 'pathmnist', or 'all'")
    parser.add_argument("--model", type=str, default="resnet50", help="Model: 'resnet50' or 'resnet18'")
    parser.add_argument("--samples", type=int, default=1000, help="Number of calibration samples")
    parser.add_argument("--results_dir", type=str, default="./results", help="Directory where results are saved")
    parser.add_argument("--checkpoints_dir", type=str, default="./results/checkpoints", help="Directory containing model checkpoints")
    parser.add_argument("--device", type=str, default="auto", help="Device to compute CKA on")

    args = parser.parse_args()
    device = torch.device("cuda" if torch.cuda.is_available() and args.device != "cpu" else "cpu") if args.device == "auto" else torch.device(args.device)

    if args.dataset in ["cifar10", "all"]:
        cifar_res = run_cka_layer_diagnosis(
            dataset_name="cifar10",
            model_name=args.model,
            n_calibration=args.samples,
            checkpoints_dir=args.checkpoints_dir,
            results_dir=args.results_dir,
            device=device,
        )

    if args.dataset in ["pathmnist", "all"]:
        path_res = run_cka_layer_diagnosis(
            dataset_name="pathmnist",
            model_name=args.model,
            n_calibration=args.samples,
            checkpoints_dir=args.checkpoints_dir,
            results_dir=args.results_dir,
            device=device,
        )

    if args.dataset == "all":
        compare_domain_drift(cifar_res, path_res, save_path=os.path.join(args.results_dir, "cka_drift_comparison.png"))
        # Also copy / save as standard cka_heatmap.png as required by blueprint
        import shutil
        cifar_hm = os.path.join(args.results_dir, "cka_cifar10_pretrained_vs_finetuned.png")
        std_hm = os.path.join(args.results_dir, "cka_heatmap.png")
        if os.path.exists(cifar_hm):
            shutil.copy(cifar_hm, std_hm)
            print(f"[*] Standard {std_hm} generated successfully.")
