import sys
import urllib.request
from collections import Counter

# Since only one mirror for now, url is constant
URL = "http://ftp.uk.debian.org/debian/dists/stable/main/"

def check_architecture(arch: str) -> bool:
    """Make sure the architecture is a valid option.

    Args:
    arch -- Architecture input
    """
    return True if arch in options else False

def download_contents_index(url: str) -> str:
    """Download contents index.

    Args:
    url -- URL of Debian Mirror
    """
    # Try and download contents index, exit if download fails
    try:
        urllib.request.urlretrieve(f"{url}", "contents_index")
        # Open downloaded file and read
        with open("contents_index", "r") as fp:
            output = fp.read()
        return output
    except:
        sys.exit("Unable to download contents index!")
        
def parse_and_count(content: str) -> list:
    """Parse contents index and count files per package.

    Args:
    content -- Content index text
    """
    # Split the text by comma delimiter
    content = content.split(",")
    # Prune filenames and only keep package names for file count
    pkgs = ["".join(path.strip().split("/")[:-1]) for path in content]
    # Return list of top ten packages with most files
    return Counter(pkgs).most_common(10)


if __name__ == "__main__":
    # Make sure valid number of arguments input
    if len(sys.argv) != 2:
        sys.exit("Usage: package_statistics.py <ARCH>")
    # Architecture Input Arg
    architecture = sys.argv[1]
    # TODO: Check if architecture is valid otherwise exit
    # Download the respective contents index for the architecture
    content = download_contents_index(URL)
    # Parse the file output and count files per package
    pkg_count = parse_and_count(content)
    # Output top ten packages with most files associated with them
    for index, pkg in enumerate(pkg_count):
        print(f"{i}. {pkg[0]}  {pkg[1]}")
