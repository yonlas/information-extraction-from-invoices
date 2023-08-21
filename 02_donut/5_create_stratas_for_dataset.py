# import pandas as pd
# import json
# import os

# # Load the metadata.jsonl file
# metadata_path = 'metadata/metadata.jsonl'
# with open(metadata_path, 'r') as f:
#     metadata = [json.loads(line) for line in f]

# # Convert the metadata to a DataFrame
# df = pd.DataFrame(metadata)

# # Count the number of occurrences of each unique vendor_name
# vendor_counts = df['ground_truth'].apply(lambda x: json.loads(x)['gt_parse']['vendor_name']).value_counts()

# train_counts = {}
# val_counts = {}
# test_counts = {}

# # Calculate the number of samples for each set
# for vendor, count in vendor_counts.items():
#     train_count = int(count * 0.7)
#     val_count = int(count * 0.15)
#     test_count = int(count * 0.15)

#     # Ensure at least one sample in each subset
#     if train_count < 1:
#         train_count = 1
#     if val_count < 1:
#         val_count = 1
#         train_count -= 1
#     if test_count < 1:
#         test_count = 1
#         train_count -= 1

#     # Balance between test and validation
#     if abs(val_count - test_count) > 1:
#         diff = abs(val_count - test_count) // 2
#         if val_count > test_count:
#             val_count -= diff
#             test_count += diff
#         else:
#             test_count -= diff
#             val_count += diff

#     # Distribute the remaining samples to train
#     remaining = count - (train_count + val_count + test_count)
#     train_count += remaining

#     train_counts[vendor] = train_count
#     val_counts[vendor] = val_count
#     test_counts[vendor] = test_count

# # Adjust the distribution for the top 3 vendors
# top_vendors = vendor_counts.head(3).index.tolist()
# remaining_difference = (0.7 * len(df) - sum(train_counts.values()))
# for vendor in top_vendors:
#     if remaining_difference > 0:
#         train_counts[vendor] += 1
#         remaining_difference -= 1

# # Sample filenames and save them
# train_files = {}
# val_files = {}
# test_files = {}

# for vendor, row in vendor_counts.items():
#     vendor_data = df[df['ground_truth'].apply(lambda x: json.loads(x)['gt_parse']['vendor_name']) == vendor]
#     train_vendor = vendor_data.sample(n=train_counts[vendor], random_state=42)
#     val_vendor = vendor_data.drop(train_vendor.index).sample(n=val_counts[vendor], random_state=42)
#     test_vendor = vendor_data.drop(train_vendor.index).drop(val_vendor.index)
    
#     train_files[vendor] = train_vendor['file_name'].tolist()
#     val_files[vendor] = val_vendor['file_name'].tolist()
#     test_files[vendor] = test_vendor['file_name'].tolist()

# # Save the sampled filenames to CSV
# pd.DataFrame.from_dict(train_files, orient='index').transpose().to_csv(os.path.join('metadata', 'train_files.csv'), index=False)
# pd.DataFrame.from_dict(val_files, orient='index').transpose().to_csv(os.path.join('metadata', 'val_files.csv'), index=False)
# pd.DataFrame.from_dict(test_files, orient='index').transpose().to_csv(os.path.join('metadata', 'test_files.csv'), index=False)

# # Print the distribution
# for vendor in vendor_counts.index:
#     total_samples = vendor_counts[vendor]
#     train_proportion = (train_counts[vendor] / total_samples) * 100
#     val_proportion = (val_counts[vendor] / total_samples) * 100
#     test_proportion = (test_counts[vendor] / total_samples) * 100
    
#     print(f"Vendor: {vendor}")
#     print(f"Total samples: {total_samples}")
#     print(f"Train: {train_counts[vendor]} ({train_proportion:.2f}%), Validation: {val_counts[vendor]} ({val_proportion:.2f}%), Test: {test_counts[vendor]} ({test_proportion:.2f}%)")
#     print("------")

# # Convert the dictionaries to DataFrames
# df_train = pd.DataFrame.from_dict(train_counts, orient='index', columns=['Train'])
# df_val = pd.DataFrame.from_dict(val_counts, orient='index', columns=['Validation'])
# df_test = pd.DataFrame.from_dict(test_counts, orient='index', columns=['Test'])

# # Concatenate the DataFrames
# result_df = pd.concat([df_train, df_val, df_test], axis=1)

# # Save the result to a csv file in the metadata folder
# result_df.to_csv(os.path.join('metadata', 'vendor_distribution.csv'))

# # Calculate and print the total number of invoices in each set and their proportions
# total_train = sum(train_counts.values())
# total_val = sum(val_counts.values())
# total_test = sum(test_counts.values())
# total_invoices = len(df)

# print(f"Total invoices: {total_invoices}")
# print(f"Train: {total_train} ({(total_train/total_invoices)*100:.2f}%)")
# print(f"Validation: {total_val} ({(total_val/total_invoices)*100:.2f}%)")
# print(f"Test: {total_test} ({(total_test/total_invoices)*100:.2f}%)")
