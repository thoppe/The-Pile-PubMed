from pathlib import Path
from ftplib import FTP
from wasabi import msg
import pandas as pd
import utils

# https://docs.python.org/3.8/library/ftplib.html

base_url = "ftp.ncbi.nlm.nih.gov"
days_to_update = 1
save_dest = Path("data/")


def update_listing(dest, f_save):

    if f_save.exists() and utils.days_since_modified(f_save) < days_to_update:
        msg.good(
            f"PUBMED {dest} listing is <{days_to_update} days old, " f"not updating"
        )
        return True

    ftp = FTP(base_url, user="anonymous", passwd="")
    ftp.cwd(dest)

    data = []
    for key, row in ftp.mlsd():
        row["filename"] = key
        data.append(row)

    df = pd.DataFrame(data).set_index("filename")

    utils.mkdir(save_dest)
    df.to_csv(f_save)
    msg.good(f"Downloaded {f_save}")


if __name__ == "__main__":

    f0 = save_dest / "PUBMED_ftp_baseline.csv"
    update_listing("/pubmed/baseline", f0)

    f1 = save_dest / "PUBMED_ftp_updatefiles.csv"
    update_listing("/pubmed/updatefiles", f1)

    df = pd.read_csv(f0)
    idx = df.filename.str.endswith(".gz")
    total_size = df[idx]["size"].sum() / 2 ** 30
    msg.info(f"Baseline file size {total_size:0.1f} GB")

    df = pd.read_csv(f1)
    idx = df.filename.str.endswith(".gz")
    total_size = df[idx]["size"].sum() / 2 ** 30
    msg.info(f"Update file size   {total_size:0.1f} GB")
