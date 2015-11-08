#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
#  Copyright (C) 2014 Daniel Rodriguez
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from utils.mvc import DynamicClass, PubSend


@DynamicClass(moddirs=['modules'])
class MainModel(object):
    MOTD = [
        # MOTD 1
        'Anyone can write a program a computer can understand\n',
        # MOTD 2
        'This is the last MOTD',
    ]

    def __init__(self):
        self.next_motd = 0

    @PubSend('model.next_motd')
    def GetNextMOTD2(self):
        motd = self.MOTD[self.next_motd]
        self.next_motd += 1
        if self.next_motd == len(self.MOTD):
            self.next_motd = 0

        return motd

    @PubSend('model.next_motd')
    def GetNextMOTD(self):
        return self.Hola()

    def Hola(self):
        motd = self.MOTD[self.next_motd]
        self.next_motd += 1
        if self.next_motd == len(self.MOTD):
            self.next_motd = 0

        return motd
