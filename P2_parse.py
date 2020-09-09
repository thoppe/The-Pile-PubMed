from pathlib import Path
from wasabi import msg
from dspipe import Pipe
from tqdm import tqdm
import bs4
from utils import iterate_pubmed_xml
import jsonlines


def compute(f0, f1):

    data = []

    for pmid, text in tqdm(iterate_pubmed_xml(f0)):

        # This is the bottleneck operation
        soup = bs4.BeautifulSoup(text, "lxml")

        article = {}
        article["abstract"] = soup.find("abstract")
        article["title"] = soup.article.find("articletitle")
        article["pmid"] = soup.find("pmid")

        # Skip if any missing fields
        if any((v is None for v in article.values())):
            continue

        # Remove copyright information from abstract text
        copy = article["abstract"].find("copyrightinformation")
        if copy is not None:
            copy.decompose()

        # Convert to text, remove extra spacing.
        for k, val in article.items():
            article[k] = " ".join(val.get_text().strip().split())

        # Check if article has a PMCID to filter later
        pmc = soup.find("articleid", idtype="pmc")

        if pmc is not None:
            article["pmc"] = pmc.get_text()
        else:
            article["pmc"] = None

        # Check if article has language tag to filter later
        lang = soup.find("language")

        if lang is not None:
            article["language"] = lang.get_text()
        else:
            article["language"] = None

        data.append(article)

    # Only write at the end to mark as success
    with jsonlines.open(f1, "w") as FOUT:
        FOUT.write_all(data)

    msg.good(f"Finished {f1}, saved {len(data)} articles")


def safe_compute(*args):
    try:
        compute(*args)
    except:
        print(f"Failed {args}")


P = Pipe(
    source="data/baseline/gz",
    dest="data/baseline/parsed",
    input_suffix=".gz",
    output_suffix=".jsonl",
    shuffle=True,
)

P(compute, -1)
