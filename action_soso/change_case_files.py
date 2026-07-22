#  action_soso/action_soso/change_case_files.py
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
Changes the case of the title of a file. If no filenames are given, operates on
all the files in the current directory.
"""
import sys, argparse
from re import compile as rcompile
from pathlib import Path
from copy import copy
from . import path_list, get_user_confirmation


WORD_REGEX		= rcompile(r'\w')
SPLITTER_REGEX	= rcompile(r'[_\-\s]')
ALLNUMS_REGEX	= rcompile('^[0-9]+$')
ALLCAPS_REGEX	= rcompile('^[A-Z]+$')
KEEP_CHARS		= ["'", '"', '>', '<', ':', ';', ',']


class CaseChanger:

	def __init__(self, options):
		self.options = options
		if options.title:
			self.func = str.capitalize
		elif options.upper:
			self.func = str.upper
		else:
			self.func = str.lower
		if options.dash:
			self.spacer = '-'
		elif options.space:
			self.spacer = ' '
		else:
			self.spacer = '_'
		self.multispc_regex = rcompile(fr'{self.spacer}+')

	def change_case(self, path):
		new_path = path.parent / (self._replace(path.stem) + path.suffix.lower())
		if new_path.name == path.name:
			return
		if not self.options.yes or self.options.dry_run or self.options.verbose:
			description = f'Rename "{path.name}"\n    -> "{new_path.name}"'
			if new_path.exists():
				description += ' (EXISTS)'
			print(description)
		if not self.options.dry_run and (self.options.yes or get_user_confirmation(default_true = True)):
			path.rename(new_path)

	def _replace(self, string):
		def _replace_part(part):
			if len(part) == 0 \
				or not WORD_REGEX.search(part) \
				or ALLNUMS_REGEX.match(part) \
				or self.options.ignore_caps and ALLCAPS_REGEX.match(part):
				return part
			return self.func(part)
		new_string = self.spacer.join([
			_replace_part(part)
			for part in SPLITTER_REGEX.split(string)
			if len(part)
		])
		return self.multispc_regex.sub(new_string, self.spacer)


def _main():
	parser = argparse.ArgumentParser()
	parser.add_argument('Filename', type=str, nargs = '*',
		help='File name(s) or directory name(s)')
	case_group = parser.add_mutually_exclusive_group(required = True)
	case_group.add_argument('--title', '-t', action='store_true',
		help='Make title case')
	case_group.add_argument('--upper', '-u', action='store_true',
		help='Make uppercase')
	case_group.add_argument('--lower', '-l', action='store_true',
		help='Make uppercase')
	spacer_group = parser.add_mutually_exclusive_group(required = True)
	spacer_group.add_argument('--dash', '-d', action='store_true',
		help='Space words with dashes (the default)')
	spacer_group.add_argument('--underscore', '-U', action='store_true',
		help='Space words with underscores')
	spacer_group.add_argument('--space', '-s', action='store_true',
		help='Space words with spaces')
	parser.add_argument('--recurse', '-r', action='store_true',
		help='Recursively rename all the files in the given directories.')
	parser.add_argument('--ignore-caps', '-i', action='store_true',
		help='Ignore parts of file names which are all capital letters.')
	parser.add_argument('--yes', '-y', action='store_true',
		help='Rename without confirmation.')
	parser.add_argument('--dry-run', '-n', action = 'store_true',
		help = 'Don\'t do anything - just show what would be done.')
	parser.add_argument('--verbose', '-v', action = 'store_true',
		help = 'Print what this script is doing.')
	parser.epilog = __doc__
	options = parser.parse_args()

	paths = path_list(options)
	if options.recurse:
		ndirs = len([ path for path in paths if path.is_dir() ])
		nfiles = len(paths) - ndirs
		prompt ='Rename '
		if ndirs:
			prompt += str(ndirs)
			prompt += ' directory' if ndirs == 1 else ' directories'
			if nfiles:
				prompt += ' and '
		if nfiles:
			prompt += str(nfiles)
			prompt += 'file' if nfiles == 1 else 'files'
		if not get_user_confirmation(prompt):
			exit(1)

	cc = CaseChanger(options)
	for path in paths:
		cc.change_case(path)


def main():
	try:
		return _main()
	except KeyboardInterrupt:
		print()
		return 9


if __name__ == '__main__':
	sys.exit(main() or 0)


#  end action_soso/action_soso/change_case_files.py
