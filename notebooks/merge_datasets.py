# Merge multiple datasets into one
import glob

import pandas as pd

# read all csv files in a directory
path = r"data/comments"
all_files = glob.glob(path + "/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)

# save to csv
frame.to_csv("data/comments.csv", index=False)


#%%
path = r"data/instagram/comments"

all_files = glob.glob(path + "/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)

frame.to_csv("data/instagram/comments.csv", index=False)

#%%

path_yt_comments = r"data/youtube/comments.csv"
path_ig_comments = r"data/instagram/comments.csv"

li = []

for filename in [path_yt_comments, path_ig_comments]:
    df = pd.read_csv(filename, index_col=None, header=0)
    if "comment" in df.columns:
        df = df.rename(columns={"comment": "text"})
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)

frame.to_csv("data/comments.csv", index=False)

#%%

import pandas as pd
import glob

# merge and create a new csv file for twitter data only full_text column

path = r"data/twitter"

all_files = glob.glob(path + "/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

# concat only full_text column
frame = pd.concat([df["full_text"] for df in li], axis=0, ignore_index=True)

# save to csv
frame.to_csv("data/twitter.csv", index=False)


frame.to_csv("data/twitter.csv", index=False)

#%%

twitter_df = pd.read_csv("data/twitter.csv")

comment_df = pd.read_csv("data/comments.csv")

twitter_df.rename(columns={"full_text": "text"}, inplace=True)

# merge twitter and comments

merged_df = pd.concat([twitter_df, comment_df], axis=0, ignore_index=True)

merged_df.to_csv("data/datasets.csv", index=False)


#%%
