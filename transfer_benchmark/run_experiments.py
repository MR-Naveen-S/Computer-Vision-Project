import os
import sys
import time
import argparse
import yaml
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from tqdm import tqdm

# Ensure local imports work whether run from transfer_benchmark/ or root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.dataset_loader import get_dataloaders
from models.model_factory import (
    build_model,
    get_optimizer_param_groups,
    get_model_param_stats,
)
from utils.metrics import compute_classification_metrics, MetricTracker
from utils.plotting import plot_comparative_bar_charts, plot_transfer_gap_delta


def train_epoch(model, loader, criterion, optimizer, device, scaler=None):
    model.train()
    total_loss = 0.0
    total_samples = 0

    use_amp = scaler is not None and device.type == "cuda"

    for images, targets in loader:
        if targets.dim() > 1:
            targets = targets.squeeze().long()
        else:
            targets = targets.long()

        images, targets = images.to(device, non_blocking=True), targets.to(device, non_blocking=True)
        batch_size = images.size(0)

        optimizer.zero_grad()

        if use_amp:
            with torch.amp.autocast(device_type="cuda"):
                outputs = model(images)
                loss = criterion(outputs, targets)
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
        else:
            outputs = model(images)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()

        total_loss += loss.item() * batch_size
        total_samples += batch_size

    return total_loss / max(total_samples, 1)


@torch.no_grad()
def evaluate(model, loader, criterion, device):
    model.eval()
    all_preds, all_labels = [], []
    total_loss = 0.0
    total_samples = 0

    for images, targets in loader:
        if targets.dim() > 1:
            targets = targets.squeeze().long()
        else:
            targets = targets.long()

        batch_size = images.size(0)
        images, targets = images.to(device, non_blocking=True), targets.to(device, non_blocking=True)

        outputs = model(images)
        loss = criterion(outputs, targets)

        preds = torch.argmax(outputs, dim=1).cpu().numpy()
        all_preds.extend(preds)
        all_labels.extend(targets.cpu().numpy())

        total_loss += loss.item() * batch_size
        total_samples += batch_size

    metrics = compute_classification_metrics(all_labels, all_preds)
    metrics["val_loss"] = total_loss / max(total_samples, 1)
    return metrics


def run_single_experiment(
    dataset_name: str,
    model_name: str,
    strategy: str,
    epochs: int = 10,
    batch_size: int = 64,
    base_lr: float = 1e-3,
    backbone_lr: float = 1e-4,
    weight_decay: float = 1e-4,
    data_cache: str = "./data_cache",
    results_dir: str = "./results",
    max_train_samples: int = None,
    max_test_samples: int = None,
    save_checkpoint: bool = True,
    device: torch.device = None,
):
    """
    Executes a single benchmark run for a specific (dataset, model, strategy) triplet.
    """
    if device is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    print(f"\n{'='*75}")
    print(f"[*] RUNNING: Dataset={dataset_name.upper()} | Model={model_name} | Strategy={strategy}")
    print(f"[*] Target Device: {device} | Epochs: {epochs} | Batch Size: {batch_size}")
    print(f"{'='*75}")

    train_loader, test_loader, num_classes = get_dataloaders(
        dataset_name=dataset_name,
        batch_size=batch_size,
        data_cache=data_cache,
        max_train_samples=max_train_samples,
        max_test_samples=max_test_samples,
    )

    model = build_model(model_name, strategy, num_classes).to(device)
    param_stats = get_model_param_stats(model)
    print(
        f"[*] Params: Total={param_stats['total_params']:,} | "
        f"Trainable={param_stats['trainable_params']:,} ({param_stats['trainable_percent']:.1f}%)"
    )

    criterion = nn.CrossEntropyLoss()
    param_groups = get_optimizer_param_groups(
        model,
        strategy=strategy,
        base_lr=base_lr,
        backbone_lr=backbone_lr,
        weight_decay=weight_decay,
    )
    optimizer = torch.optim.AdamW(param_groups)
    scaler = torch.amp.GradScaler("cuda") if device.type == "cuda" else None

    tracker = MetricTracker()
    best_acc = 0.0
    best_f1 = 0.0
    best_state_dict = None

    ckpt_dir = os.path.join(results_dir, "checkpoints")
    os.makedirs(ckpt_dir, exist_ok=True)
    ckpt_path = os.path.join(ckpt_dir, f"{dataset_name}_{model_name}_{strategy}_best.pt")

    pbar = tqdm(range(1, epochs + 1), desc=f"{dataset_name}-{model_name}-{strategy}")
    for epoch in pbar:
        tracker.start_epoch()
        train_loss = train_epoch(model, train_loader, criterion, optimizer, device, scaler=scaler)
        eval_metrics = evaluate(model, test_loader, criterion, device)

        acc = eval_metrics["accuracy"]
        f1 = eval_metrics["f1_weighted"]

        tracker.end_epoch(epoch, train_loss, acc, f1)

        if acc > best_acc:
            best_acc = acc
            best_f1 = f1
            if save_checkpoint:
                best_state_dict = model.state_dict().copy()
                torch.save(
                    {
                        "model_name": model_name,
                        "dataset_name": dataset_name,
                        "strategy": strategy,
                        "num_classes": num_classes,
                        "epoch": epoch,
                        "accuracy": best_acc,
                        "f1": best_f1,
                        "state_dict": best_state_dict,
                    },
                    ckpt_path,
                )

        pbar.set_postfix({
            "Loss": f"{train_loss:.4f}",
            "Acc": f"{acc*100:.2f}%",
            "Best": f"{best_acc*100:.2f}%",
        })

    summary = tracker.get_summary()
    domain_type = "near" if "cifar" in dataset_name.lower() else "far"

    result_record = {
        "dataset": dataset_name,
        "domain": domain_type,
        "model": model_name,
        "strategy": strategy,
        "best_accuracy": best_acc,
        "best_f1": best_f1,
        "best_epoch": summary.get("best_epoch", epochs),
        "total_train_time_sec": summary.get("total_train_time_sec", 0.0),
        "avg_epoch_time_sec": summary.get("avg_epoch_time_sec", 0.0),
        "convergence_epoch": summary.get("convergence_epoch", epochs),
        "time_to_convergence_sec": summary.get("time_to_convergence_sec", summary.get("total_train_time_sec", 0.0)),
        "trainable_params": param_stats["trainable_params"],
        "total_params": param_stats["total_params"],
        "checkpoint_path": ckpt_path if save_checkpoint and os.path.exists(ckpt_path) else None,
    }

    print(f"[+] Completed: Best Top-1 Acc = {best_acc*100:.2f}% | Best F1 = {best_f1:.4f} | Total Time = {summary.get('total_train_time_sec', 0.0):.1f}s")
    return result_record


