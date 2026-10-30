"""
Top-level entry point for the Transfer Learning Empirical Benchmark project.
Allows running the 24-experiment matrix, CKA representation drift analysis, or both.
"""

import os
import sys
import argparse

# Add transfer_benchmark to sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BENCHMARK_DIR = os.path.join(BASE_DIR, "transfer_benchmark")
sys.path.insert(0, BENCHMARK_DIR)

from transfer_benchmark.run_experiments import run_benchmark_suite
from transfer_benchmark.run_cka_analysis import run_cka_layer_diagnosis, compare_domain_drift


def main():
    parser = argparse.ArgumentParser(
        description="Transfer Learning for Image Classification: When Does Pre-Training Help or Hurt?"
    )
    parser.add_argument("--mode", type=str, choices=["all", "experiments", "cka"], default="all",
                        help="Execution mode: 'experiments' (run 24-benchmark sweep), 'cka' (run CKA drift analysis), or 'all' (both)")
    parser.add_argument("--quick", action="store_true",
                        help="Quick prototyping mode: run a calibrated fast verification across all configurations")
    parser.add_argument("--epochs", type=int, default=None, help="Epochs per run")
    parser.add_argument("--batch_size", type=int, default=None, help="Batch size")
    parser.add_argument("--lr", type=float, default=None, help="Base learning rate")
    parser.add_argument("--backbone_lr", type=float, default=None, help="Backbone learning rate for full_finetune")
    parser.add_argument("--max_train_samples", type=int, default=None, help="Subsample train set size")
    parser.add_argument("--max_test_samples", type=int, default=None, help="Subsample test set size")
    parser.add_argument("--datasets", type=str, default=None, help="Comma-separated datasets (e.g. cifar10,pathmnist)")
    parser.add_argument("--models", type=str, default=None, help="Comma-separated models (e.g. resnet50,efficientnet_b0,mobilenet_v2)")
    parser.add_argument("--strategies", type=str, default=None, help="Comma-separated strategies")
    parser.add_argument("--results_dir", type=str, default=os.path.join(BENCHMARK_DIR, "results"), help="Results directory")
    parser.add_argument("--data_cache", type=str, default=os.path.join(BENCHMARK_DIR, "data_cache"), help="Data cache directory")
    parser.add_argument("--config", type=str, default=os.path.join(BENCHMARK_DIR, "configs", "default_config.yaml"), help="Config file")
    parser.add_argument("--device", type=str, default="auto", help="Device ('auto', 'cuda', 'cpu')")
    parser.add_argument("--force", action="store_true", help="Force re-running existing completed runs")

    args = parser.parse_args()

    os.makedirs(args.results_dir, exist_ok=True)
    os.makedirs(args.data_cache, exist_ok=True)

    if args.mode in ["all", "experiments"]:
        print(f"\n[>>>] STAGE 1: EXECUTING BENCHMARK MATRIX EXPERIMENTS [>>>]\n")
        run_benchmark_suite(config_path=args.config, args=args)

    if args.mode in ["all", "cka"]:
        print(f"\n[>>>] STAGE 2: EXECUTING LINEAR CKA REPRESENTATIONAL DRIFT ANALYSIS [>>>]\n")
        import torch
        device = torch.device("cuda" if torch.cuda.is_available() and args.device != "cpu" else "cpu") if args.device == "auto" else torch.device(args.device)

        cifar_res = run_cka_layer_diagnosis(
            dataset_name="cifar10",
            model_name="resnet50",
            n_calibration=1000 if not args.quick else 300,
            checkpoints_dir=os.path.join(args.results_dir, "checkpoints"),
            results_dir=args.results_dir,
            device=device,
        )

        path_res = run_cka_layer_diagnosis(
            dataset_name="pathmnist",
            model_name="resnet50",
            n_calibration=1000 if not args.quick else 300,
            checkpoints_dir=os.path.join(args.results_dir, "checkpoints"),
            results_dir=args.results_dir,
            device=device,
        )

        compare_domain_drift(
            cifar_res,
            path_res,
            save_path=os.path.join(args.results_dir, "cka_drift_comparison.png")
        )

        # Standard cka_heatmap.png
        import shutil
        cifar_hm = os.path.join(args.results_dir, "cka_cifar10_pretrained_vs_finetuned.png")
        std_hm = os.path.join(args.results_dir, "cka_heatmap.png")
        if os.path.exists(cifar_hm):
            shutil.copy(cifar_hm, std_hm)
            print(f"[*] Standard {std_hm} generated successfully.")

    # Automatically synthesize results into research report
    try:
        from transfer_benchmark.generate_report import generate_synthesis_report
        generate_synthesis_report(results_dir=args.results_dir)
    except Exception as e:
        print(f"[!] Warning generating synthesis report: {e}")

    print(f"\n[SUCCESS] ALL STAGES FINISHED. Check outputs in: {args.results_dir}\n")


if __name__ == "__main__":
    main()
