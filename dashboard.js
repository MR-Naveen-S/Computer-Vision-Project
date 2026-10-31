/**
 * Transfer Learning Empirical Benchmark - Interactive Dashboard Engine
 * Vanilla JavaScript (ES6+) with Chart.js Integration
 */

// ============================================================================
// 1. Core Benchmark Experimental Dataset (24 Configurations)
// ============================================================================
const BENCHMARK_DATA = [
  {
    dataset: "cifar10",
    domain: "near",
    model: "resnet50",
    strategy: "scratch",
    accuracy: 14.67,
    f1: 0.0517,
    best_epoch: 1,
    avg_epoch_time: 64.41,
    total_time: 128.82,
    trainable_params: 23528522,
    total_params: 23528522,
    delta: 0.0
  },
  {
    dataset: "cifar10",
    domain: "near",
    model: "resnet50",
    strategy: "feature_extraction",
    accuracy: 61.33,
    f1: 0.5741,
    best_epoch: 2,
    avg_epoch_time: 30.95,
    total_time: 61.89,
    trainable_params: 20490,
    total_params: 23528522,
    delta: 46.66
  },
  {
    dataset: "cifar10",
    domain: "near",
    model: "resnet50",
    strategy: "partial_finetune",
    accuracy: 69.33,
    f1: 0.6913,
    best_epoch: 2,
    avg_epoch_time: 35.29,
    total_time: 70.57,
    trainable_params: 14985226,
    total_params: 23528522,
    delta: 54.66
  },
  {
    dataset: "cifar10",
    domain: "near",
    model: "resnet50",
    strategy: "full_finetune",
    accuracy: 70.67,
    f1: 0.6819,
    best_epoch: 2,
    avg_epoch_time: 63.15,
    total_time: 126.30,
    trainable_params: 23528522,
    total_params: 23528522,
    delta: 56.00
  },
  {
    dataset: "cifar10",
    domain: "near",
    model: "efficientnet_b0",
    strategy: "scratch",
    accuracy: 5.33,
    f1: 0.0054,
    best_epoch: 1,
    avg_epoch_time: 30.16,
    total_time: 60.32,
    trainable_params: 4020358,
    total_params: 4020358,
    delta: 0.0
  },
  {
    dataset: "cifar10",
    domain: "near",
    model: "efficientnet_b0",
    strategy: "feature_extraction",
    accuracy: 21.33,
    f1: 0.1784,
    best_epoch: 2,
    avg_epoch_time: 11.63,
    total_time: 23.26,
    trainable_params: 12810,
    total_params: 4020358,
    delta: 16.00
  },
  {
    dataset: "cifar10",
    domain: "near",
    model: "efficientnet_b0",
    strategy: "partial_finetune",
    accuracy: 60.67,
    f1: 0.5938,
    best_epoch: 2,
    avg_epoch_time: 14.59,
    total_time: 29.18,
    trainable_params: 3168550,
    total_params: 4020358,
    delta: 55.34
  },
  {
    dataset: "cifar10",
    domain: "near",
    model: "efficientnet_b0",
    strategy: "full_finetune",
    accuracy: 42.67,
    f1: 0.3917,
    best_epoch: 2,
    avg_epoch_time: 30.40,
    total_time: 60.79,
    trainable_params: 4020358,
    total_params: 4020358,
    delta: 37.34
  },
  {
    dataset: "cifar10",
    domain: "near",
    model: "mobilenet_v2",
    strategy: "scratch",
    accuracy: 11.33,
    f1: 0.0231,
    best_epoch: 2,
    avg_epoch_time: 24.76,
    total_time: 49.52,
    trainable_params: 2236682,
    total_params: 2236682,
    delta: 0.0
  },
  {
    dataset: "cifar10",
    domain: "near",
    model: "mobilenet_v2",
    strategy: "feature_extraction",
    accuracy: 41.33,
    f1: 0.3874,
    best_epoch: 2,
    avg_epoch_time: 10.64,
    total_time: 21.28,
    trainable_params: 12810,
    total_params: 2236682,
    delta: 30.00
  },
  {
    dataset: "cifar10",
    domain: "near",
    model: "mobilenet_v2",
    strategy: "partial_finetune",
    accuracy: 56.00,
    f1: 0.5347,
    best_epoch: 2,
    avg_epoch_time: 10.61,
    total_time: 21.22,
    trainable_params: 12810,
    total_params: 2236682,
    delta: 44.67
  },
  {
    dataset: "cifar10",
    domain: "near",
    model: "mobilenet_v2",
    strategy: "full_finetune",
    accuracy: 55.33,
    f1: 0.5200,
    best_epoch: 2,
    avg_epoch_time: 24.58,
    total_time: 49.16,
    trainable_params: 2236682,
    total_params: 2236682,
    delta: 44.00
  },
  {
    dataset: "pathmnist",
    domain: "far",
    model: "resnet50",
    strategy: "scratch",
    accuracy: 14.00,
    f1: 0.1471,
    best_epoch: 2,
    avg_epoch_time: 64.40,
    total_time: 128.81,
    trainable_params: 23526473,
    total_params: 23526473,
    delta: 0.0
  },
  {
    dataset: "pathmnist",
    domain: "far",
    model: "resnet50",
    strategy: "feature_extraction",
    accuracy: 28.00,
    f1: 0.1953,
    best_epoch: 1,
    avg_epoch_time: 19.28,
    total_time: 19.28,
    trainable_params: 18441,
    total_params: 23526473,
    delta: 14.00
  },
  {
    dataset: "pathmnist",
    domain: "far",
    model: "resnet50",
    strategy: "partial_finetune",
    accuracy: 64.67,
    f1: 0.6327,
    best_epoch: 2,
    avg_epoch_time: 34.61,
    total_time: 69.23,
    trainable_params: 14983177,
    total_params: 23526473,
    delta: 50.67
  },
  {
    dataset: "pathmnist",
    domain: "far",
    model: "resnet50",
    strategy: "full_finetune",
    accuracy: 51.33,
    f1: 0.4272,
    best_epoch: 2,
    avg_epoch_time: 63.99,
    total_time: 127.98,
    trainable_params: 23526473,
    total_params: 23526473,
    delta: 37.33
  },
  {
    dataset: "pathmnist",
    domain: "far",
    model: "efficientnet_b0",
    strategy: "scratch",
    accuracy: 6.00,
    f1: 0.0068,
    best_epoch: 1,
    avg_epoch_time: 30.49,
    total_time: 60.97,
    trainable_params: 4019077,
    total_params: 4019077,
    delta: 0.0
  },
  {
    dataset: "pathmnist",
    domain: "far",
    model: "efficientnet_b0",
    strategy: "feature_extraction",
    accuracy: 41.33,
    f1: 0.3574,
    best_epoch: 2,
    avg_epoch_time: 11.98,
    total_time: 23.97,
    trainable_params: 11529,
    total_params: 4019077,
    delta: 35.33
  },
  {
    dataset: "pathmnist",
    domain: "far",
    model: "efficientnet_b0",
    strategy: "partial_finetune",
    accuracy: 31.33,
    f1: 0.2388,
    best_epoch: 1,
    avg_epoch_time: 15.30,
    total_time: 30.61,
    trainable_params: 3167269,
    total_params: 4019077,
    delta: 25.33
  },
  {
    dataset: "pathmnist",
    domain: "far",
    model: "efficientnet_b0",
    strategy: "full_finetune",
    accuracy: 33.33,
    f1: 0.2874,
    best_epoch: 2,
    avg_epoch_time: 31.07,
    total_time: 62.15,
    trainable_params: 4019077,
    total_params: 4019077,
    delta: 27.33
  },
  {
    dataset: "pathmnist",
    domain: "far",
    model: "mobilenet_v2",
    strategy: "scratch",
    accuracy: 9.33,
    f1: 0.0159,
    best_epoch: 1,
    avg_epoch_time: 24.80,
    total_time: 49.59,
    trainable_params: 2235401,
    total_params: 2235401,
    delta: 0.0
  },
  {
    dataset: "pathmnist",
    domain: "far",
    model: "mobilenet_v2",
    strategy: "feature_extraction",
    accuracy: 46.67,
    f1: 0.3555,
    best_epoch: 2,
    avg_epoch_time: 10.64,
    total_time: 21.28,
    trainable_params: 11529,
    total_params: 2235401,
    delta: 37.34
  },
  {
    dataset: "pathmnist",
    domain: "far",
    model: "mobilenet_v2",
    strategy: "partial_finetune",
    accuracy: 53.33,
    f1: 0.4359,
    best_epoch: 2,
    avg_epoch_time: 10.64,
    total_time: 21.29,
    trainable_params: 11529,
    total_params: 2235401,
    delta: 44.00
  },
  {
    dataset: "pathmnist",
    domain: "far",
    model: "mobilenet_v2",
    strategy: "full_finetune",
    accuracy: 52.67,
    f1: 0.4040,
    best_epoch: 2,
    avg_epoch_time: 24.86,
    total_time: 49.71,
    trainable_params: 2235401,
    total_params: 2235401,
    delta: 43.34
  }
];

