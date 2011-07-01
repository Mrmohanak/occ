# -*- coding: utf-8 -*-
"""
Ojuba Control Center
Copyright © 2009, Muayyad Alsadi <alsadi@ojuba.org>

    Released under terms of Waqf Public License.
    This program is free software; you can redistribute it and/or modify
    it under the terms of the latest version Waqf Public License as
    published by Ojuba.org.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

    The Latest version of the license can be found on
    "http://waqf.ojuba.org/license"
"""
import gtk

from OjubaControlCenter.pluginsClass import PluginsClass
from OjubaControlCenter.widgets import LaunchButton

class occPlugin(PluginsClass):
  def __init__(self,ccw):
    PluginsClass.__init__(self, ccw,_('Gnome Control Center'),'gnome',50)
    vb=gtk.VBox(False,2)
    self.add(vb)
    hb=gtk.HBox(False,0)
    #hb.pack_start(gtk.image_new_from_icon_name('gnome-control-center', gtk.ICON_SIZE_BUTTON),False,False,0)
    #hb.pack_start(LaunchOrInstall(self,_('GNOME Control Center'),'/usr/bin/gnome-control-center',['control-center']),False,False,0)
    hb.pack_start(LaunchButton(_('GNOME Control Center'),'/usr/bin/gnome-control-center',icon='gnome-control-center'),False,False,0)
    hb.pack_start(LaunchButton(_('GNOME Menu Editor'),'/usr/bin/alacarte',icon='alacarte'),False,False,0)
    vb.pack_start(hb,False,False,6)

