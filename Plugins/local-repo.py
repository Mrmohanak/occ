# -*- coding: utf-8 -*-
"""
Ojuba Control Center
Copyright © 2011, Ojuba.org <core@ojuba.org>

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
import os
import re
from OjubaControlCenter.utils import cmd_out
from OjubaControlCenter.widgets import NiceButton, InstallOrInactive, wait, sure, info, error, sel_dir_dlg
from OjubaControlCenter.pluginsClass import PluginsClass

class occPlugin(PluginsClass):
  repo_fn="/etc/yum.repos.d/local-occ.repo"
  tdir_re=re.compile('''[\s\t]*baseurl[\s\t]*=[\s\t]*file://(.*)''')
  def __init__(self,ccw):
    PluginsClass.__init__(self, ccw,_('Local repository:'),'install',8)
    self.tdir=self.get_repo_path_cb()
    vb=gtk.VBox(False,2)
    self.add(vb)
    h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    l=gtk.Label(_("Ojuba can create local rpository for you!"))
    h.pack_start(l,False,False,2)
    
    h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    b=gtk.Button(_('Change directory'))
    b.connect('clicked', self.ch_dir_cb)
    h.pack_start(b, False,False,2)
    l=gtk.Label(_("Repository directory:"))
    h.pack_start(l,False,False,2)
    self.repo_dir_l = l = gtk.Label(self.tdir)
    h.pack_start(l,False,False,2)
    
    h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    self.gen_info_c = c = gtk.CheckButton(_("Generate local repository informations"))
    #c.set_active(True)
    c.connect("toggled", self.ch_apply_b_sens)
    h.pack_start(c, False,False,2)
    self.write_config_c = c = gtk.CheckButton(_("Write local repository configuration"))
    #c.set_active(True)
    c.connect("toggled", self.ch_apply_b_sens)
    h.pack_start(c, False,False,2)
    
    h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    self.apply_b = b = gtk.Button(_('Create local repository'))
    b.connect('clicked', self.apply_cb)
    h.pack_start(b, False,False,2)
    self.ch_apply_b_sens()
    
  def ch_apply_b_sens(self, *b):
    s=(self.gen_info_c.get_active() or self.write_config_c.get_active()) and os.path.isdir(self.tdir)
    self.apply_b.set_sensitive(s)
        
  def ch_dir_cb(self, *b):
    tdir_dlg=sel_dir_dlg()
    if os.path.isdir(self.tdir):
      tdir_dlg.set_filename(self.tdir)
    if (tdir_dlg.run()==gtk.RESPONSE_ACCEPT):
      self.tdir = tdir_dlg.get_filename()
      tdir_dlg.hide()
      self.repo_dir_l.set_text(self.tdir)
    else:
      tdir_dlg.hide()
    return self.ch_apply_b_sens()
    
  def apply_cb(self, *b):
    if not os.path.isdir(self.tdir):
      return error(_("Select repository directory frist!"), self.ccw)
    dlg=wait(self.ccw)
    dlg.show_all()
    ret=False
    if self.gen_info_c.get_active():
      s=self.create_repo_cb(self.tdir)
      if s: dlg.hide(); return error(s)
      ret=True
    if self.write_config_c.get_active():
      if self.write_repo_cb(self.tdir) == '0': ret=True
    dlg.hide()
    if ret:info(_("Done!"), self.ccw)
    
  def get_repo_path_cb(self):
    fn=self.repo_fn
    if not os.path.isfile(fn): return 'None'
    l=open(self.repo_fn, 'r').read().strip()
    m=self.tdir_re.findall(l)[0]
    if m:return m
    return 'None'
    
  def create_repo_cb(self, tdir):
    return cmd_out('''createrepo "%s"''' %tdir)[1]
    
  def write_repo_cb(self, tdir):
    file_cont="""[local-occ]\nname=local-occ\nbaseurl=file://%s\nenabled=1\ngpgcheck=0\ncost=400\nskip_if_unavailable=1""" %tdir
    # FIXME: UnicodeEncodeError when writing arabic using mech
    #return self.ccw.mechanism('run', 'write_conf', self.repo_fn, file_cont)
    # instead 
    tfn=os.path.join(os.path.expanduser('~'), '.local-repo')
    open(tfn, 'wt+').write(file_cont)
    cmd='mv -f "%s" "%s"' %(tfn, self.repo_fn)
    return self.ccw.mechanism('run', 'system', cmd)
    
