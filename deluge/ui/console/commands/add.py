#
# add.py
#
# Copyright (C) 2008-2009 Ido Abramovich <ido.deluge@gmail.com>
# Copyright (C) 2009 Andrew Resch <andrewresch@gmail.com>
#
# Deluge is free software.
#
# You may redistribute it and/or modify it under the terms of the
# GNU General Public License, as published by the Free Software
# Foundation; either version 3 of the License, or (at your option)
# any later version.
#
# deluge is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with deluge.    If not, write to:
# 	The Free Software Foundation, Inc.,
# 	51 Franklin Street, Fifth Floor
# 	Boston, MA    02110-1301, USA.
#
from deluge.ui.console.main import BaseCommand
import deluge.ui.console.colors as colors
from deluge.ui.client import client
import deluge.component as component

from optparse import make_option
import os
import base64

class Command(BaseCommand):
    """Add a torrent"""
    option_list = BaseCommand.option_list + (
            make_option('-p', '--path', dest='path',
                        help='save path for torrent'),
    )

    usage = "Usage: add [-p <save-location>] <torrent-file> [<torrent-file> ...]"

    def handle(self, *args, **options):
        self.console = component.get("ConsoleUI")

        t_options = {}
        if options["path"]:
            t_options["download_location"] = options["path"]

        for arg in args:
            if not os.path.isfile(arg):
                self.console.write("{!error!}This is a directory!")
                continue
            self.console.write("{!info!}Attempting to add torrent: %s" % arg)
            filename = os.path.split(arg)[-1]
            filedump = base64.encodestring(open(arg).read())

            def on_success(result):
                self.console.write("{!success!}Torrent added!")
            def on_fail(result):
                self.console.write("{!error!}Torrent was not added! %s" % result)

            client.core.add_torrent_file(filename, filedump, t_options).addCallback(on_success).addErrback(on_fail)

    def complete(self, line):
        line = os.path.abspath(os.path.expanduser(line))
        ret = []
        if os.path.exists(line):
            # This is a correct path, check to see if it's a directory
            if os.path.isdir(line):
                # Directory, so we need to show contents of directory
                #ret.extend(os.listdir(line))
                for f in os.listdir(line):
                    # Skip hidden
                    if f.startswith("."):
                        continue
                    f = os.path.join(line, f)
                    if os.path.isdir(f):
                        f += "/"
                    ret.append(f)
            else:
                # This is a file, but we could be looking for another file that
                # shares a common prefix.
                for f in os.listdir(os.path.dirname(line)):
                    if f.startswith(os.path.split(line)[1]):
                        ret.append(os.path.join( os.path.dirname(line), f))
        else:
            # This path does not exist, so lets do a listdir on it's parent
            # and find any matches.
            ret = []
            for f in os.listdir(os.path.dirname(line)):
                if f.startswith(os.path.split(line)[1]):
                    p = os.path.join(os.path.dirname(line), f)

                    if os.path.isdir(p):
                        p += "/"
                    ret.append(p)

        return ret
