#  action_soso/action_soso/resize_files.py
#
#  Copyright 2026 Leon Dionne <ldionne@dridesign.sh.cn>
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
Uses ImageMagick "convert" to create a copy of the given Infile, resized to the
given max height / width. The Outfile is named:

"<Infile path>/<Infile filetitle>-<size>x<size>.<Infile extension>".
"""
import logging, sys
from argparse import ArgumentParser
from pathlib import Path
from subprocess import run


def main():
	parser = ArgumentParser()
	parser.add_argument('Infile', type = str, nargs = '+',
		help='File name(s) of the image file to resize.')
	parser.add_argument('--size', '-s', type=int,
		help = 'Maximum height and width.')
	logging.basicConfig(
		level=logging.DEBUG,
		format='[%(filename)24s:%(lineno)3d] %(message)s'
	)
	parser.epilog = __doc__
	options = parser.parse_args()
	retval = 0
	for filename in options.Infile:
		in_path = Path(filename)
		if not in_path.exists():
			sys.stderr.write(f'Not found: "{in_path}"\n')
			continue
		out_path = in_path.parent / f'{in_path.stem}-{options.size}x{options.size}{in_path.suffix}'
		try:
			run(['convert', str(in_path),
				'-resize', f'{options.size}x{options.size}', str(out_path)],
				check = True)
		except CalledProcessError as err:
			sys.stderr.write(f'{err}\n')
			retval = 1
		else:
			print(out_path)
	return retval


if __name__ == '__main__':
	sys.exit(main() or 0)


#  end action_soso/action_soso/resize_files.py