// CKA Layer-wise Drift Similarity Data
const CKA_DATA = {
  stages: ["Stage 1 (Low)", "Stage 2 (Mid-Low)", "Stage 3 (Mid-High)", "Stage 4 (Deep)"],
  cifar10: {
    resnet50: [0.942, 0.887, 0.764, 0.685],
    mobilenet_v2: [0.931, 0.864, 0.742, 0.651],
    efficientnet_b0: [0.915, 0.829, 0.718, 0.612]
  },
  pathmnist: {
    resnet50: [0.918, 0.781, 0.584, 0.482],
    mobilenet_v2: [0.892, 0.735, 0.541, 0.463],
    efficientnet_b0: [0.874, 0.698, 0.512, 0.421]
  },
  random_scratch: [0.048, 0.052, 0.071, 0.064]
};

// ============================================================================
// 2. Global State & UI Filters
// ============================================================================
const state = {
  dataset: "all",      // 'all' | 'cifar10' | 'pathmnist'
  model: "all",        // 'all' | 'resnet50' | 'efficientnet_b0' | 'mobilenet_v2'
  strategy: "all",     // 'all' | 'scratch' | 'feature_extraction' | 'partial_finetune' | 'full_finetune'
  metric: "accuracy",  // 'accuracy' | 'f1' | 'time'
  searchQuery: "",
  sortColumn: "accuracy",
  sortAscending: false
};

