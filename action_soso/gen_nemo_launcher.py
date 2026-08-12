#  action_soso/action_soso/gen_nemo_launcher.py
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
Generates a nemo launcher with your bookmarks appearing as menu items.
"""
import logging, sys
from argparse import ArgumentParser
from pathlib import Path

HOME = Path.home()
BOOKMARK_ENTRY = """[Desktop Action open-{0}]
Name={2}
Exec=nemo "{1}"

"""
MAIN_ENTRY = """[Desktop Entry]
Name=Files
Comment=Access and organize files
Exec=nemo %U
Icon=folder
Keywords=folders;filesystem;explorer;
Terminal=false
Type=Application
StartupNotify=false
Categories=GNOME;GTK;Utility;Core;
MimeType=inode/directory;application/x-gnome-saved-search;
Actions=open-home;open-desktop;open-recent;$actions;

"""
STANDARD_ENTRIES = f"""[Desktop Action open-home]
Name=Home Folder
Exec=nemo %u

[Desktop Action open-desktop]
Name=Desktop
Exec=nemo {HOME}/Desktop

[Desktop Action open-recent]
Name=Recent
Exec=nemo recent:///

[Desktop Action update-launcher]
Name=Update this menu
Exec={sys.argv[0]}

"""
AUTORUN_LAUNCHER = f"""[Desktop Entry]
Type=Application
Name=Generate nemo launcher
Exec={sys.argv[0]}
Comment=Sets up the nemo menu on the left side of the screen to show your bookmarks.
X-GNOME-Autostart-enabled=true

"""



def main():
	parser = ArgumentParser()
	parser.add_argument('--autorun', '-a', action = 'store_true',
		help = 'Have this script run automatically at startup.')
	parser.epilog = __doc__
	options = parser.parse_args()
	logging.basicConfig(
		level=logging.DEBUG,
		format="[%(filename)24s:%(lineno)3d] %(levelname)-8s %(message)s"
	)
	if options.autorun:
		launcher_path = HOME / '.config' / 'autostart' / 'nemo-gen-launcher.desktop'
		launcher_path.write_text(AUTORUN_LAUNCHER, encoding = 'utf-8')
		launcher_path.chmod(0o744)
		print(f'Wrote "{launcher_path}"')
		print("This script should now run every time you start up or log in.")
		print()
	launcher_path = HOME / '.local' / 'share' / 'applications' / 'nemo.desktop'
	with open(launcher_path, 'w') as fob:
		fob.write(MAIN_ENTRY)
		path = HOME  / '.config' / 'gtk-3.0' / 'bookmarks'
		for index, parts in enumerate([ line.split(' ', 1)
			for line in path.read_text().splitlines() ]):
			fob.write(BOOKMARK_ENTRY.format(index, *parts))
		fob.write(STANDARD_ENTRIES)
	print(f'Wrote "{launcher_path}"')

if __name__ == "__main__":
	sys.exit(main() or 0)


#  end action_soso/action_soso/gen_nemo_launcher.py
