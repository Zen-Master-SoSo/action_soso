# action_soso

A bunch of handy utilities and nemo actions that utilize them.

### change-case-files

Changes the case of the title of a file. If no filenames are given, operates on
all the files in the current directory.

Usage:

```bash
$ change-case-files -ld "Filename With Caps and Spaces.txt"
filename-with-caps-and-spaces.txt
```

Help:

	usage: change-case-files.py [-h] (--title | --upper | --lower) (--dash |
	                            --underscore | --space) [--recurse] [--yes]
	                            [Filename ...]

	positional arguments:
	  Filename          File name(s) or directory name(s)

	options:
	  -h, --help        show this help message and exit
	  --title, -t       Make title case
	  --upper, -u       Make uppercase
	  --lower, -l       Make uppercase
	  --dash, -d        Space words with dashes (the default)
	  --underscore, -n  Space words with underscores
	  --space, -s       Space words with spaces
	  --recurse, -r     Recursively rename all the files in the given directories.
	  --yes, -y         Rename without confirmation.

### copy-content

Copies the content of the given file to the clipboard using xclip.

Help:

	usage: copy-content [-h] Filename

	positional arguments:
	  Filename    File name(s) or directory name(s)

	options:
	  -h, --help  show this help message and exit

### date-filename

Appends today's date to a file, optionally creating a copy or a read-only
backup copy.

Usage:

```bash
$ date-filename README.md
$ ls
 action_soso   LICENSE   pyproject.toml  'README 07.21.2026.md'
```

Help:

	usage: date-filename.py [-h] [--copy | --backup] [--dashes] [--year-first]
							[--time] [--dry-run] [--verbose]
							[Filename ...]

	positional arguments:
	  Filename          File name(s) or directory name(s)

	options:
	  -h, --help        show this help message and exit
	  --copy, -c        Make a copy and leave the original file.
	  --backup, -b      Make a read-only backup copy and leave the original file.
	  --dashes, -d      Use dashes instead of dots to separate the date parts.
	  --year-first, -y  Append date as yyyy/mm/dd instead of mm/dd/yyyy.
	  --time, -t        Also append the current time.
	  --dry-run, -n     Don't do anything - just show what would be done.
	  --verbose, -v     Print what this script is doing.

### number-files

Prepends or appends a sequential number to names of the given files. If no
directory names are given, renames all of the files in the current directory.
This command operates on directories, renumbering the files in each directory
given as a set. If multiple directory names are given, each directory is
treated as a separate set.

Help:

	usage: number-files [-h] (--prefix | --suffix) [--dash-separator |
						--dot-separator] [--compact] [--recurse] [--yes]
						[--dry-run] [--verbose]
						[Filename ...]

	positional arguments:
	  Filename              File name(s) or directory name(s)

	options:
	  -h, --help            show this help message and exit
	  --prefix, -p          Prefix the file names with a number
	  --suffix, -s          Append numbers to the ends of the file names
	  --dash-separator, -d  Separate the number and file title with a dash
	  --dot-separator, -D   Separate the number and file title with a dot
	  --compact, -c         Use compact numbers - do not pad numbers with zeroes
	  --recurse, -r         Recursively rename all the files in the given
							directories.
	  --yes, -y             Rename without confirmation.
	  --dry-run, -n         Don't do anything - just show what would be done.
	  --verbose, -v         Print what this script is doing.
