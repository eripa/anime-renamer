anime-renamer
=============

A script for parsing and renaming anime episodes such as Bleach, Naruto and One Piece. The script will fetch meta-data from theTVDB to figure out "real" episode numbering (ex S02E03) from incremental numnering model used in anime releases.

## How to use
### config file
Copy/move the shows.cfg-template file to shows.cfg and edit to your liking. All values are separated by commas (',').

The first section is called "global" and contains:

 * file_extensions
 * shows
 * output_root

_file\_extensions_ specifies what file extensions the script will look for. _shows_ is a list of the shows that the script should look for and _output\_root_ dictates where the renamed files should be put.

Sub sections should be defined for each show in the _shows_ list in _global_.

Each section should be written in lower case, such as "naruto shippuuden" and can contain a list of filler episodes like this:
filler_episodes=10-12,15,20-23

an "output\_dir" can also be specified. This will be a relative path to the global setting "output\_root"

### Run the script
The script takes folders and one argument as input:

    ./anime-renamer.py \[folder 1] \[folder 2] \[folder n] \[....] [--real]


If --real is omitted from the command line, noting will be commited. Append --real to make the script actually rename and move files.

