import pandas as pd
import numpy as np


# Input file created in Task 2
input_file = "data/trends_clean.csv"

# Output file for Task 4
output_file = "data/trends_analysed.csv"


# ---------------------------------
# 1. LOAD AND EXPLORE THE DATA
# ---------------------------------

# Load the cleaned CSV into a Pandas DataFrame
df = pd.read_csv(input_file)

print(f"Loaded data: {df.shape}")

print("\nFirst 5 rows:")
print(df.head())


# Calculate average score and comments
average_score = df["score"].mean()
average_comments = df["num_comments"].mean()

print(f"\nAverage score   : {average_score:.2f}")
print(f"Average comments: {average_comments:.2f}")


# ---------------------------------
# 2. ANALYSIS USING NUMPY
# ---------------------------------

# Convert score column into a NumPy array
scores = df["score"].to_numpy()


# Calculate statistics using NumPy
mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)
max_score = np.max(scores)
min_score = np.min(scores)


print("\n--- NumPy Stats ---")

print(f"Mean score   : {mean_score:.2f}")
print(f"Median score : {median_score:.2f}")
print(f"Std deviation: {std_score:.2f}")
print(f"Max score    : {max_score}")
print(f"Min score    : {min_score}")


# ---------------------------------
# FIND CATEGORY WITH MOST STORIES
# ---------------------------------

category_counts = df["category"].value_counts()

# Find the highest category count
max_count = category_counts.max()

# Find all categories having that highest count
most_common_categories = category_counts[
    category_counts == max_count
].index.tolist()


# Handle both single winner and tie cases
if len(most_common_categories) == 1:
    print(
        f"\nMost stories in: "
        f"{most_common_categories[0]} "
        f"({max_count} stories)"
    )
else:
    print(
        f"\nMost stories in: "
        f"{', '.join(most_common_categories)} "
        f"({max_count} stories each)"
    )


# ---------------------------------
# FIND MOST COMMENTED STORY
# ---------------------------------

# Get the row index having the highest num_comments
most_commented_index = df["num_comments"].idxmax()

# Get the complete row
most_commented_story = df.loc[most_commented_index]


print(
    f'\nMost commented story: '
    f'"{most_commented_story["title"]}" '
    f'— {most_commented_story["num_comments"]} comments'
)


# ---------------------------------
# 3. ADD NEW COLUMNS
# ---------------------------------

# Engagement shows the amount of discussion per upvote
df["engagement"] = (
    df["num_comments"] / (df["score"] + 1)
)


# Mark stories with score greater than average as popular
df["is_popular"] = (
    df["score"] > average_score
)


# Display first few rows with the new columns
print("\nData with new columns:")

print(
    df[
        [
            "title",
            "score",
            "num_comments",
            "engagement",
            "is_popular"
        ]
    ].head()
)


# ---------------------------------
# 4. SAVE THE ANALYSED DATA
# ---------------------------------

df.to_csv(output_file, index=False)

print(f"\nSaved to {output_file}")