let mainChartInstance = null;
let deltaChartInstance = null;
let ckaChartInstance = null;

// ============================================================================
// 3. Helper Functions
// ============================================================================
function formatModelName(model) {
  switch (model) {
    case "resnet50": return "ResNet-50";
    case "efficientnet_b0": return "EfficientNet-B0";
    case "mobilenet_v2": return "MobileNet-V2";
    default: return model;
  }
}

function formatStrategy(strat) {
  switch (strat) {
    case "scratch": return "Random Scratch";
    case "feature_extraction": return "Feature Extraction";
    case "partial_finetune": return "Partial Fine-Tune";
    case "full_finetune": return "Full Fine-Tune";
    default: return strat;
  }
}

function formatDataset(ds) {
  switch (ds) {
    case "cifar10": return "CIFAR-10 (Near)";
    case "pathmnist": return "PathMNIST (Far)";
    default: return ds.toUpperCase();
  }
}

function formatParams(num) {
  if (num >= 1e6) {
    return (num / 1e6).toFixed(2) + "M";
  } else if (num >= 1e3) {
    return (num / 1e3).toFixed(1) + "K";
  }
  return num.toString();
}

// ============================================================================
// 4. Data Filtering Logic
// ============================================================================
function getFilteredData() {
  return BENCHMARK_DATA.filter(item => {
    if (state.dataset !== "all" && item.dataset !== state.dataset) return false;
    if (state.model !== "all" && item.model !== state.model) return false;
    if (state.strategy !== "all" && item.strategy !== state.strategy) return false;
    if (state.searchQuery) {
      const q = state.searchQuery.toLowerCase();
      const match = 
        item.dataset.toLowerCase().includes(q) ||
        item.model.toLowerCase().includes(q) ||
        item.strategy.toLowerCase().includes(q) ||
        item.domain.toLowerCase().includes(q);
      if (!match) return false;
    }
    return true;
  });
}

// ============================================================================
// 5. Chart.js Implementations
// ============================================================================
function initCharts() {
  initMainChart();
  initDeltaChart();
  initCkaDriftChart();
}

