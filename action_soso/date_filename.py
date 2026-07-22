#  action_soso/action_soso/date_filename.py
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
Appends today's date to a file, optionally creating a copy or a read-only
backup copy.
"""
import logging
from argparse import ArgumentParser
from time import strftime
from pathlib import Path
from shutil import copy2


def main():
	parser = ArgumentParser()
	parser.add_argument('Filename', type = str, nargs = '*',
		help='File name(s) or directory name(s)')
	op_group = parser.add_mutually_exclusive_group()
	op_group.add_argument('--copy', '-c', action = 'store_true',
		help = 'Make a copy and leave the original file.')
	op_group.add_argument('--backup', '-b', action = 'store_true',
		help = 'Make a read-only backup copy and leave the original file.')
	parser.add_argument('--dashes', '-d', action = 'store_true',
		help = 'Use dashes instead of dots to separate the date parts.')
	parser.add_argument('--year-first', '-y', action = 'store_true',
		help = 'Append date as yyyy/mm/dd instead of mm/dd/yyyy.')
	parser.add_argument('--time', '-t', action = 'store_true',
		help = 'Also append the current time.')
	parser.add_argument('--dry-run', '-n', action = 'store_true',
		help = 'Don\'t do anything - just show what would be done.')
	parser.add_argument('--verbose', '-v', action = 'store_true',
		help = 'Print what this script is doing.')
	logging.basicConfig(
		level=logging.DEBUG,
		format='[%(filename)24s:%(lineno)3d] %(message)s'
	)
	parser.epilog = __doc__
	options = parser.parse_args()

	formats = {
		0b00	: '%m.%d.%Y',
		0b01	: '%m-%d-%Y',
		0b10	: '%Y.%m.%d',
		0b11	: '%Y-%m-%d'
	}
	date_part = strftime(formats[ (1 if options.dashes else 0) + (2 if options.year_first else 0) ])

	paths = [ Path(filename) for filename in options.Filename ] \
		if options.Filename \
		else list(Path().iterdir())
	for path in paths:
		new_path = path.parent / (path.stem + ('-' if options.dashes else ' ') + date_part + path.suffix)
		if options.verbose or options.dry_run:
			if options.copy:
				print(f'Copy "{path.name}" to "{new_path.name}"')
			elif options.backup:
				print(f'Make a read-only copy of "{path.name}" at "{new_path.name}"')
			else:
				print(f'Rename "{path.name}" to "{new_path.name}"')
		if not options.dry_run:
			if options.copy:
				copy2(path, new_path)
			elif options.backup:
				copy2(path, new_path)
				new_path.chmod(path.stat().st_mode & 0o555)
			else:
				path.rename(new_path)


if __name__ == '__main__':
	sys.exit(main() or 0)


#  end action_soso/action_soso/date_filename.py
