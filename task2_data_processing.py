import pandas as pd


# JSON file created in Task 1
input_file = "data/trends_20260929.json"

# CSV file that will contain the cleaned data
output_file = "data/trends_clean.csv"


# Load JSON data into a Pandas DataFrame
df = pd.read_json(input_file)

print(f"Loaded {len(df)} stories from {input_file}")


# Remove duplicate stories based on post_id
df = df.drop_duplicates(subset=["post_id"])

print("After removing duplicates:", len(df))


# Remove rows where important fields are missing
df = df.dropna(subset=["post_id", "title", "score"])

print("After removing nulls:", len(df))


# Convert score to numeric values
# Invalid values are converted to NaN
df["score"] = pd.to_numeric(
    df["score"],
    errors="coerce"
)

# Remove score values that could not be converted to numbers
df = df.dropna(subset=["score"])

# Convert score to integer
df["score"] = df["score"].astype(int)


# Convert number of comments to integer
# Missing or invalid comment counts are treated as 0
df["num_comments"] = pd.to_numeric(
    df["num_comments"],
    errors="coerce"
).fillna(0).astype(int)


# Remove stories with a score lower than 5
df = df[df["score"] >= 5]

print("After removing low scores:", len(df))


# Remove unnecessary spaces from story titles
df["title"] = df["title"].str.strip()


# Save the cleaned data as CSV
df.to_csv(output_file, index=False)

print(f"\nSaved {len(df)} rows to {output_file}")


# Print number of stories in each category
print("\nStories per category:")

category_counts = df["category"].value_counts()

print(category_counts)