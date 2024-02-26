import argparse
from collections import defaultdict
from pathlib import Path

from numpy import require

from maniple.metrics.check_utils import bugid_patches

def main():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--bugids", nargs="+", help="The bug ids to check", required=True)
    argument_parser.add_argument("--bugid-folder", help="The folder containing the bug id folders", required=True)
    args = argument_parser.parse_args()

    bugids = args.bugids
    bugid_folder = Path(args.bugid_folder)

    for bugid in bugids:
        patches = bugid_patches(bugid, bugid_folder)
        d = defaultdict(list)

        for patch in patches:
            bitvector = patch.name.split("_")[0]
            d[bitvector].append(patch)

        sorted_d = dict(sorted(d.items(), key=lambda item: len(item[1]), reverse=True))
        
        for bitvector, patches in sorted_d.items():
            print(f"{bitvector}: {len(patches)}")
            for patch in patches:
                p = str(patch).replace('json', 'md').replace('result', 'response')
                print(f"  {p}")
            print()

if __name__ == "__main__":
    main()
