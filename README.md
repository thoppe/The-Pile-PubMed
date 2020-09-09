# The-Pile-PubMed
Download, parse, and filter data [PubMed](https://pubmed.ncbi.nlm.nih.gov/), data-ready for [The-Pile](https://github.com/EleutherAI/The-Pile).

We use the 2019 baseline. Articles without a proper PMID, title, abstract, are ignored. Articles not with a PMC currently filtered out, as the text will overlap with the PubMed Central data pull. Current statistics:

    ✔ Saved to data/PUBMED_title_abstracts_up_to_2019.txt.gz
    ℹ 18,163,831 articles in English, filtered 1,479,778 in other languages
    ℹ Compressed filesize 8,538,103,489
    ℹ Uncompressed filesize 25,254,435,255