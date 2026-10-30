import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


def set_plot_style():
    sns.set_theme(style="whitegrid", font="sans-serif")
    plt.rcParams.update({
        "font.size": 11,
        "axes.labelsize": 12,
        "axes.titlesize": 13,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "figure.titlesize": 14,
    })


def plot_cka_heatmap(
    matrix: np.ndarray,
    layer_names: list,
    title: str = "Linear CKA Layer-wise Representation Similarity",
    subtitle: str = None,
    save_path: str = "./results/cka_heatmap.png",
    cmap: str = "viridis",
):
    """
    Plots a standardized, publication-ready CKA similarity heatmap.
    """
    set_plot_style()
    os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 6.5), dpi=300)
    sns.heatmap(
        matrix,
        xticklabels=layer_names,
        yticklabels=layer_names,
        vmin=0.0,
        vmax=1.0,
        cmap=cmap,
        annot=True,
        fmt=".2f",
        cbar_kws={"label": "Linear CKA Similarity"},
        square=True,
        ax=ax,
        linewidths=0.5,
    )

    ax.set_title(title, pad=15, fontweight="bold")
    if subtitle:
        ax.text(
            0.5,
            1.02,
            subtitle,
            horizontalalignment="center",
            verticalalignment="bottom",
            transform=ax.transAxes,
            fontsize=10,
            color="#555555",
        )
    ax.set_xlabel("Target Layer Representations", labelpad=10)
    ax.set_ylabel("Source Layer Representations", labelpad=10)

    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    print(f"[*] CKA Heatmap saved to: {save_path}")


def plot_comparative_bar_charts(results_df: pd.DataFrame, save_dir: str = "./results"):
    """
    Plots comparative bar charts across (2 domains × 3 models × 4 strategies).
    """
    set_plot_style()
    os.makedirs(save_dir, exist_ok=True)

    strategy_order = ["scratch", "feature_extraction", "partial_finetune", "full_finetune"]
    palette = {
        "scratch": "#e74c3c",             # Red: Scratch baseline
        "feature_extraction": "#3498db",  # Blue: Frozen backbone
        "partial_finetune": "#9b59b6",    # Purple: Partial adaptation
        "full_finetune": "#2ecc71",       # Green: Full fine-tuning
    }

    # 1. Accuracy comparison across Datasets & Backbones
    fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=True, dpi=300)
    datasets = results_df["dataset"].unique()

    for idx, d_name in enumerate(datasets):
        ax = axes[idx]
        sub_df = results_df[results_df["dataset"] == d_name]
        sns.barplot(
            data=sub_df,
            x="model",
            y="best_accuracy",
            hue="strategy",
            hue_order=[s for s in strategy_order if s in sub_df["strategy"].unique()],
            palette=palette,
            ax=ax,
        )
        domain_label = "Near-Domain (Natural Photos)" if "cifar" in d_name.lower() else "Far-Domain (Histopathology)"
        ax.set_title(f"Dataset: {d_name.upper()} ({domain_label})", fontweight="bold")
        ax.set_xlabel("Backbone Architecture")
        ax.set_ylabel("Top-1 Accuracy" if idx == 0 else "")
        ax.set_ylim(0, 1.05)
        ax.legend(title="Adaptation Strategy", loc="lower right" if "cifar" in d_name.lower() else "upper left")

    plt.suptitle("Transfer Learning Benchmark: Accuracy by Strategy & Architecture", fontsize=15, fontweight="bold", y=0.98)
    acc_path = os.path.join(save_dir, "benchmark_accuracy_comparison.png")
    plt.tight_layout()
    plt.savefig(acc_path, bbox_inches="tight")
    plt.close()

    # 2. Training Time / Convergence Speed Comparison
    fig, axes = plt.subplots(1, 2, figsize=(16, 6), sharey=False, dpi=300)
    for idx, d_name in enumerate(datasets):
        ax = axes[idx]
        sub_df = results_df[results_df["dataset"] == d_name]
        sns.barplot(
            data=sub_df,
            x="model",
            y="total_train_time_sec",
            hue="strategy",
            hue_order=[s for s in strategy_order if s in sub_df["strategy"].unique()],
            palette=palette,
            ax=ax,
        )
        ax.set_title(f"Training Time: {d_name.upper()}", fontweight="bold")
        ax.set_xlabel("Backbone Architecture")
        ax.set_ylabel("Total Training Time (Seconds)")
        ax.legend(title="Adaptation Strategy", loc="upper right")

    plt.suptitle("Computational Efficiency: Training Duration Across Strategies", fontsize=15, fontweight="bold", y=0.98)
    time_path = os.path.join(save_dir, "benchmark_training_time.png")
    plt.tight_layout()
    plt.savefig(time_path, bbox_inches="tight")
    plt.close()

    print(f"[*] Benchmark charts saved to: {acc_path} and {time_path}")


def plot_transfer_gap_delta(results_df: pd.DataFrame, save_path: str = "./results/transfer_gap_delta.png"):
    """
    Plots the empirical Transfer Delta: Accuracy(Full Finetune) - Accuracy(Scratch)
    to clearly show the boundary condition where transfer learning helps vs where gain shrinks.
    """
    set_plot_style()
    os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)

    records = []
    for (d, m), group in results_df.groupby(["dataset", "model"]):
        scratch_acc = group[group["strategy"] == "scratch"]["best_accuracy"].values
        finetune_acc = group[group["strategy"] == "full_finetune"]["best_accuracy"].values
        fe_acc = group[group["strategy"] == "feature_extraction"]["best_accuracy"].values

        if len(scratch_acc) > 0 and len(finetune_acc) > 0:
            delta_full = (finetune_acc[0] - scratch_acc[0]) * 100.0
            records.append({
                "dataset": d,
                "model": m,
                "type": "Full Fine-Tune vs Scratch",
                "delta_pct": delta_full,
            })
        if len(scratch_acc) > 0 and len(fe_acc) > 0:
            delta_fe = (fe_acc[0] - scratch_acc[0]) * 100.0
            records.append({
                "dataset": d,
                "model": m,
                "type": "Feature Extraction vs Scratch",
                "delta_pct": delta_fe,
            })

    if not records:
        return

    delta_df = pd.DataFrame(records)
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
    sns.barplot(
        data=delta_df,
        x="model",
        y="delta_pct",
        hue="dataset",
        palette=["#3498db", "#e67e22"],
        ax=ax,
    )
    ax.axhline(0, color="black", linestyle="--", linewidth=1)
    ax.set_ylabel("Accuracy Delta (% Points vs Scratch)")
    ax.set_xlabel("Backbone Model")
    ax.set_title("Empirical Transfer Margin: Pre-training Advantage Over Scratch", fontweight="bold")
    ax.legend(title="Target Domain")

    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    print(f"[*] Transfer delta plot saved to: {save_path}")
