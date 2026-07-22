#  action_soso/action_soso/number_files.py
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
Prepends or appends a sequential number to names of the given files. If no
directory names are given, renames all of the files in the current directory.

This command operates on directories, renumbering the files in each directory
given as a set. If multiple directory names are given, each directory is
treated as a separate set.
"""
import sys, argparse
from pathlib import Path
from math import ceil, log10
from . import path_list, get_user_confirmation, print_columnar

class Numberer:

	def __init__(self, options):
		self.options = options
		self.num_func = self._compact if options.compact else self._padded
		self.stem_func = self._prefix if options.prefix else self._suffix
		self.sep = '-' if options.dash_separator else '.' if options.dot_separator else ' '

	def renumber(self, src_paths, directory_path = None):
		nplaces = ceil(log10(len(src_paths)))
		dest_paths = [
			Path(filepath.parent) / (
				self.stem_func(filepath, self.num_func(x, nplaces)) + filepath.suffix)
			for x, filepath in enumerate(src_paths)
		]
		if not self.options.yes or self.options.dry_run or self.options.verbose:
			if directory_path:
				print(f' {directory_path}')
				print(' ' + '-' * 118)
			print_columnar([ dest_path.name for dest_path in dest_paths ])
			print()
			if not self.options.dry_run and not self.options.yes:
				print(f'Rename these files')
		if not self.options.dry_run and (
			self.options.yes or get_user_confirmation(default_true = True)):
			for src, dest in zip(src_paths, dest_paths):
				src.rename(dest)

	def _prefix(self, path, numstr):
		return f'{numstr}{self.sep}{path.stem}'

	def _suffix(self, path, numstr):
		return f'{path.stem}{self.sep}{numstr}'

	def _padded(self, x, nplaces):
		return str(x + 1).zfill(nplaces)

	def _compact(self, x, _):
		return str(x + 1)


def _main():
	parser = argparse.ArgumentParser()
	parser.add_argument('Filename', type = str, nargs = '*',
		help='File name(s) or directory name(s)')
	placement_group = parser.add_mutually_exclusive_group(required = True)
	placement_group.add_argument('--prefix', '-p', action='store_true',
		help='Prefix the file names with a number')
	placement_group.add_argument('--suffix', '-s', action='store_true',
		help='Append numbers to the ends of the file names')
	separator_group = parser.add_mutually_exclusive_group()
	separator_group.add_argument('--dash-separator', '-d', action='store_true',
		help='Separate the number and file title with a dash')
	separator_group.add_argument('--dot-separator', '-D', action='store_true',
		help='Separate the number and file title with a dot')
	parser.add_argument('--compact', '-c', action='store_true',
		help='Use compact numbers - do not pad numbers with zeroes')
	parser.add_argument('--recurse', '-r', action='store_true',
		help='Recursively rename all the files in the given directories.')
	parser.add_argument('--yes', '-y', action='store_true',
		help='Rename without confirmation.')
	parser.add_argument('--dry-run', '-n', action = 'store_true',
		help = 'Don\'t do anything - just show what would be done.')
	parser.add_argument('--verbose', '-v', action = 'store_true',
		help = 'Print what this script is doing.')
	parser.epilog = __doc__
	options = parser.parse_args()
	numberer = Numberer(options)
	selected_paths = path_list(options)
	directory_paths = [ path for path in selected_paths if path.is_dir() ]
	if options.recurse or len(directory_paths) == len(selected_paths):
		for directory_path in directory_paths:
			file_paths = [ entry for entry in directory_path.iterdir() if entry.is_file() ]
			if file_paths:
				numberer.renumber(file_paths, directory_path)
	else:
		numberer.renumber(selected_paths)


def main():
	try:
		return _main()
	except KeyboardInterrupt:
		print()
		return 9


if __name__ == '__main__':
	sys.exit(main() or 0)


#  end action_soso/action_soso/number_files.py
