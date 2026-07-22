#  action_soso/action_soso/install_nemo_actions.py
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
Copies all of the nemo actions in this repository to your nemo actions folder.
"""
import sys, argparse
from os import linesep
from pathlib import Path
from shutil import copy2
from . import get_user_confirmation, print_columnar


def _main():
	parser = argparse.ArgumentParser()
	parser.epilog = __doc__
	parser.parse_args()

	actions = list(Path(__file__).parent.joinpath('actions').iterdir())
	print_columnar(sorted([ action.name for action in actions ]))
	print()
	actions_path = Path().home().joinpath('.local', 'share', 'nemo', 'actions')
	print(f'Copy these files to "{actions_path}"')
	if get_user_confirmation():
		actions_path.mkdir(parents = True, exist_ok = True)
		for src_path in actions:
			dest_path = actions_path / src_path.name
			if dest_path.exists():
				print(f'{dest_path} exists.')
				if not get_user_confirmation('Overwrite'):
					continue
			copy2(src_path, dest_path)
	else:
		print('Aborted - nothing was copied')

def main():
	try:
		return _main()
	except KeyboardInterrupt:
		print()
		return 9


if __name__ == '__main__':
	sys.exit(main() or 0)


#  end action_soso/action_soso/install_nemo_actions.py