function initMainChart() {
  const ctx = document.getElementById("mainBenchmarkChart");
  if (!ctx) return;

  const isDark = document.documentElement.getAttribute("data-theme") !== "light";
  const gridColor = isDark ? "rgba(255, 255, 255, 0.08)" : "rgba(0, 0, 0, 0.08)";
  const textColor = isDark ? "#94a3b8" : "#475569";

  const chartData = prepareMainChartData();

  if (mainChartInstance) mainChartInstance.destroy();

  mainChartInstance = new Chart(ctx, {
    type: "bar",
    data: chartData,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "top",
          labels: {
            color: textColor,
            font: { family: "Inter", size: 12, weight: 600 }
          }
        },
        tooltip: {
          backgroundColor: isDark ? "rgba(15, 23, 42, 0.95)" : "rgba(255, 255, 255, 0.95)",
          titleColor: isDark ? "#f8fafc" : "#0f172a",
          bodyColor: isDark ? "#cbd5e1" : "#334155",
          borderColor: isDark ? "rgba(255,255,255,0.15)" : "rgba(0,0,0,0.15)",
          borderWidth: 1,
          padding: 12,
          callbacks: {
            label: function(context) {
              const val = context.parsed.y;
              if (state.metric === "accuracy") return ` ${context.dataset.label}: ${val.toFixed(2)}% Top-1`;
              if (state.metric === "f1") return ` ${context.dataset.label}: ${val.toFixed(4)} Macro-F1`;
              return ` ${context.dataset.label}: ${val.toFixed(1)}s / epoch`;
            }
          }
        }
      },
      scales: {
        x: {
          grid: { color: gridColor },
          ticks: { color: textColor, font: { family: "Inter", size: 11, weight: 500 } }
        },
        y: {
          grid: { color: gridColor },
          ticks: {
            color: textColor,
            callback: function(value) {
              if (state.metric === "accuracy") return value + "%";
              if (state.metric === "f1") return value.toFixed(2);
              return value + "s";
            }
          },
          suggestedMax: state.metric === "accuracy" ? 80 : (state.metric === "f1" ? 0.8 : 70)
        }
      }
    }
  });
}

function prepareMainChartData() {
  const models = ["resnet50", "efficientnet_b0", "mobilenet_v2"];
  const strategies = ["scratch", "feature_extraction", "partial_finetune", "full_finetune"];
  const strategyColors = {
    scratch: "#ef4444",
    feature_extraction: "#3b82f6",
    partial_finetune: "#8b5cf6",
    full_finetune: "#10b981"
  };

  // Generate labels based on active dataset filter
  let labels = [];
  if (state.dataset === "all" || state.dataset === "cifar10") {
    models.forEach(m => labels.push(`${formatModelName(m)} [CIFAR-10]`));
  }
  if (state.dataset === "all" || state.dataset === "pathmnist") {
    models.forEach(m => labels.push(`${formatModelName(m)} [PathMNIST]`));
  }

  const datasets = strategies.map(strat => {
    const dataValues = [];

    // CIFAR-10 block
    if (state.dataset === "all" || state.dataset === "cifar10") {
      models.forEach(m => {
        const found = BENCHMARK_DATA.find(d => d.dataset === "cifar10" && d.model === m && d.strategy === strat);
        if (found) {
          if (state.metric === "accuracy") dataValues.push(found.accuracy);
          else if (state.metric === "f1") dataValues.push(found.f1);
          else dataValues.push(found.avg_epoch_time);
        } else {
          dataValues.push(0);
        }
      });
    }

    // PathMNIST block
    if (state.dataset === "all" || state.dataset === "pathmnist") {
      models.forEach(m => {
        const found = BENCHMARK_DATA.find(d => d.dataset === "pathmnist" && d.model === m && d.strategy === strat);
        if (found) {
          if (state.metric === "accuracy") dataValues.push(found.accuracy);
          else if (state.metric === "f1") dataValues.push(found.f1);
          else dataValues.push(found.avg_epoch_time);
        } else {
          dataValues.push(0);
        }
      });
    }

    return {
      label: formatStrategy(strat),
      data: dataValues,
      backgroundColor: strategyColors[strat],
      borderRadius: 4,
      borderSkipped: false
    };
  });

  return { labels, datasets };
}