def run_benchmark_suite(config_path: str = None, args=None):
    """
    Executes the full evaluation matrix (2 Datasets × 3 Architectures × 4 Adaptation Strategies).
    """
    # Load configuration
    if config_path and os.path.exists(config_path):
        with open(config_path, "r") as f:
            cfg = yaml.safe_load(f)
    else:
        cfg = {}

    results_dir = getattr(args, "results_dir", None) or cfg.get("experiment", {}).get("results_dir", "./results")
    data_cache = getattr(args, "data_cache", None) or cfg.get("experiment", {}).get("data_cache_dir", "./data_cache")
    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(data_cache, exist_ok=True)

    epochs = getattr(args, "epochs", None) or cfg.get("training", {}).get("epochs", 10)
    batch_size = getattr(args, "batch_size", None) or cfg.get("training", {}).get("batch_size", 64)
    base_lr = getattr(args, "lr", None) or cfg.get("training", {}).get("lr", 1e-3)
    backbone_lr = getattr(args, "backbone_lr", None) or cfg.get("training", {}).get("backbone_lr", 1e-4)

    max_train = getattr(args, "max_train_samples", None) or cfg.get("training", {}).get("max_train_samples")
    max_test = getattr(args, "max_test_samples", None) or cfg.get("training", {}).get("max_test_samples")

    # Override for quick verification mode if specified
    if getattr(args, "quick", False):
        print("[!] Quick verification mode enabled: Subsampling data and reducing epochs for rapid sweep.")
        epochs = min(epochs, 3)
        max_train = 1500 if max_train is None else min(max_train, 1500)
        max_test = 500 if max_test is None else min(max_test, 500)

    # Matrix items
    datasets_arg = getattr(args, "datasets", None)
    datasets_list = (
        datasets_arg.split(",")
        if datasets_arg
        else [d["name"] if isinstance(d, dict) else d for d in cfg.get("matrix", {}).get("datasets", ["cifar10", "pathmnist"])]
    )
    models_arg = getattr(args, "models", None)
    models_list = (
        models_arg.split(",")
        if models_arg
        else cfg.get("matrix", {}).get("models", ["resnet50", "efficientnet_b0", "mobilenet_v2"])
    )
    strategies_arg = getattr(args, "strategies", None)
    strategies_list = (
        strategies_arg.split(",")
        if strategies_arg
        else cfg.get("matrix", {}).get("strategies", ["scratch", "feature_extraction", "partial_finetune", "full_finetune"])
    )

    device_str = getattr(args, "device", None) or cfg.get("training", {}).get("device", "auto")
    if device_str == "auto":
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    else:
        device = torch.device(device_str)

    print(f"\n{'='*75}")
    print(" TRANSFER LEARNING EMPIRICAL BENCHMARK: MATRIX RUNNER")
    print(f"{'='*75}")
    print(f" Datasets     ({len(datasets_list)}): {datasets_list}")
    print(f" Backbones    ({len(models_list)}): {models_list}")
    print(f" Strategies   ({len(strategies_list)}): {strategies_list}")
    print(f" Total Runs   : {len(datasets_list) * len(models_list) * len(strategies_list)}")
    print(f" Device       : {device}")
    print(f" Epochs/run   : {epochs}")
    print(f" Batch Size   : {batch_size}")
    print(f"{'='*75}\n")

    summary_csv = os.path.join(results_dir, "benchmark_summary.csv")
    results = []

    # If results already partially exist, load to avoid re-running completed runs
    if os.path.exists(summary_csv) and not (args and args.force):
        try:
            existing_df = pd.read_csv(summary_csv)
            results = existing_df.to_dict("records")
            print(f"[*] Found {len(results)} existing completed runs in {summary_csv}.")
        except Exception:
            results = []

    completed_triplets = {(r["dataset"], r["model"], r["strategy"]) for r in results}

    total_runs = len(datasets_list) * len(models_list) * len(strategies_list)
    run_idx = 0

    for d in datasets_list:
        for m in models_list:
            for s in strategies_list:
                run_idx += 1
                if (d, m, s) in completed_triplets:
                    print(f"[-] [{run_idx}/{total_runs}] Skipping already completed: {d} | {m} | {s}")
                    continue

                print(f"\n[+] [{run_idx}/{total_runs}] Progressing: {d} | {m} | {s}")
                try:
                    res = run_single_experiment(
                        dataset_name=d,
                        model_name=m,
                        strategy=s,
                        epochs=epochs,
                        batch_size=batch_size,
                        base_lr=base_lr,
                        backbone_lr=backbone_lr,
                        data_cache=data_cache,
                        results_dir=results_dir,
                        max_train_samples=max_train,
                        max_test_samples=max_test,
                        save_checkpoint=True,
                        device=device,
                    )
                    results.append(res)
                    # Checkpoint results incrementally after every experiment
                    pd.DataFrame(results).to_csv(summary_csv, index=False)
                except Exception as e:
                    print(f"[!] Error during run {d}-{m}-{s}: {e}")
                    import traceback
                    traceback.print_exc()

    # Final summary and plots
    df = pd.DataFrame(results)
    df.to_csv(summary_csv, index=False)
    print(f"\n{'='*75}")
    print(f"[SUCCESS] Benchmark Matrix Complete! Results saved to: {summary_csv}")
    print(f"{'='*75}")

    try:
        plot_comparative_bar_charts(df, save_dir=results_dir)
        plot_transfer_gap_delta(df, save_path=os.path.join(results_dir, "transfer_gap_delta.png"))
    except Exception as e:
        print(f"[!] Warning generating final benchmark plots: {e}")

    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transfer Learning Empirical Benchmark Matrix Runner")
    parser.add_argument("--config", type=str, default="./configs/default_config.yaml", help="Path to YAML config")
    parser.add_argument("--results_dir", type=str, default="./results", help="Directory to save results")
    parser.add_argument("--data_cache", type=str, default="./data_cache", help="Directory to cache datasets")
    parser.add_argument("--epochs", type=int, default=None, help="Number of epochs per experiment")
    parser.add_argument("--batch_size", type=int, default=None, help="Batch size")
    parser.add_argument("--lr", type=float, default=None, help="Base learning rate")
    parser.add_argument("--backbone_lr", type=float, default=None, help="Backbone learning rate")
    parser.add_argument("--max_train_samples", type=int, default=None, help="Subsample train set size")
    parser.add_argument("--max_test_samples", type=int, default=None, help="Subsample test set size")
    parser.add_argument("--datasets", type=str, default=None, help="Comma-separated datasets (e.g. cifar10,pathmnist)")
    parser.add_argument("--models", type=str, default=None, help="Comma-separated models (e.g. resnet50,efficientnet_b0)")
    parser.add_argument("--strategies", type=str, default=None, help="Comma-separated strategies")
    parser.add_argument("--device", type=str, default=None, help="Device ('cpu', 'cuda', 'auto')")
    parser.add_argument("--quick", action="store_true", help="Quick mode for rapid validation")
    parser.add_argument("--force", action="store_true", help="Force re-running already completed experiments")

    parsed_args = parser.parse_args()
    run_benchmark_suite(config_path=parsed_args.config, args=parsed_args)
