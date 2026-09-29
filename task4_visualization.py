import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Input file created in Task 3
input_file = "data/trends_analysed.csv"

# Folder where all chart images will be saved
output_folder = "outputs"


# ---------------------------------
# 1. LOAD DATA AND SETUP
# ---------------------------------

# Load analysed data
df = pd.read_csv(input_file)

print(f"Loaded {len(df)} stories from {input_file}")


# Create outputs folder if it does not already exist
os.makedirs(output_folder, exist_ok=True)


# The is_popular column may sometimes be read as text from CSV.
# Convert it into a proper True/False column.
df["is_popular"] = (
    df["is_popular"]
    .astype(str)
    .str.lower()
    .map({"true": True, "false": False})
)


# Function to shorten long story titles
def shorten_title(title):
    title = str(title)

    if len(title) > 50:
        return title[:47] + "..."

    return title


# ---------------------------------
# 2. CHART 1 - TOP 10 STORIES
# ---------------------------------

# Find the 10 stories with the highest score
top_10 = df.nlargest(10, "score").copy()

# Shorten titles longer than 50 characters
top_10["short_title"] = top_10["title"].apply(shorten_title)

# Sort so that the highest scoring story appears at the top
top_10 = top_10.sort_values("score")


plt.figure(figsize=(10, 6))

plt.barh(
    top_10["short_title"],
    top_10["score"]
)

plt.title("Top 10 Stories by Score")
plt.xlabel("Score")
plt.ylabel("Story Title")

plt.tight_layout()

# Save before plt.show()
plt.savefig(
    "outputs/chart1_top_stories.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()

print("Saved outputs/chart1_top_stories.png")


# ---------------------------------
# 3. CHART 2 - STORIES PER CATEGORY
# ---------------------------------

# Count the number of stories in each category
category_counts = df["category"].value_counts()

# Generate a different colour for each category
colors = plt.cm.tab10(
    np.linspace(0, 1, len(category_counts))
)


plt.figure(figsize=(8, 6))

plt.bar(
    category_counts.index,
    category_counts.values,
    color=colors
)

plt.title("Stories per Category")
plt.xlabel("Category")
plt.ylabel("Number of Stories")

plt.xticks(rotation=25)

plt.tight_layout()

# Save before plt.show()
plt.savefig(
    "outputs/chart2_categories.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()

print("Saved outputs/chart2_categories.png")


# ---------------------------------
# 4. CHART 3 - SCORE VS COMMENTS
# ---------------------------------

# Separate popular and non-popular stories
popular_stories = df[df["is_popular"] == True]
non_popular_stories = df[df["is_popular"] == False]


plt.figure(figsize=(8, 6))

# Plot non-popular stories
plt.scatter(
    non_popular_stories["score"],
    non_popular_stories["num_comments"],
    label="Non-popular",
    alpha=0.7
)

# Plot popular stories using a different colour
plt.scatter(
    popular_stories["score"],
    popular_stories["num_comments"],
    label="Popular",
    alpha=0.7
)

plt.title("Score vs Number of Comments")
plt.xlabel("Score")
plt.ylabel("Number of Comments")

plt.legend()

plt.tight_layout()

# Save before plt.show()
plt.savefig(
    "outputs/chart3_scatter.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()

print("Saved outputs/chart3_scatter.png")


# ---------------------------------
# BONUS - COMBINED DASHBOARD
# ---------------------------------

# Create a 2 x 2 dashboard
fig, axes = plt.subplots(
    2,
    2,
    figsize=(16, 11)
)


# ----- Dashboard Chart 1 -----

axes[0, 0].barh(
    top_10["short_title"],
    top_10["score"]
)

axes[0, 0].set_title("Top 10 Stories by Score")
axes[0, 0].set_xlabel("Score")
axes[0, 0].set_ylabel("Story Title")


# ----- Dashboard Chart 2 -----

axes[0, 1].bar(
    category_counts.index,
    category_counts.values,
    color=colors
)

axes[0, 1].set_title("Stories per Category")
axes[0, 1].set_xlabel("Category")
axes[0, 1].set_ylabel("Number of Stories")

axes[0, 1].tick_params(
    axis="x",
    rotation=25
)


# ----- Dashboard Chart 3 -----

axes[1, 0].scatter(
    non_popular_stories["score"],
    non_popular_stories["num_comments"],
    label="Non-popular",
    alpha=0.7
)

axes[1, 0].scatter(
    popular_stories["score"],
    popular_stories["num_comments"],
    label="Popular",
    alpha=0.7
)

axes[1, 0].set_title("Score vs Number of Comments")
axes[1, 0].set_xlabel("Score")
axes[1, 0].set_ylabel("Number of Comments")

axes[1, 0].legend()


# Fourth position is unused
axes[1, 1].axis("off")


# Overall dashboard title
fig.suptitle(
    "TrendPulse Dashboard",
    fontsize=18
)

plt.tight_layout(
    rect=[0, 0, 1, 0.96]
)

# Save dashboard before showing it
plt.savefig(
    "outputs/dashboard.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()

print("Saved outputs/dashboard.png")


print("\nAll visualizations created successfully.")