function initDeltaChart() {
  const ctx = document.getElementById("deltaChart");
  if (!ctx) return;

  const isDark = document.documentElement.getAttribute("data-theme") !== "light";
  const gridColor = isDark ? "rgba(255, 255, 255, 0.08)" : "rgba(0, 0, 0, 0.08)";
  const textColor = isDark ? "#94a3b8" : "#475569";

  // Filter transfer configurations (exclude scratch baseline)
  const transferRuns = BENCHMARK_DATA.filter(d => d.strategy !== "scratch");
  
  // Group by (Model + Strategy) and show CIFAR-10 vs PathMNIST
  const labels = [
    "R50 Feature", "R50 Partial", "R50 Full",
    "EffB0 Feature", "EffB0 Partial", "EffB0 Full",
    "MNV2 Feature", "MNV2 Partial", "MNV2 Full"
  ];

  const cifarDeltas = [46.66, 54.66, 56.00, 16.00, 55.34, 37.34, 30.00, 44.67, 44.00];
  const pathDeltas = [14.00, 50.67, 37.33, 35.33, 25.33, 27.33, 37.34, 44.00, 43.34];

  if (deltaChartInstance) deltaChartInstance.destroy();

  deltaChartInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels: labels,
      datasets: [
        {
          label: "CIFAR-10 (Near Domain)",
          data: cifarDeltas,
          backgroundColor: "#10b981",
          borderRadius: 4
        },
        {
          label: "PathMNIST (Far Domain)",
          data: pathDeltas,
          backgroundColor: "#f59e0b",
          borderRadius: 4
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "top",
          labels: { color: textColor, font: { family: "Inter", size: 11, weight: 600 } }
        },
        tooltip: {
          callbacks: {
            label: (ctx) => ` Δ Transfer: +${ctx.parsed.y.toFixed(2)}%`
          }
        }
      },
      scales: {
        x: {
          grid: { color: gridColor },
          ticks: { color: textColor, font: { family: "Inter", size: 9 } }
        },
        y: {
          grid: { color: gridColor },
          ticks: {
            color: textColor,
            callback: (val) => `+${val}%`
          },
          suggestedMax: 65
        }
      }
    }
  });
}

function initCkaDriftChart() {
  const ctx = document.getElementById("ckaDriftChart");
  if (!ctx) return;

  const isDark = document.documentElement.getAttribute("data-theme") !== "light";
  const gridColor = isDark ? "rgba(255, 255, 255, 0.08)" : "rgba(0, 0, 0, 0.08)";
  const textColor = isDark ? "#94a3b8" : "#475569";

  if (ckaChartInstance) ckaChartInstance.destroy();

  ckaChartInstance = new Chart(ctx, {
    type: "line",
    data: {
      labels: CKA_DATA.stages,
      datasets: [
        {
          label: "ResNet-50 CIFAR-10 (Near)",
          data: CKA_DATA.cifar10.resnet50,
          borderColor: "#10b981",
          backgroundColor: "rgba(16, 185, 129, 0.1)",
          tension: 0.35,
          borderWidth: 2.5,
          pointRadius: 5
        },
        {
          label: "ResNet-50 PathMNIST (Far)",
          data: CKA_DATA.pathmnist.resnet50,
          borderColor: "#f59e0b",
          backgroundColor: "rgba(245, 158, 11, 0.1)",
          tension: 0.35,
          borderWidth: 2.5,
          pointRadius: 5
        },
        {
          label: "MobileNet-V2 PathMNIST (Far)",
          data: CKA_DATA.pathmnist.mobilenet_v2,
          borderColor: "#ec4899",
          backgroundColor: "transparent",
          borderDash: [5, 5],
          tension: 0.35,
          borderWidth: 2,
          pointRadius: 4
        },
        {
          label: "Random Scratch Baseline (Zero Drift)",
          data: CKA_DATA.random_scratch,
          borderColor: "#ef4444",
          backgroundColor: "transparent",
          borderDash: [3, 3],
          borderWidth: 1.5,
          pointRadius: 3
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "top",
          labels: { color: textColor, font: { family: "Inter", size: 11, weight: 600 } }
        },
        tooltip: {
          callbacks: {
            label: (ctx) => ` ${ctx.dataset.label}: ${ctx.parsed.y.toFixed(3)} CKA`
          }
        }
      },
      scales: {
        x: {
          grid: { color: gridColor },
          ticks: { color: textColor, font: { family: "Inter", size: 11 } }
        },
        y: {
          min: 0,
          max: 1.0,
          grid: { color: gridColor },
          ticks: { color: textColor, callback: (v) => v.toFixed(2) }
        }
      }
    }
  });
}

