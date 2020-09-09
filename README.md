# The-Pile-PubMed
Download, parse, and filter data [PubMed](https://pubmed.ncbi.nlm.nih.gov/), data-ready for [The-Pile](https://github.com/EleutherAI/The-Pile).

We use the 2019 baseline. Articles without a proper PMID, title, abstract, are ignored. Articles not with a PMC currently filtered out, as the text will overlap with the PubMed Central data pull. Current statistics:

    ✔ Saved to data/PUBMED_title_abstracts_2019_baseline.jsonl
    ℹ Saved 15,518,009, filtered 4,417,955 articles that overlapped in PMC
    ℹ Uncompressed filesize 21,628,496,354
    ℹ Uncompressed filesize  6,896,358,250

Compressed with

    zstd -T16 --keep PUBMED_title_abstracts_2019_baseline.jsonl 