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
from OjubaControlCenter.gwidgets import resetButton, GSCheckButton, mainGSCheckButton

class occPlugin(PluginsClass):
  def __init__(self,ccw):
    PluginsClass.__init__(self, ccw,_('Desktop Icons'),'gnome',20)
    SD_P='org.gnome.desktop.background'
    DT_P='org.gnome.nautilus.desktop'
    mvb=gtk.VBox(False,2)
    vb=gtk.VBox(False,2)
    self.add(mvb)
    h=gtk.HBox(False,0)
    h.pack_start(gtk.Label(_('Select the icons you want to be visible on desktop')),False,False,0)
    mvb.pack_start(h,False,False,6)
    GS = ccw.GSettings(SD_P)
    c=mainGSCheckButton(vb,_('Show desktop icons'),'show-desktop-icons',GS)
    vb.pack_start(c,False,False,1)
    GS = ccw.GSettings(DT_P)
    DT_l=( \
       (_('Computer'),'computer-icon-visible'),
       (_('Home'),'home-icon-visible'),
       (_('Network'),'network-icon-visible'),
       (_('Trash'),'trash-icon-visible'),
       (_('Mounted volumes'),'volumes-visible')
    )
    
    for t,k in DT_l:
      g=GSCheckButton(t,k,GS)
      vb.pack_start(g,False,False,1)
    c.update_cboxs()
    b = resetButton(vb)
    mvb.pack_start(vb,False,False,1)
    mvb.pack_start(b,False,False,1)

