from pathlib import Path
from wasabi import msg
import pandas as pd
from dspipe import Pipe
from tqdm import tqdm
import bs4
from utils import iterate_pubmed_xml


def compute(f0, f1):

    data = []

    for pmid, text in tqdm(iterate_pubmed_xml(f0)):

        # This is the bottleneck operation
        soup = bs4.BeautifulSoup(text, "lxml")

        article = {}
        article["abstract"] = soup.find("abstract")
        article["title"] = soup.article.find("articletitle")
        article["lang"] = soup.find("language")
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

        data.append(article)

    df = pd.DataFrame(data).set_index("pmid")
    df.to_csv(f1)

    msg.good(f"Finished {f1}, saved {len(df)} articles")


P = Pipe(
    source="data/baseline/gz",
    dest="data/baseline/parsed",
    input_suffix=".gz",
    output_suffix=".csv",
    shuffle=True,
)

P(compute, -1)
