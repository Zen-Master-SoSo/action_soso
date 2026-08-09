#  action_soso/action_soso/__main__.py
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
# action_soso

A bunch of handy utilities and nemo actions that utilize them.

* change-case-files
  Changes the case of the title of a file. If no filenames are given, operates on
  all the files in the current directory.

* copy-content
  Copies the content of the given file to the clipboard using xclip.

* date-filename
  Appends today's date to a file, optionally creating a copy or a read-only
  backup copy.

* number-files
  Prepends or appends a sequential number to names of the given files. If no
  directory names are given, renames all of the files in the current directory.
  This command operates on directories, renumbering the files in each directory
  given as a set. If multiple directory names are given, each directory is
  treated as a separate set.

To install Nemo actions:
  $ action-soso --install
"""
import sys
from argparse import ArgumentParser
from os import linesep
from pathlib import Path
from shutil import copy2
from . import get_user_confirmation, print_columnar


def _main():
	parser = ArgumentParser()
	parser.add_argument('--install', '-i', action='store_true',
		help='Install the nemo actions, making the utilities available from nemo context menus.')
	options = parser.parse_args()

	if options.install:
		actions = list(Path(__file__).parent.joinpath('actions').iterdir())
		print_columnar(sorted([ action.name for action in actions ]))
		print()
		actions_path = Path().home().joinpath('.local', 'share', 'nemo', 'actions')
		print(f'Copy these files to "{actions_path}"')
		if get_user_confirmation(default_true = True):
			actions_path.mkdir(parents = True, exist_ok = True)
			for src_path in actions:
				copy2(src_path, actions_path / src_path.name)
			print('Success!')
			print('Quit and restart nemo to make sure the actions are available.')
			print('(Run "nemo --quit" to make sure all instances have exited.)')
		else:
			print('Aborted - nothing was copied')
	else:
		print(__doc__)

def main():
	try:
		return _main()
	except KeyboardInterrupt:
		print()
		return 9


if __name__ == '__main__':
	sys.exit(main() or 0)


#  end action_soso/action_soso/__main__.py
