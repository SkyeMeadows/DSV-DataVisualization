import json
import os

import matplotlib as mpl # type: ignore
mpl.use("Agg")

import matplotlib.pyplot as plt # type: ignore

import numpy as np # type: ignore
import logging
import argparse
import matplotlib.ticker as ticker


# Log levels:
# - DEBUG
# - INFO
# - WARNING
# - ERROR
# - CRITICAL

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Setting up Logging
logging.basicConfig(
    filename=os.path.join(BASE_DIR, "GraphLog.txt"),
    filemode='w', 
    level=logging.DEBUG, 
    format='%(asctime)s [%(levelname)s] %(message)s', 
    datefmt='%H:%M:%S' 
)

log = logging.getLogger(__name__)

mpl.set_loglevel("warning")

log.debug("Getting file paths")
data_path = os.path.join(BASE_DIR, "data.json")
graph_path = os.path.join(BASE_DIR, "Graphs", "graph_memory.png")

# === Parse Passed Arguments ===
log.debug("Parsing Arguments")
parser = argparse.ArgumentParser(description="TBD")
parser.add_argument("--weapon_one", type=str, required=True)
parser.add_argument("--weapon_two", type=str, required=True)
parser.add_argument("--trait_one", type=str, required=True)
parser.add_argument("--trait_two", type=str, required=False)
args = parser.parse_args()

# === Sort Data ===
log.debug("Reading Weapon Data")
with open(data_path) as file:
    data = json.load(file)

log.debug("Sorting Weapon values")
sorted_weapons = sorted(
    data.items(), 
    key=lambda item: item[1].get(args.trait_one, 0), 
    reverse=False
)

# === Filtering by Arguments ===
log.debug("Filtering by Arguments - Weapon names")
chosen_weapons = [
    (name, weapon)
    for name, weapon, in sorted_weapons
    if name in {args.weapon_one, args.weapon_two}
]

log.debug("Filtering by Arguments - Traits")
chosen_traits = [args.trait_one]
if args.trait_two:
    chosen_traits.append(args.trait_two)

# === Organizing Data ===
log.debug("Isolating chosen weapons")
chosen_weapon_names = [name for name, _ in chosen_weapons]

# === Preparing to Graph ===
log.debug("Setting y_pos, bar height, and offset")
y_pos = np.arange(len(chosen_weapon_names))
total_bar_height = 0.8
bar_height = total_bar_height / len(chosen_traits)

# === Graphing ===
log.debug("Started graphing")
fig, ax1 = plt.subplots(figsize=(20,12))

ax2 = ax1.twiny()

log.debug("Gathering data for first attribute plot")
values_one = [weapon.get(chosen_traits[0]) for _, weapon in chosen_weapons]
log.debug("Checking if second attribute was chosen")
if not args.trait_two:
    log.debug("Plotting first attribute with offset")
    ax1.barh(y_pos, values_one, height=bar_height, label=chosen_traits[0], color="green")
else:
    log.debug("No second attribute, plotting single bar per weapon")
    ax1.barh(y_pos + (bar_height / 2), values_one, height=bar_height, label=chosen_traits[0], color="green")

log.debug("Checking if second attribute was chosen")
if args.trait_two:
    log.debug("Plotting second attribute with offset")
    values_two = [weapon.get(chosen_traits[1]) for _, weapon in chosen_weapons]
    ax2.barh(y_pos - (bar_height / 2), values_two, height=bar_height, label=chosen_traits[1], color="blue")

log.debug("Formatting the graph, first axis")
ax1.spines["bottom"].set_color("green")
ax1.xaxis.label.set_color("green")
ax1.tick_params(axis="x", colors="green")
ax1.set_xlabel(chosen_traits[0])
ax1.xaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=False))
ax1.ticklabel_format(style="plain", axis="x")
ax1.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

log.debug("Checking if second attribute was chosen")
if args.trait_two:
    log.debug("Formatting the graph, second axis")
    ax2.spines["top"].set_color("blue")
    ax2.xaxis.label.set_color("blue")
    ax2.tick_params(axis="x", colors="blue")
    ax2.set_xlabel(chosen_traits[1])
    ax2.xaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=False))
    ax2.ticklabel_format(style="plain", axis="x")
    ax2.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))

log.debug("Setting y-ticks and y-labels")
ax1.set_yticks(y_pos)
ax1.set_yticklabels([name for name, _ in chosen_weapons])

lines, labels = ax1.get_legend_handles_labels()
if args.trait_two:
    lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2, loc="lower right")

log.debug("Finalizing plot and saving")
plt.title("Weapon Comparison")
plt.tight_layout()
plt.savefig(graph_path)