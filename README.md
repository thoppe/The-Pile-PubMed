# The-Pile-PubMed
Download, parse, and filter data [PubMed](https://pubmed.ncbi.nlm.nih.gov/), data-ready for [The-Pile](https://github.com/EleutherAI/The-Pile).

We use the 2019 baseline. Articles without a proper PMID, title, abstract, are ignored. Articles not with a PMC currently filtered out, as the text will overlap with the PubMed Central data pull. Current statistics:

### Pile-V2 Statistics

    ✔ Saved to data/PUBMED_title_abstracts_2020_baseline.jsonl
    ℹ Collection completed 12/15/2021
    ℹ Saved 16,677,660 publications
    ℹ Filtered 5,864,687 articles that overlapped in PMC
    ℹ Uncompressed filesize 23,494,141,868
    ℹ Compressed filesize 7,476,150,095
    ℹ sha256sum 5df50c9dff39030eee63f576fb9df225c99e7eae8ce2579358df92114eb4e684

### Pile-V1 Statistics

    ✔ Saved to data/PUBMED_title_abstracts_2019_baseline.jsonl
    ℹ Saved 15,518,009 publications
    ℹ Filtered 4,417,955 articles that overlapped in PMC
    ℹ Uncompressed filesize 21,628,496,354
    ℹ Compressed filesize    6,896,358,250
