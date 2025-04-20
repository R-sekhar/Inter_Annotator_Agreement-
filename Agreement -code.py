import pandas as pd


# Replace these file names with your actual Excel file names.
df_a1 = pd.read_excel('Annotator1_plumbing.xlsx')
df_a2 = pd.read_excel('Annotator2_plumbing.xlsx')


df_a1.columns = df_a1.columns.str.strip()
df_a2.columns = df_a2.columns.str.strip()



if 'Argument' not in df_a1.columns and 'Arguments' in df_a1.columns:
    df_a1.rename(columns={'Arguments': 'Argument'}, inplace=True)
if 'Argument2' not in df_a1.columns and 'Arguments2' in df_a1.columns:
    df_a1.rename(columns={'Arguments2': 'Argument2'}, inplace=True)
if 'Sense' not in df_a1.columns and 'Senses' in df_a1.columns:
    df_a1.rename(columns={'Senses': 'Sense'}, inplace=True)
if 'Sense2' not in df_a1.columns and 'Senses2' in df_a1.columns:
    df_a1.rename(columns={'Senses2': 'Sense2'}, inplace=True)


if 'Argument' not in df_a2.columns and 'Arguments' in df_a2.columns:
    df_a2.rename(columns={'Arguments': 'Argument'}, inplace=True)
if 'Argument2' not in df_a2.columns and 'Arguments2' in df_a2.columns:
    df_a2.rename(columns={'Arguments2': 'Argument2'}, inplace=True)
if 'Sense' not in df_a2.columns and 'Senses' in df_a2.columns:
    df_a2.rename(columns={'Senses': 'Sense'}, inplace=True)
if 'Sense2' not in df_a2.columns and 'Senses2' in df_a2.columns:
    df_a2.rename(columns={'Senses2': 'Sense2'}, inplace=True)


df_a1['order'] = df_a1.index


df_a1_long = pd.DataFrame({
    "Argument": pd.concat([df_a1["Argument"], df_a1["Argument2"]], ignore_index=True),
    "Sense_a1": pd.concat([df_a1["Sense"], df_a1["Sense2"]], ignore_index=True)
})
df_a2_long = pd.DataFrame({
    "Argument": pd.concat([df_a2["Argument"], df_a2["Argument2"]], ignore_index=True),
    "Sense_a2": pd.concat([df_a2["Sense"], df_a2["Sense2"]], ignore_index=True)
})

# --- Step 2.1: Remove blank or missing Argument entries before merging ---
df_a1_long = df_a1_long[df_a1_long["Argument"].notna() & df_a1_long["Argument"].str.strip().ne("")]
df_a2_long = df_a2_long[df_a2_long["Argument"].notna() & df_a2_long["Argument"].str.strip().ne("")]


merged_df = pd.merge(df_a1_long, df_a2_long, on="Argument", how="outer", sort=False)


merged_df["Sense_a1"] = merged_df["Sense_a1"].fillna("N/A")
merged_df["Sense_a2"] = merged_df["Sense_a2"].fillna("N/A")

# Remove rows where both annotations are "N/A"
merged_df = merged_df[~((merged_df["Sense_a1"] == "N/A") & (merged_df["Sense_a2"] == "N/A"))]


def compute_agreement(row):
    s1 = row["Sense_a1"].lower().strip()
    s2 = row["Sense_a2"].lower().strip()
    if s1 == "n/a" or s2 == "n/a":
        return 0
    return 1 if s1 == s2 else 0

merged_df["Agreement"] = merged_df.apply(compute_agreement, axis=1)


A1_inter_A2 = merged_df['Agreement'].sum()
A1_union_A2 = len(merged_df)
accuracy = A1_inter_A2 / A1_union_A2 if A1_union_A2 > 0 else 0

precision = A1_inter_A2 / merged_df[merged_df['Sense_a1'] != "N/A"].shape[0] if merged_df['Sense_a1'].ne("N/A").any() else 0
recall = A1_inter_A2 / merged_df[merged_df['Sense_a2'] != "N/A"].shape[0] if merged_df['Sense_a2'].ne("N/A").any() else 0
f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0


print("Global Agreement Metrics:")
print(f"  Overall Agreement (row-level): {merged_df['Agreement'].mean():.2f}")
print(f"  Accuracy: {accuracy:.2f}")
print(f"  Precision: {precision:.2f}")
print(f"  Recall: {recall:.2f}")
print(f"  F1 Score: {f1:.2f}")

-
output_filename = "Results/A1 VS A2_RV_Plumbing.xlsx"
merged_df.to_excel(output_filename, index=False)
print(f"Comparison results saved to: '{output_filename}'")
