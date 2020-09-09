import pandas as pd
from pathlib import Path
from dspipe import Pipe
import gzip
from utils import iterate_pubmed_xml
from wasabi import msg

n_non_english = 0
n_english = 0

f_save = "data/PUBMED_title_abstracts_up_to_2019.txt.gz"

FOUT = gzip.open(f_save, mode="wt", compresslevel=9)


def compute(f0):
    global n_english, n_non_english

    df = pd.read_csv(f0)

    # Remove non-english entries
    idx = df.lang != "eng"
    n_non_english += idx.sum()
    n_english += (~idx).sum()

    # Concatenate
    df = df[~idx]
    text = df.title.astype(str) + df.abstract.astype(str)

    # Write each article to a newline
    for block in text:
        FOUT.write(block + "\n")


P = Pipe(source="data/baseline/parsed", input_suffix=".csv", limit=None)

P(compute, 1)

msg.good(f"Saved to {f_save}")
msg.info(
    f"{n_english:,} articles in English, filtered {n_non_english:,} in other languages"
)

filesize = Path(f_save).stat().st_size
msg.info(f"Compressed filesize {filesize:,}")
