#!/usr/bin/env python3
import pathlib
import datetime

def _next_available_dir(path: pathlib.Path):
    # MONTH-DAY-NN
    today = datetime.date.today()
    N = 0
    while (True):
        month = today.strftime("%b")
        day   = today.strftime("%d")
        directory = pathlib.Path.joinpath(path, f'{month}-{day}-{N}')
        if not pathlib.Path.exists(directory):
            return directory
        N += 1

def make_project_dir(prefix: str = None, dry_run: bool = False, check_exists: bool = True):

    if prefix is not None:
        pre = pathlib.Path(prefix)
    else:
        pre = pathlib.Path.cwd()

    # Check to make sure the prefix directory exists
    if not pathlib.Path.exists(pre) and check_exists:
        raise FileNotFoundError(f"The directory {pre.name} does not exist")

    project_dir = _next_available_dir(pre)

    # Make the directory if this isn't a dry run
    if not dry_run:
        # If we didn't check to make sure parents exist, then we'll
        # go ahead and assume they wanted us to make those directories
        # as well.
        project_dir.mkdir(parents=not check_exists)

    # Return the pathlib.Path of the new directory
    return (project_dir.resolve())

if __name__ == "__main__":
    print(make_project_dir(dry_run=True))
    print(make_project_dir('experiment-results', check_exists=False, dry_run=True))