// ============================================================================
// 6. Dynamic Benchmark Data Table Engine
// ============================================================================
function renderTable() {
  const tbody = document.getElementById("benchmarkTableBody");
  if (!tbody) return;

  const data = getFilteredData();

  // Sorting
  data.sort((a, b) => {
    let valA = a[state.sortColumn];
    let valB = b[state.sortColumn];

    if (typeof valA === "string") {
      return state.sortAscending ? valA.localeCompare(valB) : valB.localeCompare(valA);
    }
    return state.sortAscending ? valA - valB : valB - valA;
  });

  tbody.innerHTML = "";

  if (data.length === 0) {
    tbody.innerHTML = `<tr><td colspan="9" style="text-align: center; padding: 2rem; color: var(--text-muted);">No benchmark configurations matched the selected filters.</td></tr>`;
    return;
  }

  data.forEach(row => {
    const tr = document.createElement("tr");

    const deltaClass = row.delta > 0 ? "delta-positive" : (row.delta === 0 ? "delta-neutral" : "delta-negative");
    const deltaSign = row.delta > 0 ? "+" : "";

    tr.innerHTML = `
      <td>
        <strong>${formatModelName(row.model)}</strong>
      </td>
      <td>
        <span class="domain-badge ${row.domain}">${row.dataset.toUpperCase()}</span>
      </td>
      <td>
        <span class="strategy-badge ${row.strategy}">${formatStrategy(row.strategy)}</span>
      </td>
      <td>
        <strong style="color: var(--text-primary); font-size: 0.95rem;">${row.accuracy.toFixed(2)}%</strong>
      </td>
      <td>
        <span class="delta-badge ${deltaClass}">${deltaSign}${row.delta.toFixed(2)}%</span>
      </td>
      <td class="font-mono">
        ${row.f1.toFixed(4)}
      </td>
      <td>
        ${row.avg_epoch_time.toFixed(1)}s
      </td>
      <td>
        ${formatParams(row.trainable_params)}
      </td>
      <td>
        ${formatParams(row.total_params)}
      </td>
    `;
    tbody.appendChild(tr);
  });
}

// ============================================================================
// 7. Interactive Strategy Decision Wizard
// ============================================================================
function updateStrategyRecommendation() {
  const domain = document.getElementById("wizDomain")?.value || "near";
  const sampleSize = document.getElementById("wizSampleSize")?.value || "medium";
  const compute = document.getElementById("wizCompute")?.value || "standard";
  const paramBudget = document.getElementById("wizParams")?.value || "standard";

  let recStrategy = "Partial Fine-Tuning";
  let recModel = "ResNet-50";
  let recDesc = "";
  let expectedAcc = "65% - 72%";
  let ckaPreserve = "High (>0.85 early stages)";
  let speed = "35s / epoch";

  if (domain === "near") {
    if (compute === "high" || sampleSize === "large") {
      recStrategy = "Full Fine-Tuning (Differential LR)";
      recModel = "ResNet-50";
      recDesc = "Near-domain natural imagery benefits from adapting all layers with lower backbone LR (1e-4) and head LR (1e-3). Reaches highest overall benchmark accuracy (70.67%).";
      expectedAcc = "70.67% (Top Rank)";
      ckaPreserve = "Moderate (0.685 deep stage)";
      speed = "63.1s / epoch";
    } else if (compute === "low" || paramBudget === "edge") {
      recStrategy = "Partial Fine-Tuning";
      recModel = "MobileNet-V2";
      recDesc = "MobileNet-V2 with late-layer unfreezing delivers 56.00% accuracy with ultra-low 10.6s/epoch latency and 2.24M parameters.";
      expectedAcc = "56.00%";
      ckaPreserve = "High (0.742 mid stage)";
      speed = "10.6s / epoch (Fastest)";
    } else {
      recStrategy = "Partial Fine-Tuning";
      recModel = "EfficientNet-B0 or ResNet-50";
      recDesc = "Partial Fine-Tuning achieves 69.33% accuracy on ResNet-50 while saving 45% GPU compute compared to full backpropagation.";
      expectedAcc = "69.33%";
      ckaPreserve = "High (>0.88 early)";
      speed = "35.3s / epoch";
    }
  } else { // Far Domain (MedMNIST / PathMNIST)
    if (compute === "low" && sampleSize === "small") {
      recStrategy = "Feature Extraction (Frozen Backbone)";
      recModel = "MobileNet-V2";
      recDesc = "Avoid catastrophic distortion of general filters on tiny out-of-distribution sets. MobileNet-V2 feature extraction reaches 46.67% accuracy in just 10.6s.";
      expectedAcc = "46.67%";
      ckaPreserve = "1.000 (Exact Preservation)";
      speed = "10.6s / epoch";
    } else {
      recStrategy = "Partial Fine-Tuning (Stage 3 & 4)";
      recModel = "ResNet-50";
      recDesc = "Optimal for far-domain histopathology. Retains foundational edge/texture filters in Stage 1-2 while realigning deep domain representations. Outperforms Full Fine-Tuning by +13.34%.";
      expectedAcc = "64.67% (Best Far Domain)";
      ckaPreserve = "0.781 (Stage 2) -> 0.482 (Stage 4)";
      speed = "34.6s / epoch";
    }
  }

  const titleEl = document.getElementById("wizRecTitle");
  const descEl = document.getElementById("wizRecDesc");
  const accEl = document.getElementById("wizExpectedAcc");
  const modelEl = document.getElementById("wizRecModel");
  const ckaEl = document.getElementById("wizCkaPreserve");
  const speedEl = document.getElementById("wizSpeed");

  if (titleEl) titleEl.textContent = recStrategy;
  if (descEl) descEl.textContent = recDesc;
  if (accEl) accEl.textContent = expectedAcc;
  if (modelEl) modelEl.textContent = recModel;
  if (ckaEl) ckaEl.textContent = ckaPreserve;
  if (speedEl) speedEl.textContent = speed;
}

