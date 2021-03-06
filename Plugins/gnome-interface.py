# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent syntax=python
# -*- Mode: Python; py-indent-offset: 4 -*-
"""
Ojuba Control Center
Copyright © 2009, Ojuba Team <core@ojuba.org>

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

from gi.repository import Gtk
import os
from OjubaControlCenter.pluginsClass import PluginsClass
from OjubaControlCenter.gwidgets import resetButton, GSCheckButton, comboBox, comboBoxWithFolder, creatVBox
from OjubaControlCenter.widgets import InstallOrInactive

## NOTE: these global vars is loader validators
category = 'gnome'
caption = _('Shell Interface')
description = _("Adjust interface settings")
priority = 40

class occPlugin(PluginsClass):
    def __init__(self,ccw):
        PluginsClass.__init__(self, ccw, caption, category, priority)
        self.GConf=ccw.GConf
        self.dirs=self.get_dirs()
        creatVBox(self, ccw, description, self.GioSettings) 
        
    def GioSettings(self, vb, ccw):
        P='org.gnome.desktop.interface'
        FB_l = ()
        if P in ccw.GSchemas_List: 
            GS = ccw.GSettings(P)
            FB_l=( \
                 (_('Show seconds in clock'),'clock-show-seconds'),
                 (_('Show date in clock'),'clock-show-date'),
                 (_('Menus have icons'),'menus-have-icons'),
                 (_('Buttons have icons'),'buttons-have-icons')
                )
            ret = True
        for t,k in FB_l:
            if k in GS.list_keys():
                b=GSCheckButton(t,k,GS)
                vb.pack_start(b,False,False,1)
        tf=comboBox(_('Clock format'),'clock-format',GS, GS.get_range('clock-format')[1])
        vb.pack_start(tf,False,False,1)
        PP="org.gnome.shell.extensions.user-theme"
        b=InstallOrInactive(self, 'Install Gnome shell extension user theme','Gnome shell extension user theme installed','Package used to change Gnome shell theme',['gnome-shell-extension-user-theme'],'/usr/share/glib-2.0/schemas/org.gnome.shell.extensions.user-theme.gschema.xml')
        P_Stst=b.get_sensitive()
        if not P_Stst:
            GSP = ccw.GSettings(PP)
            cb=comboBoxWithFolder(_('Shell theme'),'name',GSP,self.get_shell_themes(),_('Add Shell theme'),os.path.expanduser('~/.themes'), self.get_shell_themes)
            vb.pack_start(cb,False,False,1)
        else:
            vb.pack_start(b,False,False,1)
        FD_l=( \
             (_('GTK+ theme'),'gtk-theme',self.get_gtk_themes(),_('Add GTK+ theme'),os.path.expanduser('~/.themes'), self.get_gtk_themes),
             (_('Icon theme'),'icon-theme',self.get_valid_icon_themes(),_('Add icons theme'),os.path.expanduser('~/.icons'), self.get_valid_icon_themes),
             (_('Cursor theme'),'cursor-theme',self.get_valid_cursor_themes(),_('Add cursor theme'),os.path.expanduser('~/.icons'), self.get_valid_cursor_themes)
        )
        for t,k,l,bt,dst,ls_func in FD_l:
            cb=comboBoxWithFolder(t,k,GS, l, bt, dst, ls_func)
            vb.pack_start(cb,False,False,1)
        return ret

    def get_metacity_themes(self):
        valid = self.walk_directories(self.dirs['themes'], lambda d:
                         os.path.exists(os.path.join(d, "metacity-1")))
        return valid
        
    def get_gtk_themes(self):
        """ Only shows themes that have variations for gtk+-3 and gtk+-2 """
        valid = self.walk_directories(self.dirs['themes'], lambda d:
                         os.path.exists(os.path.join(d, "gtk-2.0")) and \
                         os.path.exists(os.path.join(d, "gtk-3.0")))
        return valid
    
    def get_shell_themes(self):
        """ Only shows themes that have variations for gtk+-3 and gtk+-2 """
        valid = self.walk_directories(self.dirs['themes'], lambda d:
                         os.path.exists(os.path.join(d, "gnome-shell")) and \
                         os.path.exists(os.path.join(d, "gnome-shell", "gnome-shell.css")))
        valid.append('')
        return valid
        
    def get_valid_cursor_themes(self):
        valid = self.walk_directories(self.dirs['icons'], lambda d:
                            os.path.isdir(d) and \
                            os.path.exists(os.path.join(d, "cursors")))
        return valid
    
    def get_valid_icon_themes(self):
        valid = self.walk_directories(self.dirs['icons'], lambda d:
                         os.path.isdir(d) and \
                         not os.path.exists(os.path.join(d, "cursors")))
        return valid
        
    def get_dirs(self):
        dirs={}
        dirs['icons'] =    ( os.path.join('/usr/share/', "icons"),
                                             os.path.join(os.path.expanduser("~"), ".icons"))
        dirs['themes'] = ( os.path.join('/usr/share/', "themes"),
                                             os.path.join(os.path.expanduser("~"), ".themes"))
        return dirs

    def walk_directories(self, dirs, filter_func):
        valid = []
        try:
                for thdir in dirs:
                        if os.path.isdir(thdir):
                                for t in os.listdir(thdir):
                                        if filter_func(os.path.join(thdir, t)):
                                                 valid.append(t)
        except: pass
        return valid
