# -*- coding: utf-8 -*-


import sys
import copy
import collections
if sys.version_info[0] > 2:
    str = str
try:
    import cdecimal as decimal
except ImportError:
    import decimal
from django.utils.translation import gettext as _
from . import botslib
from . import botsglobal
from .botsconfig import *

class Node(object):
    ''' Node class for building trees in python programs.
        Used for:
        - building tree of segments (from edi-file).
        - building structured records (from edi-file).
        - as tree to store results of queries on edi-file
        - parameter for mappings.
    '''
    __slots__ = ('record', 'children', 'parent', '_queries', 'linpos_info', 'structure')

    def __init__(self, record=None, linpos_info=None):
        if record and 'BOTSIDnr' not in record:
            record['BOTSIDnr'] = '1'
        self.record = record
        self.children = []
        self.parent = None
        self._queries = None
        self.linpos_info = linpos_info
        self.structure = None

    def __len__(self):
        return len(self.children)

    def __getitem__(self, key):
        if isinstance(key, str):
            if self.record and key in self.record:
                if isinstance(self.record[key], list):
                    return self.record[key][0]
                else:
                    return self.record[key]
        elif isinstance(key, int):
            return self.children[key]

    def __setitem__(self, key, value):
        if isinstance(key, str):
            if self.record is None:
                self.record = {}
            if key not in self.record:
                self.record[key] = value
            elif isinstance(self.record[key], list):
                self.record[key].append(value)
            else:
                self.record[key] = [self.record[key], value]
        else:
            raise KeyError('Key must be a string')

    def __contains__(self, key):
        return key in self.record if self.record else False

    def get(self, *mpaths):
        if Node.checklevel:
            self._mpath_sanity_check(mpaths[:-1])
            if not isinstance(mpaths[-1], dict):
                raise botslib.MappingFormatError(_('Must be dicts in tuple: get(%(mpath)s)'), {'mpath': mpaths})
            if 'BOTSID' not in mpaths[-1]:
                raise botslib.MappingFormatError(_('Last section without "BOTSID": get(%(mpath)s)'), {'mpath': mpaths})
            count = 0
            for key, value in list(mpaths[-1].items()):
                if not isinstance(key, str):
                    raise botslib.MappingFormatError(
                        _('Keys must be strings in last section: get(%(mpath)s)'), {'mpath': mpaths})
                if value is None:
                    count += 1
                elif not isinstance(value, str):
                    raise botslib.MappingFormatError(
                        _('Values must be strings (or none) in last section: get(%(mpath)s)'), {'mpath': mpaths})
            if count > 1:
                raise botslib.MappingFormatError(_('Max one "None" in last section: get(%(mpath)s)'), {'mpath': mpaths})
        for part in mpaths:
            if 'BOTSIDnr' not in part:
                part['BOTSIDnr'] = '1'
        if Node.checklevel == 2:
            self._mpath_grammar_check(mpaths)
        terug = self._getcore(mpaths)
        botsglobal.logmap.debug('"%(terug)s" for get%(mpaths)s', {'terug': terug, 'mpaths': str(mpaths)})
        return terug

    def append(self, childnode):
        childnode.parent = self
        self.children.append(childnode)

    def display(self, level=0):
        if level == 0:
            print('displaying all nodes in node tree:')
        print(('    ' * level, self.record))
        for childnode in self.children:
            childnode.display(level + 1)

    def getcount(self):
        count = 0
        if self.record:
            count += 1
        for child in self.children:
            count += child.getcount()
        return count

    def linpos(self):
        if self.linpos_info:
            return ' line %(lin)s pos %(pos)s' % {'lin': self.linpos_info[0], 'pos': self.linpos_info[1]}
        else:
            return ''

    def _getcore(self, mpaths):
        if len(mpaths) != 1:
            for key, value in list(mpaths[0].items()):
                if key not in self.record or value != self.record[key]:
                    return None
            else:
                for childnode in self.children:
                    terug = childnode._getcore(mpaths[1:])
                    if terug is not None:
                        return terug
                else:
                    return None
        else:
            terug = 1
            for key, value in list(mpaths[0].items()):
                if key not in self.record:
                    return None
                elif value is None:
                    terug = self.record[key][:]
                elif value != self.record[key]:
                    return None
            else:
                return terug

    def put(self, *mpaths, **kwargs):
        if not mpaths or not isinstance(mpaths, tuple):
            raise botslib.MappingFormatError(_('Must be dicts in tuple: put(%(mpath)s)'), {'mpath': mpaths})
        for part in mpaths:
            if not isinstance(part, dict):
                raise botslib.MappingFormatError(_('Must be dicts in tuple: put(%(mpath)s)'), {'mpath': mpaths})
            if 'BOTSID' not in part:
                raise botslib.MappingFormatError(_('Section without "BOTSID": put(%(mpath)s)'), {'mpath': mpaths})
            for key, value in list(part.items()):
                if value is None:
                    botsglobal.logmap.debug('"None" in put %(mpaths)s.', {'mpaths': str(mpaths)})
                    return False
                if not isinstance(key, str):
                    raise botslib.MappingFormatError(_('Keys must be strings: put(%(mpath)s)'), {'mpath': mpaths})
                if isinstance(value, list):
                    if not value:
                        botsglobal.logmap.debug('Empty list in put %(mpaths)s.', {'mpaths': str(mpaths)})
                        return False
                else:
                    if kwargs.get('strip', True):
                        part[key] = str(value).strip()
                    else:
                        part[key] = str(value)
            if 'BOTSIDnr' not in part:
                part['BOTSIDnr'] = '1'

        if self._sameoccurence(mpaths[0]):
            self._putcore(mpaths[1:])
        else:
            raise botslib.MappingRootError(_('Error in root put "%(mpath)s".'), {'mpath': mpaths[0]})
        botsglobal.logmap.debug('"True" for put %(mpaths)s', {'mpaths': str(mpaths)})
        return True

    def _putcore(self, mpaths):
        if not mpaths:
            return
        for childnode in self.children:
            if childnode.record['BOTSID'] == mpaths[0]['BOTSID'] and childnode._sameoccurence(mpaths[0]):
                childnode._putcore(mpaths[1:])
                return
        else:
            self.append(Node(mpaths[0]))
            self.children[-1]._putcore(mpaths[1:])

    def _sameoccurence(self, mpath):
        for key, value in list(self.record.items()):
            if key in mpath and mpath[key] != value:
                return False
        else:
            self.record.update(mpath)
            return True

    def _mpath_sanity_check(self, mpaths):
        if not isinstance(mpaths, tuple):
            raise botslib.MappingFormatError(_('Parameter mpath must be tuple: %(mpaths)s'), {'mpaths': mpaths})
        for part in mpaths:
            if not isinstance(part, dict):
                raise botslib.MappingFormatError(
                    _('Parameter mpath must be dicts in a tuple: %(mpaths)s'), {'mpaths': mpaths})
            if 'BOTSID' not in part:
                raise botslib.MappingFormatError(_('"BOTSID" is required in mpath: %(mpaths)s'), {'mpaths': mpaths})
            for key, value in list(part.items()):
                if not isinstance(key, str):
                    raise botslib.MappingFormatError(_('Keys must be strings in mpath: %(mpaths)s'), {'mpaths': mpaths})
                if not isinstance(value, str):
                    raise botslib.MappingFormatError(
                        _('Values must be strings in mpath: getrecord(%(mpaths)s)'), {'mpaths': mpaths})

    def _mpath_grammar_check(self, mpaths):
        def _mpath_ok_with_grammar(structure, mpaths):
            mpath = mpaths[0]
            for record_definition in structure:
                if record_definition[ID] == mpath['BOTSID'] and record_definition[BOTSIDNR] == mpath['BOTSIDnr']:
                    for key in mpath:
                        if key == 'BOTSIDnr':
                            continue
                        for field_definition in record_definition[FIELDS]:
                            if field_definition[ISFIELD]:
                                if key == field_definition[ID]:
                                    break
                            else:
                                if key == field_definition[ID]:
                                    break
                                for grammarsubfield in field_definition[SUBFIELDS]:
                                    if key == grammarsubfield[ID]:
                                        break
                                else:
                                    continue
                                break
                        else:
                            return False
                    if mpaths[1:]:
                        if not LEVEL in record_definition:
                            return False
                        return _mpath_ok_with_grammar(record_definition[LEVEL], mpaths[1:])
                    else:
                        return True
            else:
                return False
        if not self.structure:
            return
        if not _mpath_ok_with_grammar([self.structure], mpaths):
            raise botslib.MappingFormatError(
                _('Parameter mpath is not valid according to grammar: %(mpaths)s'), {'mpaths': mpaths})

    def getloop(self, *mpaths):
        if Node.checklevel:
            self._mpath_sanity_check(mpaths)
        for part in mpaths:
            if 'BOTSIDnr' not in part:
                part['BOTSIDnr'] = '1'
        if Node.checklevel == 2:
            self._mpath_grammar_check(mpaths)
        for terug in self._getloopcore(mpaths):
            botsglobal.logmap.debug('getloop %(mpaths)s returns "%(record)s".',
                                    {'mpaths': mpaths, 'record': terug.record})
            yield terug

    def _getloopcore(self, mpaths):
        for key, value in list(mpaths[0].items()):
            if key not in self.record or value != self.record[key]:
                return
        else:
            if len(mpaths) == 1:
                yield self
            else:
                for childnode in self.children:
                    for terug in childnode._getloopcore(mpaths[1:]):
                        yield terug

    def getnozero(self, *mpaths):
        terug = self.get(*mpaths)
        try:
            value = float(terug)
        except (TypeError, ValueError):
            return None
        if value == 0:
            return None
        return terug

    def getdecimal(self, *mpaths):
        terug = self.get(*mpaths)
        if terug and terug[-1] == '-':
            terug = terug[-1] + terug[:-1]
        try:
            return decimal.Decimal(terug)
        except (TypeError, ValueError):
            return decimal.Decimal('0')

    def enhance(self, query_node, enh_node):
        if enh_node is None:
            return
        if isinstance(enh_node, dict):
            self.record.update(enh_node)
        else:
            raise botslib.MappingFormatError(_('Enhance must be a dict: enhance(%(enh_node)s)'), {'enh_node': enh_node})

    def stripnode(self):
        if self.record is not None:
            for key, value in list(self.record.items()):
                self.record[key] = value.strip()
        for child in self.children:
            child.stripnode()

    def copynode(self):
        if self.record is None:
            new_node = Node(record=None)
        else:
            new_node = Node(record=dict(self.record))
        for childnode in self.children:
            new_node.append(childnode.copynode())
        return new_node