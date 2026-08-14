#  action_soso/action_soso/tag_filenames.py
#
#  Copyright 2026 Leon Dionne <ldionne@dridesign.sh.cn>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
"""
Prompts the user for a "tag" to append or prepend to the filename, and renames
the given files.
"""
import logging
from argparse import ArgumentParser
from time import strftime
from pathlib import Path
from shutil import copy2
from zenity_soso import Entry
from . import path_list

DESCRIPTION_PREPEND = 'Prefix the filename with the text you enter'
DESCRIPTION_APPEND = 'Appends the text you enter to the filename'


def main():
	parser = ArgumentParser()
	parser.add_argument('Filename', type = str, nargs = '*',
		help='File name(s) or directory name(s)')
	op_group = parser.add_mutually_exclusive_group()
	op_group.add_argument('--prefix', '-p', action = 'store_true',
		help = DESCRIPTION_PREPEND)
	op_group.add_argument('--suffix', '-s', action = 'store_true',
		help = DESCRIPTION_APPEND)
	parser.add_argument('--recurse', '-r', action='store_true',
		help='Recursively rename all the files in the given directories.')
	parser.add_argument('--dry-run', '-n', action = 'store_true',
		help = 'Don\'t do anything - just show what would be done.')
	parser.add_argument('--verbose', '-v', action = 'store_true',
		help = 'Print what this script is doing.')
	parser.epilog = __doc__
	options = parser.parse_args()
	logging.basicConfig(
		level=logging.DEBUG,
		format='[%(filename)24s:%(lineno)3d] %(message)s'
	)
	paths = path_list(options)
	dlg = Entry(title = 'Add tag to filenames',
		text = DESCRIPTION_PREPEND if options.prefix else DESCRIPTION_APPEND)
	if tag := dlg.show():
		for path in paths:
			if options.prefix:
				new_path = path.parent / (tag + path.name)
			else:
				new_path = path.parent / (path.stem + tag + path.suffix)
			if options.verbose or options.dry_run:
				print(f'Rename "{path.name}" to "{new_path.name}"')
			elif not options.dry_run:
				path.rename(new_path)


if __name__ == '__main__':
	sys.exit(main() or 0)


#  end action_soso/action_soso/tag_filenames.py
