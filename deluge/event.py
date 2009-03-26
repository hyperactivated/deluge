#
# event.py
#
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

"""
Event module.

This module describes the types of events that can be generated by the daemon
and subsequently emitted to the clients.

"""

class DelugeEvent(object):
    """
    The base class for all events.

    :prop name: this is the name of the class which is in-turn the event name
    :prop args: a list of the attribute values

    """
    def _get_name(self):
        return self.__class__.__name__

    def _get_args(self):
        if not hasattr(self, "_args"):
            return []
        return self._args

    name = property(fget=_get_name)
    args = property(fget=_get_args)

class TorrentAddedEvent(DelugeEvent):
    """
    Emitted when a new torrent is successfully added to the session.
    """
    def __init__(self, torrent_id):
        """
        :param torrent_id: str, the torrent_id of the torrent that was added
        """
        self._args = [torrent_id]

class TorrentRemovedEvent(DelugeEvent):
    """
    Emitted when a torrent has been removed from the session.
    """
    def __init__(self, torrent_id):
        """
        :param torrent_id: str, the torrent_id
        """
        self._args = [torrent_id]

class PreTorrentRemovedEvent(DelugeEvent):
    """
    Emitted when a torrent is about to be removed from the session.
    """
    def __init__(self, torrent_id):
        """
        :param torrent_id: str, the torrent_id
        """
        self._args = [torrent_id]

class TorrentStateChangedEvent(DelugeEvent):
    """
    Emitted when a torrent changes state.
    """
    def __init__(self, torrent_id, state):
        """
        :param torrent_id: str, the torrent_id
        :param state: str, the new state
        """
        self._args = [torrent_id, state]

class TorrentQueueChangedEvent(DelugeEvent):
    """
    Emitted when the queue order has changed.
    """
    pass

class TorrentFolderRenamedEvent(DelugeEvent):
    """
    Emitted when a folder within a torrent has been renamed.
    """
    def __init__(self, torrent_id, old, new):
        """
        :param torrent_id: str, the torrent_id
        :param old: str, the old folder name
        :param new: str, the new folder name
        """
        self._args = [torrent_id, old, new]

class TorrentFileRenamedEvent(DelugeEvent):
    """
    Emitted when a file within a torrent has been renamed.
    """
    def __init__(self, torrent_id, index, name):
        """
        :param torrent_id: str, the torrent_id
        :param index: int, the index of the file
        :param name: str, the new filename
        """
        self._args = [torrent_id, index, name]

class TorrentFinishedEvent(DelugeEvent):
    """
    Emitted when a torrent finishes downloading.
    """
    def __init__(self, torrent_id):
        """
        :param torrent_id: str, the torrent_id
        """
        self._args = [torrent_id]

class TorrentResumedEvent(DelugeEvent):
    """
    Emitted when a torrent resumes from a paused state.
    """
    def __init__(self, torrent_id):
        """
        :param torrent_id: str, the torrent_id
        """
        self._args = [torrent_id]

class NewVersionAvailableEvent(DelugeEvent):
    """
    Emitted when a more recent version of Deluge is available.
    """
    def __init__(self, new_release):
        """
        :param new_release: str, the new version that is available
        """
        self._args = [new_release]

class SessionStartedEvent(DelugeEvent):
    """
    Emitted when a session has started.  This typically only happens once when
    the daemon is initially started.
    """
    pass

class SessionPausedEvent(DelugeEvent):
    """
    Emitted when the session has been paused.
    """
    pass

class SessionResumedEvent(DelugeEvent):
    """
    Emitted when the session has been resumed.
    """
    pass

class ConfigValueChangedEvent(DelugeEvent):
    """
    Emitted when a config value changes in the Core.
    """
    def __init__(self, key, value):
        """
        :param key: str, the key that changed
        :param value: the new value of the `:param:key`
        """
        self._args = [key, value]
