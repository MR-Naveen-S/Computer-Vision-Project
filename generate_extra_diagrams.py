"""
Generate additional high-impact diagrams for the academic project report:
1. fig4_0_dataset_domains.png: Visual comparison of CIFAR-10 vs PathMNIST with color distribution profiles.
2. fig4_4_backbone_comparison.png: Micro-architectural block comparison (ResNet-50 vs EfficientNet vs MobileNet-V2).
3. fig6_1_decision_flowchart.png: Practical engineering decision tree flowchart for transfer strategy selection.
"""

import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

os.makedirs("report_assets", exist_ok=True)
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'

# =============================================================================
# 1. FIG 4.0: DATASET DOMAIN COMPARISON & COLOR HISTOGRAMS
# =============================================================================
def generate_dataset_domains_figure():
    print("[+] Generating fig4_0_dataset_domains.png...")
    
    # Load CIFAR-10
    cifar_classes = ['Airplane', 'Automobile', 'Bird', 'Cat', 'Deer', 'Dog', 'Frog', 'Horse', 'Ship', 'Truck']
    with open('data_cache/cifar-10-batches-py/data_batch_1', 'rb') as f:
        cifar_dict = pickle.load(f, encoding='bytes')
    cifar_data = cifar_dict[b'data'].reshape(-1, 3, 32, 32).transpose(0, 2, 3, 1)
    cifar_labels = np.array(cifar_dict[b'labels'])
    
    # Load PathMNIST
    path_classes = ['Adipose', 'Complex Stroma', 'Debris', 'Lymphocytes', 'Mucus', 'Smooth Muscle', 'Normal Mucosa', 'Cancer Stroma', 'Colorectal Adeno.']
    path_dict = np.load('data_cache/pathmnist.npz')
    path_data = path_dict['train_images']
    path_labels = path_dict['train_labels'].squeeze()
    
    fig = plt.figure(figsize=(14, 8), dpi=220)
    
    # Title Banner
    fig.suptitle("Visual Domain Divergence: Near-Domain (CIFAR-10) vs Far-Domain (PathMNIST Histology)",
                 fontsize=15, fontweight='bold', y=0.98, color="#1b365d")
    
    # Subplot layout: 2 main panels
    # Left: CIFAR-10 (4 samples + RGB histogram)
    # Right: PathMNIST (4 samples + RGB histogram)
    
    cifar_indices = [np.where(cifar_labels == c)[0][0] for c in [0, 1, 3, 6, 8, 9]] # airplane, auto, cat, frog, ship, truck
    path_indices = [np.where(path_labels == c)[0][0] for c in [0, 2, 3, 4, 6, 8]] # adipose, debris, lymph, mucus, mucosa, cancer
    
    # Panel 1: CIFAR-10 Samples
    for i, idx in enumerate(cifar_indices[:6]):
        ax = fig.add_subplot(4, 6, i + 1)
        ax.imshow(cifar_data[idx])
        ax.set_title(cifar_classes[cifar_labels[idx]], fontsize=9, fontweight='bold', color="#2c3e50")
        ax.axis('off')
        if i == 0:
            ax.text(-0.35, 0.5, "CIFAR-10\n(Natural)", transform=ax.transAxes,
                    fontsize=11, fontweight='bold', va='center', ha='right', color="#1b365d", rotation=90)
            
    # Panel 2: CIFAR RGB Distribution
    ax_cifar_hist = fig.add_subplot(4, 2, 3)
    cifar_sample_batch = cifar_data[:1000].astype(np.float32) / 255.0
    r_c = cifar_sample_batch[:, :, :, 0].flatten()
    g_c = cifar_sample_batch[:, :, :, 1].flatten()
    b_c = cifar_sample_batch[:, :, :, 2].flatten()
    ax_cifar_hist.hist(r_c, bins=50, density=True, color='#e74c3c', alpha=0.5, label='Red Channel')
    ax_cifar_hist.hist(g_c, bins=50, density=True, color='#2ecc71', alpha=0.5, label='Green Channel')
    ax_cifar_hist.hist(b_c, bins=50, density=True, color='#3498db', alpha=0.5, label='Blue Channel')
    ax_cifar_hist.set_title("CIFAR-10 Balanced Spectral Intensity Profile (Natural Lighting)", fontsize=9.5, fontweight='bold', color="#2c3e50")
    ax_cifar_hist.set_xlabel("Normalized Pixel Intensity [0, 1]", fontsize=8.5)
    ax_cifar_hist.set_ylabel("Empirical Density", fontsize=8.5)
    ax_cifar_hist.legend(fontsize=7.5, loc='upper right')
    ax_cifar_hist.grid(True, linestyle='--', alpha=0.3)
    ax_cifar_hist.set_xlim(0, 1)

    # Panel 3: PathMNIST Samples
    for i, idx in enumerate(path_indices[:6]):
        ax = fig.add_subplot(4, 6, i + 13)
        ax.imshow(path_data[idx])
        ax.set_title(path_classes[path_labels[idx]], fontsize=8.5, fontweight='bold', color="#8e44ad")
        ax.axis('off')
        if i == 0:
            ax.text(-0.35, 0.5, "PathMNIST\n(Medical)", transform=ax.transAxes,
                    fontsize=11, fontweight='bold', va='center', ha='right', color="#8e44ad", rotation=90)
            
    # Panel 4: PathMNIST RGB Distribution
    ax_path_hist = fig.add_subplot(4, 2, 7)
    path_sample_batch = path_data[:1000].astype(np.float32) / 255.0
    r_p = path_sample_batch[:, :, :, 0].flatten()
    g_p = path_sample_batch[:, :, :, 1].flatten()
    b_p = path_sample_batch[:, :, :, 2].flatten()
    ax_path_hist.hist(r_p, bins=50, density=True, color='#9b59b6', alpha=0.6, label='Red (Eosin-Pink)')
    ax_path_hist.hist(g_p, bins=50, density=True, color='#2ecc71', alpha=0.3, label='Green (Low in H&E)')
    ax_path_hist.hist(b_p, bins=50, density=True, color='#2980b9', alpha=0.6, label='Blue (Hematoxylin)')
    ax_path_hist.set_title("PathMNIST H&E Stain Spectral Profile (Skewed Bimodal)", fontsize=9.5, fontweight='bold', color="#8e44ad")
    ax_path_hist.set_xlabel("Normalized Pixel Intensity [0, 1]", fontsize=8.5)
    ax_path_hist.set_ylabel("Empirical Density", fontsize=8.5)
    ax_path_hist.legend(fontsize=7.5, loc='upper left')
    ax_path_hist.grid(True, linestyle='--', alpha=0.3)
    ax_path_hist.set_xlim(0, 1)

    # Bottom analytical callout
    fig.text(0.5, 0.02,
             "Key Takeaway: CIFAR-10 exhibits unimodal, balanced RGB color spaces with clear geometric object silhouettes.\n"
             "PathMNIST exhibits intense Hematoxylin & Eosin (purple/pink) stain bi-modality with rotational symmetry and cellular texture without object borders.",
             ha='center', fontsize=9.5, style='italic', color="#333333",
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#f8f9fa', edgecolor='#bdc3c7', lw=0.8))

    plt.tight_layout(rect=[0.03, 0.05, 0.98, 0.95])
    plt.savefig("report_assets/fig4_0_dataset_domains.png", dpi=220)
    plt.close()
    print("[SUCCESS] report_assets/fig4_0_dataset_domains.png generated.")


# =============================================================================
# 2. FIG 4.4: MICRO-ARCHITECTURAL BLOCK COMPARISON
# =============================================================================
def generate_backbone_comparison_figure():
    print("[+] Generating fig4_4_backbone_comparison.png...")
    fig, axes = plt.subplots(1, 3, figsize=(15, 7.5), dpi=220)
    fig.suptitle("Comparative Micro-Architectural Block Topologies", fontsize=15, fontweight='bold', y=0.98, color="#1b365d")
    
    # -------------------------------------------------------------
    # (A) ResNet-50 Bottleneck Block
    # -------------------------------------------------------------
    ax = axes[0]
    ax.set_title("(A) ResNet-50 Bottleneck\n(Residual Compression-Expansion)", fontsize=11, fontweight='bold', color="#1b365d")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 14)
    ax.axis('off')
    
    # Boxes
    blocks_res = [
        (2, 11.5, 6, 1.2, "Input Feature Map $x$\n$(C=256, H, W)$", "#ecf0f1", "#7f8c8d"),
        (2.5, 9.2, 5, 1.2, "$1 \\times 1$ Conv, $C_{mid}=64$\n(Channel Squeeze) + BN + ReLU", "#d4e6f1", "#2980b9"),
        (2.5, 6.9, 5, 1.2, "$3 \\times 3$ Conv, $C_{mid}=64$\n(Spatial Filtering) + BN + ReLU", "#d5f5e3", "#27ae60"),
        (2.5, 4.6, 5, 1.2, "$1 \\times 1$ Conv, $C_{out}=256$\n(Channel Expansion) + BN", "#fcf3cf", "#f39c12"),
        (3.5, 2.5, 3, 1.0, "$\\bigoplus$ Add", "#fadbd8", "#e74c3c"),
        (2, 0.5, 6, 1.2, "Output Feature Map $\\mathcal{F}(x) + x$\n+ ReLU Activation", "#ecf0f1", "#7f8c8d"),
    ]
    for x, y, w, h, text, fc, ec in blocks_res:
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2", facecolor=fc, edgecolor=ec, lw=1.5)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=8.5, fontweight='bold', color="#1a252f")
        
    # Main stream arrows
    for y_start, y_end in [(11.5, 10.4), (9.2, 8.1), (6.9, 5.8), (4.6, 3.5), (2.5, 1.7)]:
        ax.annotate("", xy=(5, y_end), xytext=(5, y_start),
                    arrowprops=dict(arrowstyle="->", lw=1.5, color="#2c3e50"))
        
    # Residual identity skip connection
    ax.plot([2, 1.2, 1.2, 3.5], [12.1, 12.1, 3.0, 3.0], color="#c0392b", lw=2, linestyle='--')
    ax.annotate("", xy=(3.5, 3.0), xytext=(1.5, 3.0),
                arrowprops=dict(arrowstyle="->", lw=2, color="#c0392b"))
    ax.text(0.9, 7.5, "Identity Shortcut\n$x$", color="#c0392b", fontsize=8.5, fontweight='bold', rotation=90, va='center')
    ax.text(5, -0.4, "Total Params: 23.5M | Latency: 128s\nDeep Residual Gradient Stability", ha='center', fontsize=8.5, color="#555555")

    # -------------------------------------------------------------
    # (B) EfficientNet-B0 MBConv Block
    # -------------------------------------------------------------
    ax = axes[1]
    ax.set_title("(B) EfficientNet-B0 MBConv\n(Compound Scaled + SE Attention)", fontsize=11, fontweight='bold', color="#1b365d")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 14)
    ax.axis('off')
    
    blocks_eff = [
        (2, 11.5, 6, 1.2, "Input Feature Map $x$\n$(C_{in}, H, W)$", "#ecf0f1", "#7f8c8d"),
        (2.5, 9.4, 5, 1.1, "$1 \\times 1$ Conv (Expand $\\times 6$)\n+ BN + Swish", "#d4e6f1", "#2980b9"),
        (2.5, 7.6, 5, 1.1, "$3 \\times 3$ Depthwise Conv\n+ BN + Swish", "#d5f5e3", "#27ae60"),
        (2.5, 5.8, 5, 1.1, "Squeeze & Excitation (SE)\nGAP $\\rightarrow$ FC $\\rightarrow$ Sigmoid $\\otimes$", "#e8daef", "#8e44ad"),
        (2.5, 4.0, 5, 1.1, "$1 \\times 1$ Conv (Project)\nLinear Output", "#fcf3cf", "#f39c12"),
        (3.5, 2.3, 3, 0.9, "$\\bigoplus$ Add", "#fadbd8", "#e74c3c"),
        (2, 0.5, 6, 1.2, "Output Feature Map\n$(C_{out}, H, W)$", "#ecf0f1", "#7f8c8d"),
    ]
    for x, y, w, h, text, fc, ec in blocks_eff:
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2", facecolor=fc, edgecolor=ec, lw=1.5)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=8.2, fontweight='bold', color="#1a252f")
        
    for y_start, y_end in [(11.5, 10.5), (9.4, 8.7), (7.6, 6.9), (5.8, 5.1), (4.0, 3.2), (2.3, 1.7)]:
        ax.annotate("", xy=(5, y_end), xytext=(5, y_start),
                    arrowprops=dict(arrowstyle="->", lw=1.5, color="#2c3e50"))
        
    ax.plot([2, 1.2, 1.2, 3.5], [12.1, 12.1, 2.75, 2.75], color="#8e44ad", lw=2, linestyle='--')
    ax.annotate("", xy=(3.5, 2.75), xytext=(1.5, 2.75),
                arrowprops=dict(arrowstyle="->", lw=2, color="#8e44ad"))
    ax.text(0.9, 7.5, "Skip Connection\n(if $C_{in}=C_{out}$)", color="#8e44ad", fontsize=8.5, fontweight='bold', rotation=90, va='center')
    ax.text(5, -0.4, "Total Params: 4.0M | Latency: 60s\nHigh Accuracy-to-FLOP Ratio", ha='center', fontsize=8.5, color="#555555")

    # -------------------------------------------------------------
    # (C) MobileNet-V2 Inverted Residual
    # -------------------------------------------------------------
    ax = axes[2]
    ax.set_title("(C) MobileNet-V2 Inverted Residual\n(Linear Bottleneck Edge Block)", fontsize=11, fontweight='bold', color="#1b365d")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 14)
    ax.axis('off')
    
    blocks_mob = [
        (2, 11.5, 6, 1.2, "Input Bottleneck $x$\n$(C_{low}=32, H, W)$", "#ecf0f1", "#7f8c8d"),
        (2.5, 9.3, 5, 1.2, "$1 \\times 1$ Conv (Expand $\\times 6$)\n$C_{high}=192$ + BN + ReLU6", "#d4e6f1", "#2980b9"),
        (2.5, 7.0, 5, 1.2, "$3 \\times 3$ Depthwise Conv\n$C_{high}=192$ + BN + ReLU6", "#d5f5e3", "#27ae60"),
        (2.5, 4.7, 5, 1.2, "$1 \\times 1$ Conv (Linear Project)\n$C_{out}=32$ (No Non-linearity)", "#fcf3cf", "#f39c12"),
        (3.5, 2.5, 3, 1.0, "$\\bigoplus$ Add", "#fadbd8", "#e74c3c"),
        (2, 0.5, 6, 1.2, "Output Bottleneck\n$(C_{low}=32, H, W)$", "#ecf0f1", "#7f8c8d"),
    ]
    for x, y, w, h, text, fc, ec in blocks_mob:
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2", facecolor=fc, edgecolor=ec, lw=1.5)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center', fontsize=8.5, fontweight='bold', color="#1a252f")
        
    for y_start, y_end in [(11.5, 10.5), (9.3, 8.2), (7.0, 5.9), (4.7, 3.5), (2.5, 1.7)]:
        ax.annotate("", xy=(5, y_end), xytext=(5, y_start),
                    arrowprops=dict(arrowstyle="->", lw=1.5, color="#2c3e50"))
        
    ax.plot([2, 1.2, 1.2, 3.5], [12.1, 12.1, 3.0, 3.0], color="#27ae60", lw=2, linestyle='--')
    ax.annotate("", xy=(3.5, 3.0), xytext=(1.5, 3.0),
                arrowprops=dict(arrowstyle="->", lw=2, color="#27ae60"))
    ax.text(0.9, 7.5, "Residual Connection\n(Stride=1 only)", color="#27ae60", fontsize=8.5, fontweight='bold', rotation=90, va='center')
    ax.text(5, -0.4, "Total Params: 2.2M | Latency: 21s\nMinimal Latency for Edge Devices", ha='center', fontsize=8.5, color="#555555")

    plt.tight_layout(rect=[0, 0.05, 1, 0.95])
    plt.savefig("report_assets/fig4_4_backbone_comparison.png", dpi=220)
    plt.close()
    print("[SUCCESS] report_assets/fig4_4_backbone_comparison.png generated.")


