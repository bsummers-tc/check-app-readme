"""Fix README.md"""
# standard library
import argparse
import json
import re
import sys
from datetime import datetime
from typing import Optional, Sequence

# third-party
import sh


def get_app_version() -> str:
    """Return the current App version number."""
    try:
        with open('install.json') as fh:
            ij = json.load(fh)
        return ij.get('programVersion')
    except Exception:
        print('Failed to get install.json programVersion data.')
        sys.exit(1)


def check_branch(branches: list) -> bool:
    """Ensure the current branch is in list of provided branches."""
    current_branch = sh.git(['-C', '.', 'rev-parse', '--abbrev-ref', 'HEAD']).strip()
    if current_branch in branches:
        return True

    # verbose output
    print(f'Current Branch:   {current_branch}')
    print(f'Enabled Branches: {branches}')
    return False


def check_version_date(filename: str) -> int:
    """Fix the date on the latest version."""
    ij_version = get_app_version()
    pattern = rf'^(?:#{{1,3}}\s?)(?:{ij_version}\s?)(?P<date>.*)'
    with open(filename, 'r+') as fh:
        for line in fh.read().split('\n'):
            if re.match(pattern, line):
                match = re.search(pattern, line)
                version_date = match.group('date')
                if version_date:
                    version_date = version_date.strip('(').strip(')')
                current_date = f'{str(datetime.date(datetime.now()))}'

                # verbose output
                print(f'Matched Line:     {line}')
                print(f'IJ Version:       {ij_version}')
                print(f'Readme Date:      {version_date}')
                print(f'Current Date:     {current_date}')

                # check that the date on the latest version is today
                if current_date != version_date:
                    print(
                        f'\nThe {filename} file has the wrong date ({version_date} '
                        f'-> {current_date}) for version {ij_version}.'
                    )
                    return 1

                # entry found and no issues
                break
        else:
            print(f'\nNo release notes found for the current version ({ij_version}).')
            return 1

    return 0


def main(argv: Optional[Sequence[str]] = None):
    """Entry point for pre-commit hook."""
    print('argv', argv)
    parser = argparse.ArgumentParser()
    parser.add_argument('--branches', action='append', default=[])
    args = parser.parse_args(argv)

    retval = 0
    # if check_branch(args.branches) is True:
    if True:
        retval = check_version_date('README.md')
    return retval


if __name__ == '__main__':
    sys.exit(main())
