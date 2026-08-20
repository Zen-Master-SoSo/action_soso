#  action_soso/action_soso/__init__.py
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
A bunch of handy utilities and nemo actions that utilize them.
"""
from math import ceil
from pathlib import Path
from subprocess import Popen
from time import sleep


__version__ = "1.5.1"


def path_list(options, cwd_default = True):
	def _recurse_path(path):
		for item in path.iterdir():
			yield item
			if item.is_dir():
				yield from _recurse_path(item)
	paths = []
	try:
		given_paths = [ Path(filename) for filename in options.Filename ]
	except AttributeError:
		given_paths = [ Path(dirname) for dirname in options.Directory ]
	if cwd_default and not given_paths:
		given_paths = list(Path().iterdir())
	if options.recurse:
		paths = []
		for filename in given_paths:
			path = Path(filename)
			if path.is_dir():
				paths.extend(list(_recurse_path(path)))
			else:
				paths.append(path)
		return paths
	return given_paths


def no_clobber(path):
	instance = 1
	stem = path.stem
	while path.exists():
		numero = f' - {instance}'
		try_stem = stem[:stem.rindex(numero)] if stem.endswith(numero) else stem
		path = path.parent / f'{try_stem}{numero}{path.suffix}'
		instance += 1
	return path


def get_user_confirmation(prompt = 'Are you sure', default_true = False):
	"""
	Prints a description of what the script wants to do and the prompt, then waits
	for the user to press either the 'y' or 'n' key.

	Returns True if user pressed 'y'. If the user presses ENTER, returns the value
	of "default_true".
	"""
	yn = 'Y/n' if default_true else 'y/N'
	while True:
		print(f'  {prompt}? [{yn}] ', end = '')
		key = input()
		if not key:
			print()
			return default_true
		if key.lower() in ('y', 'n'):
			print()
			return key.lower() == 'y'
		else:
			print('  (Enter either "y" or "n")', end = '')


def print_columnar(strings, *, screen_width = 120, indent = ' '):
	maxlen = max(len(string) for string in strings) + len(indent)
	strings = [ string.ljust(maxlen) for string in strings ]
	row_width = screen_width // maxlen
	num_rows = ceil(len(strings) / row_width)
	rows = [ strings[col * row_width: col * row_width + row_width] for col in range(num_rows) ]
	for row in rows:
		print(indent + ' '.join(row))


class CancelableAction:
	"""
	Runs a subprocess with a zenity progress dialog allowing the user to cancel.
	"""

	def __init__(self, arguments, *,
		window_title = 'Action SoSo', window_text = 'Please wait...'):
		"""
		The given "arguments" passed to subprocess.run.
		"window_title" is the title to display on the zenity progress dialog.
		"window_text" is the text to display on the zenity progress dialog.
		"""
		self.arguments = arguments
		self.window_title = window_title
		self.window_text = window_text

	def run(self):
		"""
		Run the command.

		Returns (int) 1 if the user cancels the action before it is complete.
		If the action completes, returns (int) 0.
		"""
		zenity_process = Popen(['zenity',
			'--progress', '--pulsate',
			'--no-cancel', '--ok-label', 'Cancel',	# hack - eliminate one button
			'--title', self.window_title,
			'--text', self.window_text
		])
		action_process = Popen(self.arguments)
		while True:
			if zenity_process.poll() is None:
				if action_process.poll() is None:
					sleep(0.25)
				else:
					zenity_process.terminate()
					return 0
			else:
				action_process.terminate()
				return 1


#  end action_soso/action_soso/__init__.py
