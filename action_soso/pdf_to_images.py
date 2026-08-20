#  action_soso/action_soso/pdf_to_images.py
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
Converts the given PDF into a series of images.
"""
import sys, argparse
from pathlib import Path
from . import CancelableAction


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('Filename', type = str,
		help='PDF file to convert to images')
	parser.epilog = __doc__
	options = parser.parse_args()
	given_path = Path(options.Filename)
	output_file = given_path.parent / given_path.stem / given_path.stem
	if output_file.parent.exists():
		for path in output_file.parent.iterdir():
			path.is_file and path.unlink()
	else:
		output_file.parent.mkdir()
	action = CancelableAction(['pdftocairo', '-png', options.Filename, output_file],
		window_title = 'PDF to images',
		window_text = f'Extracting "{given_path.name}" into "{output_file.parent.name}"')
	return action.run()


if __name__ == '__main__':
	sys.exit(main() or 0)


#  end action_soso/action_soso/pdf_to_images.py
