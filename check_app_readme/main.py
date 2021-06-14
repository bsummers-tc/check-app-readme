"""Fix README.md"""
# standard library
import json
import re
import sys
from datetime import datetime


def get_app_version() -> str:
    """Return the current App version number."""
    try:
        with open('install.json') as fh:
            ij = json.load(fh)
        return ij.get('programVersion')
    except Exception:
        print('Failed to get install.json programVersion data.')
        sys.exit(1)


def check_version_date(filename: str) -> int:
    """Fix the date on the latest version."""
    ij_version = get_app_version()
    pattern = rf'^#{{1,3}}\s?{ij_version}\s?'
    with open(filename, 'r+') as fh:
        for line in fh.read().split('\n'):
            if re.match(pattern, line):
                _, _, version_date = line.split(' ', maxsplit=3)
                current_date = f'{str(datetime.date(datetime.now()))}'
                version_date = version_date.strip('(').strip(')')

                # check that the date on the latest version is today
                if current_date != version_date:
                    print(
                        f'The {filename} file has the wrong date ({version_date} '
                        f'-> {current_date}) for version {ij_version}.'
                    )
                    return 1

                # entry found and no issues
                break
        else:
            print(f'No release notes found for the current version ({ij_version}).')
            return 1

    return 0


def main():
    """Entry point for pre-commit hook."""
    return check_version_date('README.md')


if __name__ == '__main__':
    sys.exit(main())