// ============================================================================
// 8. Modal Viewer for Architectural Diagrams
// ============================================================================
const MODAL_GALLERY_DATA = {
  fig3_1: {
    src: "report_assets/fig3_1_methodology_flowchart.png",
    title: "Figure 3.1: 7-Stage Research Methodology Flowchart",
    caption: "Comprehensive experimental workflow: Ingestion, backbone instantiation, 4 adaptation topologies, seed control, validation loops, and CKA matrix forward hook extraction."
  },
  fig4_0: {
    src: "report_assets/fig4_0_dataset_domains.png",
    title: "Figure 4.0: Cross-Domain Dataset Comparison (CIFAR-10 vs PathMNIST)",
    caption: "Side-by-side patch comparisons of natural photos vs histopathology tissue tiles, alongside RGB spectral channel density distributions demonstrating domain divergence."
  },
  fig4_1: {
    src: "report_assets/fig4_1_system_architecture.png",
    title: "Figure 4.1: Global System Architecture & Pipeline Dispatcher",
    caption: "Tri-panel schematic detailing Data Ingestion, Model Strategy Dispatcher with layer freezing controllers, and the Linear CKA Metric Engine."
  },
  fig4_2: {
    src: "report_assets/fig4_2_adaptation_strategies.png",
    title: "Figure 4.2: Four Adaptation Strategies & Layer Freezing Logic",
    caption: "Architectural comparison of Random Scratch, Feature Extraction, Partial Fine-Tuning, and Full Fine-Tuning with differential learning rates."
  },
  fig4_3: {
    src: "report_assets/fig4_3_cka_pipeline.png",
    title: "Figure 4.3: Linear CKA Mathematical Formulation & Matrix Centering",
    caption: "Gram matrix formulation K = XX^T and L = YY^T, Centering matrix H = I - 1/n 11^T, and normalized Hilbert-Schmidt Independence Criterion (HSIC)."
  },
  fig4_4: {
    src: "report_assets/fig4_4_backbone_comparison.png",
    title: "Figure 4.4: Backbone Micro-Architectural Block Topologies",
    caption: "Micro-architectural deep-dive: ResNet Bottleneck vs EfficientNet MBConv with Squeeze-and-Excitation vs MobileNet Inverted Residual block."
  },
  fig6_1: {
    src: "report_assets/fig6_1_decision_flowchart.png",
    title: "Figure 6.1: Engineering Decision Tree for Transfer Learning Selection",
    caption: "Algorithmic flowchart guiding computer vision practitioners on choosing the optimal strategy based on domain divergence, sample volume, and latency budgets."
  },
  cka_heatmap: {
    src: "results/cka_heatmap.png",
    title: "Figure 5.3: Empirical Linear CKA Matrix Heatmap",
    caption: "Empirical layer-to-layer similarity matrix comparing Pretrained ImageNet features against target representations, showing high diagonal preservation in early layers."
  }
};

function openDiagramModal(key) {
  const modal = document.getElementById("diagramModal");
  const img = document.getElementById("modalImg");
  const title = document.getElementById("modalTitle");
  const caption = document.getElementById("modalCaption");

  if (!modal || !MODAL_GALLERY_DATA[key]) return;

  const item = MODAL_GALLERY_DATA[key];
  img.src = item.src;
  img.alt = item.title;
  title.textContent = item.title;
  caption.textContent = item.caption;

  modal.classList.add("active");
  document.body.style.overflow = "hidden";
}

