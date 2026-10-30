"""
Generates high-resolution publication-quality diagrams for the Computer Vision Project Report:
1. Figure 3.1: Benchmark Methodology Flowchart
2. Figure 4.1: System Architecture Diagram
3. Figure 4.2: Four Transfer Learning Adaptation Strategies Diagram
4. Figure 4.3: Linear CKA Mathematical Pipeline Diagram
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

os.makedirs("report_assets", exist_ok=True)
plt.rcParams.update({"font.sans-serif": "DejaVu Sans", "font.size": 10})


def generate_flowchart():
    fig, ax = plt.subplots(figsize=(10, 13), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 13)
    ax.axis("off")

    def draw_box(x, y, w, h, text, bg_color="#e8f4f8", border_color="#2980b9", title=None):
        box = patches.FancyBboxPatch(
            (x - w / 2, y - h / 2),
            w,
            h,
            boxstyle="round,pad=0.15,rounding_size=0.15",
            facecolor=bg_color,
            edgecolor=border_color,
            linewidth=1.8,
        )
        ax.add_patch(box)
        if title:
            ax.text(x, y + h / 4, title, ha="center", va="center", fontsize=11, fontweight="bold", color="#1a252f")
            ax.text(x, y - h / 5, text, ha="center", va="center", fontsize=9.5, color="#2c3e50")
        else:
            ax.text(x, y, text, ha="center", va="center", fontsize=10, fontweight="bold", color="#2c3e50")

    def draw_arrow(x1, y1, x2, y2, label=None):
        ax.annotate(
            "",
            xy=(x2, y2),
            xytext=(x1, y1),
            arrowprops=dict(facecolor="#34495e", edgecolor="#34495e", width=1.5, headwidth=7, headlength=7),
        )
        if label:
            ax.text((x1 + x2) / 2 + 0.15, (y1 + y2) / 2, label, fontsize=8.5, color="#7f8c8d", va="center")

    # Nodes
    draw_box(5, 12.2, 7.5, 0.9, "Define Near vs Far Domains & Research Hypotheses", "#e8f8f5", "#16a085", "1. Problem Formulation")
    draw_box(5, 10.7, 8.5, 1.2, "CIFAR-10 (Near / Natural) & PathMNIST (Far / Histology)\n224x224 Resolution, 3 Channels, ImageNet Normalization", "#eaf2f8", "#2980b9", "2. Data Ingestion & Standardization")
    draw_box(5, 9.0, 8.5, 1.3, "ResNet-50 | EfficientNet-B0 | MobileNet-V2\nDropout(0.2) + Standardized Linear Classification Head", "#f4ecf7", "#8e44ad", "3. Backbone Architecture Selection")
    draw_box(5, 7.1, 9.0, 1.6, "1. Scratch (Random Weights, lr=1e-3)\n2. Feature Extraction (Backbone Frozen, Head lr=1e-3)\n3. Partial Finetune (Freeze early stages, Train deep blocks)\n4. Full Finetune (Differential lr: 1e-4 backbone, 1e-3 head)", "#fef9e7", "#f39c12", "4. Matrix Adaptation Strategies (4 Regimes)")
    draw_box(5, 4.9, 8.5, 1.4, "AdamW Optimizer with Parameter Grouping\nCross-Entropy Loss, Gradient Scaling (AMP)\nTop-1 Accuracy, Weighted F1, Convergence Tracking", "#fbeee6", "#d35400", "5. Training & Evaluation Pipeline")
    draw_box(5, 2.9, 8.5, 1.5, "PyTorch Forward Hooks on Intermediate Layers\nGlobal Average Pooling (GAP): (B, C, H, W) -> (B, C)\nLinear Centered Kernel Alignment (CKA) on N=1000", "#e8f6f3", "#1abc9c", "6. Representational Drift Diagnosis")
    draw_box(5, 1.1, 7.5, 0.9, "Benchmark CSVs, CKA Heatmaps, Synthesis Report", "#e8f8f5", "#27ae60", "7. Empirical Results & Decision Framework")

    # Arrows
    draw_arrow(5, 11.75, 5, 11.3)
    draw_arrow(5, 10.1, 5, 9.65)
    draw_arrow(5, 8.35, 5, 7.9)
    draw_arrow(5, 6.3, 5, 5.6)
    draw_arrow(5, 4.2, 5, 3.65)
    draw_arrow(5, 2.15, 5, 1.55)

    plt.tight_layout()
    save_path = "report_assets/fig3_1_methodology_flowchart.png"
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    print(f"[*] Flowchart saved to {save_path}")


def generate_system_architecture():
    fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 7.5)
    ax.axis("off")

    def draw_panel(x, y, w, h, title, bg="#f8f9f9", border="#bdc3c7"):
        panel = patches.FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.1,rounding_size=0.15", facecolor=bg, edgecolor=border, linewidth=1.5
        )
        ax.add_patch(panel)
        ax.text(x + 0.2, y + h - 0.35, title, fontsize=10.5, fontweight="bold", color="#2c3e50")

    # Panels
    draw_panel(0.4, 0.5, 3.0, 6.5, "DATA & INGESTION PIPELINE", "#ebf5fb", "#2980b9")
    draw_panel(3.8, 0.5, 3.4, 6.5, "MODELS & ADAPTATION CORE", "#fef9e7", "#d68910")
    draw_panel(7.6, 0.5, 3.0, 6.5, "DIAGNOSTICS & ANALYSIS", "#eafaf1", "#27ae60")

    def draw_sub_box(x, y, w, h, text, bg="#ffffff", border="#95a5a6"):
        box = patches.FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.08,rounding_size=0.1", facecolor=bg, edgecolor=border, linewidth=1.2
        )
        ax.add_patch(box)
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=8.5, color="#34495e")

    # Left Panel components
    draw_sub_box(0.6, 5.0, 2.6, 1.1, "CIFAR-10 Dataset\n(Near-Domain / Natural)\n50,000 Train | 10,000 Test")
    draw_sub_box(0.6, 3.6, 2.6, 1.1, "MedMNIST PathMNIST\n(Far-Domain / Histology)\n89,996 Train | 7,180 Test")
    draw_sub_box(0.6, 2.2, 2.6, 1.1, "Transform Pipeline\nResize(224, 224)\nImageNet Norm (u, s)")
    draw_sub_box(0.6, 0.8, 2.6, 1.1, "PyTorch DataLoader\nStratified Subsampling\nPin Memory & Pinning")

    # Middle Panel components
    draw_sub_box(4.0, 5.2, 3.0, 1.0, "Backbone Architectures\nResNet-50 | EfficientNet-B0\nMobileNet-V2")
    draw_sub_box(4.0, 3.8, 3.0, 1.1, "Adaptation Strategies\n1. Scratch | 2. Feature Ext.\n3. Partial FT | 4. Full FT")
    draw_sub_box(4.0, 2.3, 3.0, 1.2, "Standardized Head\nDropout(p=0.2) -> Linear\nDifferential Optimizer\n(lr=1e-4 vs lr=1e-3)")
    draw_sub_box(4.0, 0.8, 3.0, 1.2, "Training Engine\nAdamW, CrossEntropyLoss\nAMP Mixed Precision\nConvergence Logging")

    # Right Panel components
    draw_sub_box(7.8, 5.2, 2.6, 1.1, "Forward Feature Hooks\nconv1, layer1, layer2\nlayer3, layer4")
    draw_sub_box(7.8, 3.8, 2.6, 1.1, "Global Avg Pooling\n(B, C, H, W) -> (B, C)\nCalibration N=1000")
    draw_sub_box(7.8, 2.3, 2.6, 1.2, "Linear CKA Engine\nDouble Centering: H K H\nHSIC(K, L) Calculation\nDrift Alignment Curve")
    draw_sub_box(7.8, 0.8, 2.6, 1.2, "Reporting & Plots\nHeatmaps, Delta Charts\nCSV Summaries, Markdown")

    # Inter-panel arrows
    ax.annotate("", xy=(3.8, 3.8), xytext=(3.4, 3.8), arrowprops=dict(facecolor="#2980b9", edgecolor="#2980b9", width=2, headwidth=7))
    ax.annotate("", xy=(7.6, 3.8), xytext=(7.2, 3.8), arrowprops=dict(facecolor="#d68910", edgecolor="#d68910", width=2, headwidth=7))

    plt.tight_layout()
    save_path = "report_assets/fig4_1_system_architecture.png"
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    print(f"[*] Architecture saved to {save_path}")


def generate_adaptation_strategies_diagram():
    fig, axes = plt.subplots(1, 4, figsize=(13, 6), dpi=300)
    strategies = [
        ("1. Scratch", "Random Init\nAll Layers Trainable\nlr = 1e-3", ["conv1", "layer1", "layer2", "layer3", "layer4", "FC Head"], [True, True, True, True, True, True]),
        ("2. Feature Extraction", "Pretrained Weights\nBackbone Frozen\nlr = 1e-3 (Head only)", ["conv1", "layer1", "layer2", "layer3", "layer4", "FC Head"], [False, False, False, False, False, True]),
        ("3. Partial Finetune", "Pretrained Weights\nDeep Block + Head\nlr = 1e-3", ["conv1", "layer1", "layer2", "layer3", "layer4", "FC Head"], [False, False, False, False, True, True]),
        ("4. Full Finetune", "Pretrained Weights\nDifferential LR:\nBackbone 1e-4, Head 1e-3", ["conv1", "layer1", "layer2", "layer3", "layer4", "FC Head"], [True, True, True, True, True, True]),
    ]

    for idx, (title, subtitle, layers, train_mask) in enumerate(strategies):
        ax = axes[idx]
        ax.set_xlim(0, 4)
        ax.set_ylim(0, 9)
        ax.axis("off")
        ax.set_title(title, fontsize=12, fontweight="bold", pad=10)
        ax.text(2, 8.2, subtitle, ha="center", va="center", fontsize=8.5, color="#555555")

        y_positions = [6.8, 5.6, 4.4, 3.2, 2.0, 0.8]
        for y, layer_name, is_train in zip(y_positions, layers, train_mask):
            if idx == 3:  # Full finetune differential colors
                bg = "#2ecc71" if layer_name == "FC Head" else "#a9dfbf"
                border = "#27ae60"
                txt_lbl = f"{layer_name} (lr=1e-3)" if layer_name == "FC Head" else f"{layer_name} (lr=1e-4)"
            else:
                bg = "#2ecc71" if is_train else "#bdc3c7"
                border = "#27ae60" if is_train else "#7f8c8d"
                txt_lbl = f"{layer_name} (Trainable)" if is_train else f"{layer_name} (Frozen)"

            box = patches.FancyBboxPatch(
                (0.4, y - 0.4), 3.2, 0.8, boxstyle="round,pad=0.1,rounding_size=0.1",
                facecolor=bg, edgecolor=border, linewidth=1.5
            )
            ax.add_patch(box)
            ax.text(2, y, txt_lbl, ha="center", va="center", fontsize=9, fontweight="bold",
                    color="#ffffff" if is_train and idx != 3 else ("#1b4f72" if idx == 3 and layer_name != "FC Head" else "#2c3e50"))

            # Arrow to next
            if y > 0.8:
                ax.annotate("", xy=(2, y - 0.55), xytext=(2, y - 0.45),
                            arrowprops=dict(facecolor="#34495e", edgecolor="#34495e", width=1.2, headwidth=5))

    plt.suptitle("Figure 4.2: Four Transfer Learning Adaptation Strategies Configuration", fontsize=14, fontweight="bold", y=0.98)
    plt.tight_layout()
    save_path = "report_assets/fig4_2_adaptation_strategies.png"
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    print(f"[*] Adaptation strategies diagram saved to {save_path}")


def generate_cka_pipeline_diagram():
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")

    def draw_c_box(x, y, w, h, title, formula, bg="#ebf5fb", border="#2980b9"):
        box = patches.FancyBboxPatch(
            (x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.1,rounding_size=0.15",
            facecolor=bg, edgecolor=border, linewidth=1.5
        )
        ax.add_patch(box)
        ax.text(x, y + 0.35, title, ha="center", va="center", fontsize=10, fontweight="bold", color="#1b4f72")
        ax.text(x, y - 0.35, formula, ha="center", va="center", fontsize=9, color="#2c3e50")

    draw_c_box(1.5, 3.6, 2.4, 1.4, "Activation Matrix X", "X in R^(N x D1)\n(Model A, Layer l)", "#fef9e7", "#d4ac0d")
    draw_c_box(1.5, 1.4, 2.4, 1.4, "Activation Matrix Y", "Y in R^(N x D2)\n(Model B, Layer m)", "#fef9e7", "#d4ac0d")

    draw_c_box(4.5, 3.6, 2.4, 1.4, "Linear Gram Matrix K", "K = X X^T\n(N x N Pairwise Sim)", "#e8f8f5", "#16a085")
    draw_c_box(4.5, 1.4, 2.4, 1.4, "Linear Gram Matrix L", "L = Y Y^T\n(N x N Pairwise Sim)", "#e8f8f5", "#16a085")

    draw_c_box(7.5, 2.5, 3.0, 1.8, "Hilbert-Schmidt (HSIC)", "Kc = H K H,  Lc = H L H\nHSIC(K, L) = tr(Kc Lc)", "#f4ecf7", "#8e44ad")

    draw_c_box(5.0, -0.4, 6.0, 0.9, "Linear CKA Score", "CKA(K, L) = HSIC(K, L) / sqrt(HSIC(K,K) * HSIC(L,L))", "#eafaf1", "#27ae60")

    # Connectors
    ax.annotate("", xy=(3.3, 3.6), xytext=(2.7, 3.6), arrowprops=dict(facecolor="#34495e", width=1.5, headwidth=6))
    ax.annotate("", xy=(3.3, 1.4), xytext=(2.7, 1.4), arrowprops=dict(facecolor="#34495e", width=1.5, headwidth=6))
    ax.annotate("", xy=(6.0, 2.9), xytext=(5.7, 3.3), arrowprops=dict(facecolor="#34495e", width=1.5, headwidth=6))
    ax.annotate("", xy=(6.0, 2.1), xytext=(5.7, 1.7), arrowprops=dict(facecolor="#34495e", width=1.5, headwidth=6))

    plt.suptitle("Figure 4.3: Linear CKA (Centered Kernel Alignment) Computational Pipeline", fontsize=13, fontweight="bold", y=0.96)
    plt.tight_layout()
    save_path = "report_assets/fig4_3_cka_pipeline.png"
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    print(f"[*] CKA pipeline diagram saved to {save_path}")


if __name__ == "__main__":
    generate_flowchart()
    generate_system_architecture()
    generate_adaptation_strategies_diagram()
    generate_cka_pipeline_diagram()
    print("[SUCCESS] All report diagrams generated successfully.")
