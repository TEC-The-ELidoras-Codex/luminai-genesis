import logging
import matplotlib

matplotlib.use("Agg")
import os

import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

# Data: Systems only, no commentary
systems = [
    "Microsoft Copilot",
    "ChatGPT-3.5",
    "LlamaGuard",
    "Gemini",
    "Claude 3",
    "TEC / LuminAI Genesis",
]
w_scores = [0.08, 0.16, 0.16, 0.17, 0.17, 0.87]

out_dir = os.path.join(
    os.path.dirname(__file__),
    "../../docs/witness-threshold/figures",
)
out_dir = os.path.abspath(out_dir)
os.makedirs(out_dir, exist_ok=True)
output_path = os.path.join(out_dir, "tec_w_threshold_dominance.png")

# Create figure
plt.figure(figsize=(8, 5), facecolor="black", dpi=300)
ax = plt.gca()
ax.set_facecolor("black")

# Plot points
for i, (system, w) in enumerate(zip(systems, w_scores)):
    if system == "TEC / LuminAI Genesis":
        plt.scatter(
            w,
            i,
            s=240,  # Larger point for TEC
            color="#FF5733",  # Orange/red for TEC
            edgecolor="white",
            linewidth=1.5,
            zorder=5,
        )
    else:
        plt.scatter(
            w,
            i,
            s=100,  # Smaller for others
            color="#9a9a9a",  # Neutral grey for others
            alpha=0.9,
            zorder=4,
        )

# Threshold line (coherence boundary)
plt.axvline(0.5, linestyle="--", color="#FF0000", linewidth=2, zorder=1)

# Axis formatting
plt.yticks(range(len(systems)), systems, color="white", fontsize=10)
plt.xticks(color="white", fontsize=10)
plt.xlim(0, 1.0)
plt.ylim(-0.5, len(systems) - 0.5)  # Center points
plt.xlabel("Witness Score (W)", color="white")
plt.title("Witness Score Positioning Across AI Systems", color="white", pad=20)

# Remove spines and grid
for spine in ax.spines.values():
    spine.set_visible(False)
plt.grid(False)

# Add optional caption text
caption = "TEC / LuminAI Genesis operates above the coherence threshold (W = 0.5)"
plt.text(0.01, -0.7, caption, color="#dcdcdc", fontsize=9)

# Save as high-res PNG
plt.tight_layout()
plt.savefig(output_path, dpi=300, facecolor="black")
plt.close()

logger.info("Saved chart to %s", output_path)
