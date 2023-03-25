from rich.console import Console
from rich.table import Table
from rich.progress import track
import requests
import sys
import json
import re
import subprocess
import os
console = Console()


def main():

    USER = input("Enter mixcloud upload username: ")
    SHOW = input("Enter show name: ")

    table = Table(title="Information entered")

    table.add_column("User", style="cyan", no_wrap=True)
    table.add_column("Show", style="magenta")

    table.add_row(USER, SHOW)
    console.print(table)

    DOWNLOAD_DIR_DEFAULT = os.path.join(
        os.environ["HOME"], "Downloads/Mixcloud", SHOW)

    with console.status("[bold blue]Fetching show links...") as status:
        r = requests.get("https://api.mixcloud.com/" +
                         USER + "/cloudcasts/")
        json_r = json.loads(r.text)
        show_links = []
        while True:
            for i in range(len(json_r["data"])):
                if SHOW in json_r["data"][i]["name"]:
                    show_links.append("https://mixcloud.com" +
                                      json_r["data"][i]["key"])
            if "next" not in json_r["paging"]:
                break
            r = requests.get(json_r["paging"]["next"])
            json_r = json.loads(r.text)

    print(f"Retrieved {len(show_links)} episode/s for {SHOW} from {USER}")

    if len(show_links) > 0:

        DOWNLOAD_DIR_USER = input(
            "Enter absolute path location to download to [enter to use default]: ")

        if DOWNLOAD_DIR_USER == "":
            os.makedirs(DOWNLOAD_DIR_DEFAULT, exist_ok=True)
            CWD = DOWNLOAD_DIR_DEFAULT
            print("Saving to: ", DOWNLOAD_DIR_DEFAULT)
        else:
            try:
                os.makedirs(DOWNLOAD_DIR_USER, exist_ok=True)
                CWD = DOWNLOAD_DIR_USER
            except:
                os.makedirs(DOWNLOAD_DIR_DEFAULT, exist_ok=True)
                CWD = DOWNLOAD_DIR_DEFAULT
                print("Unable to save to this location, saving to: ",
                      DOWNLOAD_DIR_DEFAULT)

        for i in track(range(len(show_links)), description='[green]Downloading...'):

            p = subprocess.run(["youtube-dl", show_links[i]], stdout=subprocess.DEVNULL,
                               stderr=subprocess.STDOUT, cwd=CWD)

        console.print(f"[bold green]Done! Saved to {CWD}")

    else:

        console.print("[bold red]No links retrieved, check your inputs.")


if __name__ == "__main__":
    main()
