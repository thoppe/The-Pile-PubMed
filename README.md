# The-Pile-PubMed
Download, parse, and filter data [PubMed](https://pubmed.ncbi.nlm.nih.gov/), data-ready for [The-Pile](https://github.com/EleutherAI/The-Pile).

We use the 2019 baseline. Articles without a proper PMID, title, abstract, and language ID are ignored. Articles not in English are currently filtered out. Current statistics:

    ✔ Saved to data/PUBMED_title_abstracts_up_to_2019.txt.gz
    ℹ 66,473 English articles, ignored 13,585 in other languages
    ℹ Compressed filesize 24,210,965
