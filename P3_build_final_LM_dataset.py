from pathlib import Path
from dspipe import Pipe
import jsonlines
from utils import iterate_pubmed_xml
from wasabi import msg


# Keep track of what articles we keep for reporting
stats = {
    "kept_articles": 0,
    "filtered_out": 0,
}

f_save = "data/PUBMED_title_abstracts_2020_baseline.jsonl"
FOUT = jsonlines.open(f_save, mode="w")

meta_columns = ["pmid", "language"]


def compute(f0):
    global stats

    with jsonlines.open(f0, "r") as FIN:
        for row in FIN:

            # Remove entries where they overlap with PMC
            if row["pmc"] is not None:
                stats["filtered_out"] += 1
                continue

            stats["kept_articles"] += 1

            # Concatenate
            item = {"meta": {}}
            item["text"] = "\n".join([row["title"], row["abstract"]])

            # Build the meta information
            for k in meta_columns:
                item["meta"][k] = row[k]

            # PMID should always exist and be an integer
            item["meta"]["pmid"] = int(item["meta"]["pmid"])

            # Save to the master file
            FOUT.write(item)


P = Pipe(source="data/baseline/parsed/", input_suffix=".jsonl", shuffle=True)

P(compute, 1)
msg.good(f"Saved to {f_save}")
msg.info(
    f"Saved {stats['kept_articles']:,}, filtered {stats['filtered_out']:,} articles that overlapped in PMC"
)

filesize = Path(f_save).stat().st_size
msg.info(f"Compressed filesize {filesize:,}")
