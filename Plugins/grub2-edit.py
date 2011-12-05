# -*- coding: utf-8 -*-
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

import gtk
import os
from OjubaControlCenter.utils import cmd_out, copyfile
from OjubaControlCenter.widgets import InstallOrInactive, sure, info, error, wait
from OjubaControlCenter.pluginsClass import PluginsClass

class occPlugin(PluginsClass):
  conf={}
  conf[0]={}
  conf[1]={}
  conf_fn='/etc/default/grub'
  user_conf=os.path.join(os.path.expanduser('~'),'.occ','grub')
  font_fn='/usr/share/fonts/dejavu/DejaVuSansMono.ttf'
  font_nm='Sans'
  bg_nm=os.path.join(os.path.expanduser('~'),'.occ','grub2.png')
  bg_fn='/usr/share/backgrounds/verne/default/normalish/verne.png'
  gfxmode='auto'
  def __init__(self,ccw):
    PluginsClass.__init__(self, ccw,_('Grub2 settings:'),'boot',30)
    self.default_conf()
    self.load_conf(0,self.conf_fn)
    self.load_conf(1,self.user_conf)
    
    vb=gtk.VBox(False,2)
    self.add(vb)

    h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    l=gtk.Label(_("This section will help you to change grub2 settings"))
    h.pack_start(l, False,False,2)
    
    h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    h.pack_start(gtk.Label('%s :' % _("Time out")), False,False,2)
    self.Time_Out = b = gtk.SpinButton(gtk.Adjustment(1, 1, 90, 1, 1))
    h.pack_start(b, False,False,2)
    h.pack_start(gtk.Label(_("Seconds")), False,False,2)
    
    h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    h.pack_start(gtk.Label('%s :' % _("Kernel options")), False,False,2)
    self.Kernel_Opt = e = gtk.Entry()
    e.set_width_chars(50)
    h.pack_start(e, False,False,2)
    
    h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    self.recovery_c = c = gtk.CheckButton(_('Enabel recovery option'))
    h.pack_start(c, False,False,2)
    
    h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    self.theme_c = c = gtk.CheckButton(_('Enabel Grub2 theme'))
    c.connect('toggled',self.update_theme_cb)
    h.pack_start(c, False,False,2)
    
    if os.path.isfile(self.conf[1]['FONT_FILE']): self.font_fn=self.conf[1]['FONT_FILE']
    self.font_nm = self.conf[1]['FONT_NAME']
    self.gfxmode = self.conf[0]['GRUB_GFXMODE']
    self.bg_fn = self.conf[1]['BACKGROUND']
    # Grub2 theme frame
    self.tf = f = gtk.Frame(_('Grub2 Theme:')); vb.pack_start(f,False,False,6)
    vbox = gtk.VBox(False,2)
    f.add(vbox)
    
    h=gtk.HBox(False,2); vbox.pack_start(h,False,False,6)
    l=gtk.Label(_("This section will help you to change grub2 Font and background (theme)."))
    h.pack_start(l, False,False,2)
    
    h=gtk.HBox(False,2); vbox.pack_start(h,False,False,6)
    # TODO: customizable BACKGROUND
    l=gtk.Label("%s: %s" %(_("Background"),self.bg_fn))
    b=gtk.Button(_('Change picture'))
    b.connect('clicked', self.open_pic_cb, l)
    h.pack_start(b, False,False,2)
    h.pack_start(l, False,False,2)
    
    h=gtk.HBox(False,2); vbox.pack_start(h,False,False,6)
    self.gfxmode_c = c = gtk.CheckButton('%s  = %s' %(_("Set GFXMODE"), self.gfxmode))
    c.connect('toggled',self.set_gfxmode_cb)
    c.set_tooltip_markup(_('Enable this option if you have boot troubles\n\nIf your monitor got out sync or turned off, While grub2 menu\nPress enter to continue booting, And enable this option.'))
    c.set_active(self.conf[0]['GRUB_GFXMODE']=='800x600')
    h.pack_start(c, False,False,2)
    
    h=gtk.HBox(False,2); vbox.pack_start(h,False,False,6)
    l=gtk.Label("%s: %s" %(_("Font name"),self.font_fn))
    b = gtk.FontButton()
    b.connect('font-set', self.fc_match_cb, l)
    b.set_font_name(self.conf[1]['FONT_NAME']  + ' 12')
    b.set_size_request(300,-1)
    h.pack_start(b, False,False,2)
    h.pack_start(l, False,False,2)
    
    # Apply buuton
    h=gtk.HBox(False,2); vb.pack_start(h,False,False,6)
    self.apply_b = b = gtk.Button(_('Apply'))
    b.connect('clicked', self.apply_cb)
    b.set_size_request(200,-1)
    h.pack_end(b, False,False,2)
    self.Time_Out.set_value(self.conf[0]['GRUB_TIMEOUT'])
    self.Kernel_Opt.set_text(self.conf[0]['GRUB_CMDLINE_LINUX'][1:-1])
    self.recovery_c.set_active(not self.conf[0]['GRUB_DISABLE_RECOVERY']=='true')
    self.theme_c.set_active(True)
    #self.theme_c.set_active(self.conf.has_key('GRUB_BACKGROUND') and self.conf['GRUB_BACKGROUND'] != '')
    self.theme_c.set_active(os.path.isfile('/boot/grub2/unicode.pf2'))
    
  def open_pic_cb(self, b, l):
    dlg=gtk.FileChooserDialog(_("Select PNG image data 8-bit/color RGBA file"),buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
    ff=gtk.FileFilter()
    ff.add_mime_type('image/png')
    #ff.add_pattern('*.png')
    dlg.set_filter(ff)
    dlg.set_filename(self.bg_fn)
    dlg.connect('delete-event', lambda w, *a: w.hide() or True)
    dlg.connect('response', lambda w, *a: w.hide() or True)
    err=0
    if (dlg.run()==gtk.RESPONSE_ACCEPT):
      fn=dlg.get_filename()
      if self.png_match(fn):
        self.bg_fn=fn
        l.set_text("%s: %s" %(_("Background"),self.bg_fn))
      else: err=1
    dlg.hide()
    if err: error('%s:\n%s\n%s %s' %(_('Error: This file'),fn,_('is not'),'8-bit/color RGBA, PNG image data'),self.ccw)
  
  def png_match(self, fn):
    if not os.path.isfile(fn): return False
    f = ' '.join(cmd_out("file \"%s\"" % fn)[0].split(':')[1].split()[0:-1])
    if 'PNG image data' in f and '8-bit/color RGBA' in f : return True
    return False
    
  def update_theme_cb(self, b):
    self.tf.set_sensitive(b.get_active())

  def set_gfxmode_cb(self, b):
    if b.get_active():
      self.gfxmode='800x600'
    else:
      self.gfxmode='auto'
      
  def fc_match_cb(self, b, l):
    font=b.get_font_name().split()[:-1]
    font = ' '.join(font)
    fn = cmd_out("fc-match -f '%%{file}\n' '%s'" % font)[0]
    if os.path.splitext(fn)[1][1:] != 'ttf':
      b.set_font_name(self.font_nm + ' 12') 
      return error('%s (%s)' %(_('Error: Can not use this font!'),font),self.ccw)
    #print font, fn
    if os.path.isfile(fn):
      self.font_nm=font
      self.font_fn=fn
      l.set_text("%s: %s" %(_("Font name"),self.font_fn))
    
  def apply_cb(self, w):
    if not sure(_('Are you sure you want to changes?'), self.ccw): return
    if not os.path.isdir(os.path.dirname(self.bg_nm)):
      os.mkdir(os.path.dirname(self.bg_nm))
    if not copyfile(self.bg_fn,self.bg_nm):
      return error('%s\n%s' %(_('This file can not be used, As Grub back ground:'),self.bg_fn),self.ccw)
    dlg=wait(self.ccw)
    dlg.show_all()
    self.conf[0]['GRUB_TIMEOUT'] = int(self.Time_Out.get_value())
    self.conf[0]['GRUB_DISTRIBUTOR'] = self.conf[0]['GRUB_DISTRIBUTOR']
    self.conf[0]['GRUB_DISABLE_RECOVERY'] = str(not self.recovery_c.get_active()).lower()
    self.conf[0]['GRUB_DEFAULT'] = self.conf[0]['GRUB_DEFAULT']
    self.conf[0]['GRUB_CMDLINE_LINUX'] = '"' + self.Kernel_Opt.get_text() + '"'
    self.conf[0]['GRUB_GFXMODE'] = self.gfxmode
    self.conf[0]['GRUB_GFXPAYLOAD_LINUX'] = "keep"
    self.conf[0]['GRUB_BACKGROUND'] = '/boot/grub2/oj.grub2.png'
    self.conf[1]['BACKGROUND'] = self.bg_fn
    self.conf[1]['FONT_FILE'] = self.font_fn
    self.conf[1]['FONT_NAME'] = self.font_nm
    font=self.font_fn
    if not self.theme_c.get_active(): font=''
    s = '\n'.join(map(lambda k: "%s=%s" % (k,str(self.conf[0][k])), self.conf[0].keys()))
    m = '\n'.join(map(lambda k: "%s=%s" % (k,str(self.conf[1][k])), self.conf[1].keys()))
    open(self.user_conf, 'w+').write(m)
    #print m, '\n\n',s,font, self.bg_fn,self.bg_nm
    #return
    r = self.ccw.mechanism('grub2', 'apply_cfg', self.conf_fn, s, font, self.bg_nm)
    dlg.hide()
    if r == 'NotAuth': return 
    if r.startswith("Error"): return error('%s: %s' %(_('Error!'),r),self.ccw)
    info(_('Done!'),self.ccw)

  def load_conf(self,n,fn):
    s=''
    if os.path.exists(fn):
      try: s=open(fn,'rt').read()
      except OSError: pass
    self.parse_conf(s,n)
    try: self.conf[0]['GRUB_TIMEOUT'] = int(self.conf[0]['GRUB_TIMEOUT'])
    except ValueError:self.conf[0]['GRUB_TIMEOUT'] = 5

  def parse_conf(self, s,n):
    l1=map(lambda k: k.split('=',1), filter(lambda j: j,map(lambda i: i.strip(),s.splitlines())) )
    l2=map(lambda a: (a[0].strip(),a[1].strip()),filter(lambda j: len(j)==2,l1))
    r=dict(l2)
    self.conf[n].update(dict(l2))
    return len(l1)==len(l2)

  def default_conf(self):
    self.conf={}
    self.conf[0] = {}
    self.conf[1] = {}
    self.conf[0]['GRUB_TIMEOUT'] = 0
    self.conf[0]['GRUB_DISTRIBUTOR'] = "Fedora"
    self.conf[0]['GRUB_DISABLE_RECOVERY'] = "false"
    self.conf[0]['GRUB_DEFAULT'] = "saved"
    self.conf[0]['GRUB_CMDLINE_LINUX'] = '''"rd.md=0 rd.lvm=0 rd.dm=0  KEYTABLE=us quiet SYSFONT=latarcyrheb-sun16 rhgb rd.luks=0 LANG=en_US.UTF-8"'''
    self.conf[0]['GRUB_GFXMODE'] = self.gfxmode
    self.conf[0]['GRUB_GFXPAYLOAD_LINUX'] = "keep"
    self.conf[0]['GRUB_BACKGROUND'] = '/boot/grub2/oj.grub2.png'
    self.conf[1]['BACKGROUND'] = self.bg_fn
    self.conf[1]['FONT_FILE'] = self.font_fn
    self.conf[1]['FONT_NAME'] = self.font_nm
