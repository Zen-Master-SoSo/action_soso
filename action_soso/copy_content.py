#  action_soso/action_soso/copy_content.py
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
Copies the content of the given file to the clipboard using xclip.
"""
import sys, argparse
from subprocess import run


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('Filename', type = str,
		help='File name(s) or directory name(s)')
	parser.epilog = __doc__
	options = parser.parse_args()
	run(['xclip', '-selection', 'clipboard', options.Filename], check = True)


if __name__ == '__main__':
	sys.exit(main() or 0)


#  end action_soso/action_soso/copy_content.py