# =============================================================================
# 3. FIG 6.1: DECISION TREE FLOWCHART FOR PRACTITIONERS
# =============================================================================
def generate_decision_flowchart_figure():
    print("[+] Generating fig6_1_decision_flowchart.png...")
    fig, ax = plt.subplots(figsize=(13, 8), dpi=220)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    ax.text(50, 96, "Transfer Learning Adaptation Strategy Decision Framework",
            fontsize=15, fontweight='bold', ha='center', color="#1b365d")
    
    # Root Node
    root_box = patches.FancyBboxPatch((35, 83), 30, 8, boxstyle="round,pad=0.3", facecolor="#1b365d", edgecolor="#0e2341", lw=2)
    ax.add_patch(root_box)
    ax.text(50, 87, "Evaluate Target Dataset Domain Distance\n(Relative to ImageNet Natural Photos)",
            ha='center', va='center', color='white', fontsize=10, fontweight='bold')
    
    # Level 1 Splits: Near vs Far
    # Left: Near-Domain
    near_box = patches.FancyBboxPatch((10, 66), 32, 9, boxstyle="round,pad=0.3", facecolor="#d4e6f1", edgecolor="#2980b9", lw=1.8)
    ax.add_patch(near_box)
    ax.text(26, 70.5, "NEAR-DOMAIN\n(Natural Objects, Consumer Photos, CIFAR-10)",
            ha='center', va='center', color='#1b365d', fontsize=9.5, fontweight='bold')
    
    # Right: Far-Domain
    far_box = patches.FancyBboxPatch((58, 66), 32, 9, boxstyle="round,pad=0.3", facecolor="#f5eef8", edgecolor="#8e44ad", lw=1.8)
    ax.add_patch(far_box)
    ax.text(74, 70.5, "FAR-DOMAIN / OOD\n(Histology, Radiology, SAR, Thermal)",
            ha='center', va='center', color='#4a235a', fontsize=9.5, fontweight='bold')
    
    # Arrows from root
    ax.annotate("", xy=(26, 75), xytext=(42, 83), arrowprops=dict(arrowstyle="->", lw=2, color="#2980b9"))
    ax.text(32, 80, "High Visual Overlap", color="#2980b9", fontsize=8.5, fontweight='bold')
    
    ax.annotate("", xy=(74, 75), xytext=(58, 83), arrowprops=dict(arrowstyle="->", lw=2, color="#8e44ad"))
    ax.text(67, 80, "Severe Distribution Shift", color="#8e44ad", fontsize=8.5, fontweight='bold')

    # Sub-branches Near Domain
    # Small data
    n_small = patches.FancyBboxPatch((3, 45), 21, 13, boxstyle="round,pad=0.2", facecolor="#eafaf1", edgecolor="#27ae60", lw=1.5)
    ax.add_patch(n_small)
    ax.text(13.5, 51.5, "Data Size: Small (<5K)\n\n"
                        "STRATEGY:\n"
                        "FEATURE EXTRACTION\n"
                        "(Frozen Backbone)\n\n"
                        "Arch: MobileNet-V2 / ResNet-18\n"
                        "Prevent Overfitting | Fast",
            ha='center', va='center', color='#145a32', fontsize=7.8, fontweight='bold')
    
    # Large data
    n_large = patches.FancyBboxPatch((26, 45), 21, 13, boxstyle="round,pad=0.2", facecolor="#e8f8f5", edgecolor="#16a085", lw=1.5)
    ax.add_patch(n_large)
    ax.text(36.5, 51.5, "Data Size: Large (>10K)\n\n"
                        "STRATEGY:\n"
                        "PARTIAL / FULL FINETUNE\n"
                        "(Diff LR: $10^{-4}$ / $10^{-3}$)\n\n"
                        "Arch: ResNet-50 / EfficientNet\n"
                        "Peak Accuracy (>70%)",
            ha='center', va='center', color='#0e6251', fontsize=7.8, fontweight='bold')
    
    ax.annotate("", xy=(13.5, 58), xytext=(20, 66), arrowprops=dict(arrowstyle="->", lw=1.5, color="#27ae60"))
    ax.annotate("", xy=(36.5, 58), xytext=(32, 66), arrowprops=dict(arrowstyle="->", lw=1.5, color="#16a085"))

    # Sub-branches Far Domain
    # Compute-constrained / Small
    f_small = patches.FancyBboxPatch((53, 45), 21, 13, boxstyle="round,pad=0.2", facecolor="#fef9e7", edgecolor="#f39c12", lw=1.5)
    ax.add_patch(f_small)
    ax.text(63.5, 51.5, "Constrained Compute / Small\n\n"
                        "STRATEGY:\n"
                        "PARTIAL FINETUNE\n"
                        "(Retrain Layer 4 Only)\n\n"
                        "Arch: ResNet-50 / MobileNet\n"
                        "Best Accuracy: 64.67%\n"
                        "Saves 46% Training Time",
            ha='center', va='center', color='#7d6608', fontsize=7.8, fontweight='bold')

    # Large Far-Domain
    f_large = patches.FancyBboxPatch((76, 45), 21, 13, boxstyle="round,pad=0.2", facecolor="#fdedec", edgecolor="#c0392b", lw=1.5)
    ax.add_patch(f_large)
    ax.text(86.5, 51.5, "Abundant Data (>50K)\n\n"
                        "STRATEGY:\n"
                        "FULL FINETUNE\n"
                        "(Warmup + Diff LR)\n\n"
                        "Arch: ResNet-50 / ConvNeXt\n"
                        "Mandatory (CKA Drift < 0.50)\n"
                        "Deep filters must adapt",
            ha='center', va='center', color='#78281f', fontsize=7.8, fontweight='bold')

    ax.annotate("", xy=(63.5, 58), xytext=(70, 66), arrowprops=dict(arrowstyle="->", lw=1.5, color="#f39c12"))
    ax.annotate("", xy=(86.5, 58), xytext=(78, 66), arrowprops=dict(arrowstyle="->", lw=1.5, color="#c0392b"))

    # Bottom Warnings and Heuristic Callouts
    warn_box1 = patches.FancyBboxPatch((5, 12), 42, 23, boxstyle="round,pad=0.3", facecolor="#fadbd8", edgecolor="#e74c3c", lw=1.5)
    ax.add_patch(warn_box1)
    ax.text(26, 23.5, "CRITICAL WARNING: NEVER USE PURE FEATURE EXTRACTION IN FAR DOMAINS\n\n"
                      "• ImageNet deep features are hyper-specialized for macro-objects.\n"
                      "• On PathMNIST, frozen ResNet-50 collapsed to 28.00%.\n"
                      "• Freezing deep layers causes severe representational bottlenecking.\n"
                      "• Retraining at least the deep residual block is strictly mandatory.",
            ha='center', va='center', color='#922b21', fontsize=8.2, fontweight='bold')

    warn_box2 = patches.FancyBboxPatch((53, 12), 42, 23, boxstyle="round,pad=0.3", facecolor="#d5f5e3", edgecolor="#27ae60", lw=1.5)
    ax.add_patch(warn_box2)
    ax.text(74, 23.5, "PRACTITIONER GOLDEN RULE: MOBILENET-V2 FOR EDGE DEPLOYMENT\n\n"
                      "• Delivers 56.00% (CIFAR) and 53.33% (PathMNIST) under partial fine-tuning.\n"
                      "• Requires only 2.2 Million parameters (vs 23.5M for ResNet-50).\n"
                      "• Cuts training epoch latency by over 83% (21s vs 128s).\n"
                      "• Superior parameter efficiency across all cross-domain sweeps.",
            ha='center', va='center', color='#145a32', fontsize=8.2, fontweight='bold')

    plt.tight_layout()
    plt.savefig("report_assets/fig6_1_decision_flowchart.png", dpi=220)
    plt.close()
    print("[SUCCESS] report_assets/fig6_1_decision_flowchart.png generated.")

if __name__ == "__main__":
    generate_dataset_domains_figure()
    generate_backbone_comparison_figure()
    generate_decision_flowchart_figure()