function closeDiagramModal() {
  const modal = document.getElementById("diagramModal");
  if (!modal) return;
  modal.classList.remove("active");
  document.body.style.overflow = "";
}

// ============================================================================
// 9. CSV Export Engine
// ============================================================================
function exportBenchmarkCSV() {
  const data = getFilteredData();
  const headers = ["Dataset", "Domain", "Model", "Strategy", "Top1_Accuracy_Pct", "Delta_vs_Scratch_Pct", "Macro_F1", "Avg_Epoch_Sec", "Trainable_Params", "Total_Params"];
  
  const rows = data.map(d => [
    d.dataset,
    d.domain,
    d.model,
    d.strategy,
    d.accuracy.toFixed(2),
    d.delta.toFixed(2),
    d.f1.toFixed(4),
    d.avg_epoch_time.toFixed(2),
    d.trainable_params,
    d.total_params
  ]);

  let csvContent = "data:text/csv;charset=utf-8," + [headers.join(","), ...rows.map(e => e.join(","))].join("\n");
  
  const encodedUri = encodeURI(csvContent);
  const link = document.createElement("a");
  link.setAttribute("href", encodedUri);
  link.setAttribute("download", `transfer_benchmark_export_${Date.now()}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

// ============================================================================
// 10. Event Listeners & Initialization
// ============================================================================
document.addEventListener("DOMContentLoaded", () => {
  // Theme Toggle
  const themeBtn = document.getElementById("themeToggleBtn");
  if (themeBtn) {
    const savedTheme = localStorage.getItem("dashboard-theme") || "dark";
    document.documentElement.setAttribute("data-theme", savedTheme);

    themeBtn.addEventListener("click", () => {
      const current = document.documentElement.getAttribute("data-theme");
      const next = current === "light" ? "dark" : "light";
      document.documentElement.setAttribute("data-theme", next);
      localStorage.setItem("dashboard-theme", next);
      initCharts();
    });
  }

  // Segmented Filter Controls
  document.querySelectorAll(".segmented-control").forEach(control => {
    control.addEventListener("click", (e) => {
      const btn = e.target.closest(".segment-btn");
      if (!btn) return;

      const group = btn.dataset.group;
      const val = btn.dataset.value;

      control.querySelectorAll(".segment-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      if (group === "dataset") state.dataset = val;
      if (group === "metric") state.metric = val;

      initMainChart();
      renderTable();
    });
  });

  // Search Input
  const searchInput = document.getElementById("tableSearchInput");
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      state.searchQuery = e.target.value;
      renderTable();
    });
  }

  // Table Column Sort
  document.querySelectorAll(".data-table th[data-sort]").forEach(th => {
    th.addEventListener("click", () => {
      const col = th.dataset.sort;
      if (state.sortColumn === col) {
        state.sortAscending = !state.sortAscending;
      } else {
        state.sortColumn = col;
        state.sortAscending = false;
      }

      document.querySelectorAll(".data-table th").forEach(h => {
        h.classList.remove("sorted-asc", "sorted-desc");
      });
      th.classList.add(state.sortAscending ? "sorted-asc" : "sorted-desc");

      renderTable();
    });
  });

  // Strategy Recommendation Selectors
  ["wizDomain", "wizSampleSize", "wizCompute", "wizParams"].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.addEventListener("change", updateStrategyRecommendation);
  });

  // CSV Export Button
  const exportBtn = document.getElementById("exportCsvBtn");
  if (exportBtn) exportBtn.addEventListener("click", exportBenchmarkCSV);

  // Gallery Card Click
  document.querySelectorAll(".gallery-card[data-diagram]").forEach(card => {
    card.addEventListener("click", () => {
      const diagramKey = card.dataset.diagram;
      openDiagramModal(diagramKey);
    });
  });

  // Modal Close
  const modalCloseBtn = document.getElementById("modalCloseBtn");
  const modalOverlay = document.getElementById("diagramModal");
  if (modalCloseBtn) modalCloseBtn.addEventListener("click", closeDiagramModal);
  if (modalOverlay) {
    modalOverlay.addEventListener("click", (e) => {
      if (e.target === modalOverlay) closeDiagramModal();
    });
  }

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeDiagramModal();
  });

  // Initial Boot
  initCharts();
  renderTable();
  updateStrategyRecommendation();
});
