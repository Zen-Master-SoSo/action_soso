#  action_soso/action_soso/images_to_pdf.py
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
Combines the given image files into a single PDF.
"""
import sys, argparse
from pathlib import Path
from . import CancelableAction, no_clobber


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('Filenames', type = str, nargs = '+',
		help='Images to convert to PDF file')
	parser.epilog = __doc__
	options = parser.parse_args()
	output_path = no_clobber(Path('combined.pdf'))
	args = ['convert', *options.Filenames, output_path]
	action = CancelableAction(args,
		window_title = 'Images to PDF',
		window_text = f'Combining {len(options.Filenames)} images into "{output_path}"')
	if action.run():
		output_path.unlink()


if __name__ == '__main__':
	sys.exit(main() or 0)


#  end action_soso/action_soso/images_to_pdf.py
