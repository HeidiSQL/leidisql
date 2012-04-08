# -*- coding: utf-8 -*-

import gtk
import hosts
import re
from window import loadmodule

class SessionManager(gtk.Window):
    
    def __init__ (self):
        super(SessionManager, self).__init__(gtk.WINDOW_TOPLEVEL)
        
        self.hostPathSelected = None
        self.hostSelected = None
        self.hostSelectedChange = False
        
        self.hosts = hosts.List()
        
        
        self.activate_focus()
        self.set_title(_("Session Manager"))
        self.set_resizable(False)
        self.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.set_border_width(7)
        
        self.add(self.__hbox())

        self.connect("destroy", gtk.main_quit)
        
        self.show_all()
    
    def __hbox(self):
        hbox = gtk.HBox()
        hbox.set_spacing(10)
            
        hbox.add(self.__listHosts())
        hbox.add(self.__tabs())
        
        return hbox
    
    def __listHosts(self):
        vbox = gtk.VBox(False)
        
        self.listStoreHost = gtk.ListStore(str)
        self.listHost = gtk.TreeView(self.listStoreHost)
        self.listHost.set_fixed_height_mode(gtk.TREE_VIEW_COLUMN_FIXED)
        self.listHost.set_size_request(-1, 220)
        self.listHost.connect("cursor-changed", self.on_select_host)
        
        scroll = ScrolledWindow()
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        scroll.add(self.listHost)
        vbox.pack_start(scroll)

        column = gtk.TreeViewColumn(_("Session name"))
        column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_fixed_width(170)
        column.set_resizable(False)
        
        
        cell_text = gtk.CellRendererText()
        cell_text.set_property("editable", True)
        cell_text.set_fixed_size(-1, 22)
        cell_text.set_padding(5, 0)
        column.pack_start(cell_text)
        column.add_attribute(cell_text, "text", 0)
        
        self.listHost.append_column(column)
        
        for host in self.hosts.iteritems():
            self.listStoreHost.append([host.name])
            
        self.listStoreHost.set_sort_column_id(0, gtk.SORT_ASCENDING)
        
        vbox.pack_start(self.__listHostBts(), padding=5)
        
        return vbox
    
    def __listHostBts(self):
        fixed = gtk.Fixed()
        
        btNew = gtk.Button()
        btNew.set_label(_("New"))
        btNew.set_size_request(50, -1)
        btNew.connect("clicked", self.on_new_host)
        fixed.put(btNew, 0, 0)
        
        btSave = gtk.Button()
        btSave.set_label(_("Save"))
        btSave.set_size_request(60, -1)
        btSave.connect("clicked", self.on_save_host)
        fixed.put(btSave, 55, 0)
        
        btDelete = gtk.Button()
        btDelete.set_label(_("Delete"))
        btDelete.set_size_request(70, -1)
        btDelete.connect("clicked", self.on_delte_host)
        fixed.put(btDelete, 120, 0)
        
        return fixed
    
    def __tabs(self):
        vbox = gtk.VBox(False)
        tabs = gtk.Notebook()
        vbox.pack_start(tabs)
        
        type = hosts.Type

        label = gtk.Label()
        label.set_text(type.get_tab_name(type.TAB_SETTINGS))
        tabs.append_page(self.__settings(), label)
        
        
        label = gtk.Label()
        label.set_text(type.get_tab_name(type.TAB_SSL_OPTIONS))
            #tabs.append_page(self.__fields(), label)

        label = gtk.Label()
        label.set_text(type.get_tab_name(type.TAB_STATISTCS))
        #tabs.append_page(self.__fields(), label)        
        
        
        vbox.pack_start(self.__bts_bottom_tabs(), padding=5)
        return vbox
    
    def __bts_bottom_tabs(self):
        align = gtk.Alignment(1, 1, 0, 0)
        
        
        fixed = gtk.Fixed()
        align.add(fixed)
        
        btOpen = gtk.Button()
        btOpen.set_label(_("Open"))
        btOpen.set_size_request(100, -1)
        btOpen.connect("clicked", self.on_open_host)
        fixed.put(btOpen, 0, 0)
        
        
        btCancel = gtk.Button()
        btCancel.set_label(_("Cancel"))
        btCancel.set_size_request(100, -1)
        btCancel.connect("clicked", gtk.main_quit)
        fixed.put(btCancel, 105, 0)
        
        return align
        
    def __settings(self):
        self._fields = {}
        vbox = gtk.VBox();
        
        vbox.pack_start(self.__combo_box(hosts.Type.FIELD_TYPE, hosts.Type.get_dbs()))
        vbox.pack_start(self.__entry(hosts.Type.FIELD_ADDRESS))
        vbox.pack_start(self.__entry(hosts.Type.FIELD_USER))
        vbox.pack_start(self.__entry(hosts.Type.FIELD_PASSWORD))
        vbox.pack_start(self.__spin_button(hosts.Type.FIELD_PORT))
        
        return vbox
    
    def __combo_box(self, field, model):
        listStore = gtk.ListStore(str);

        comboBox = gtk.ComboBox()
        comboBox.set_model(listStore)
        comboBox.connect("changed", self.on_change_field)
        
        
        cellText = gtk.CellRendererText()
        comboBox.pack_start(cellText, True)
        comboBox.add_attribute(cellText, "text", 0)
        
        for k in model:
            listStore.append([model[k]])
        
        return self.__join_label_field(field, comboBox)
    
    def __entry(self, field):
        entry = gtk.Entry()
        entry.set_visibility(True)
        entry.set_width_chars(25)
        
        entry.connect("changed", self.on_change_field)
        
        return self.__join_label_field(field, entry)
    
    def __spin_button(self, field):
        adj = gtk.Adjustment(1.0, 1.0, 65535.0, 1.0, 5.0, 0.0)
        spinButton = gtk.SpinButton(adj, 0, 0)
        spinButton.set_wrap(True)
        spinButton.connect("value-changed", self.on_change_field)
        
        return self.__join_label_field(field, spinButton)
    
    def __label(self, name):
        label = gtk.Label()
        label.set_width_chars(13)
        label.set_text(name + ":")
        label.set_alignment(0, 0)
        label.set_padding(0, 8)
        return label
    
    def __join_label_field(self, label, field):
        hbox = gtk.HBox()
        hbox.pack_start(self.__label(hosts.Type.get_label(label)), False, False, 5)
        hbox.pack_start(field)
        
        self._fields[label] = field
        return hbox
        
    def on_new_host(self, widget):
        host = self.hosts.create_host()
        self.hosts.add(host)
        iter = self.listStoreHost.append([host.name])

        self.hostSelected = host
        self.hostPathSelected = self.listStoreHost.get_path(iter)[0]
        
        self.listHost.set_cursor(self.hostPathSelected)
        self.__popula_fields()
        
        self.hostSelectedChange = False
    
    def on_delte_host(self, widget):
        if self.hostPathSelected != None and self.hostSelected != None:
            iter = self.listStoreHost.get_iter(self.hostPathSelected)
            self.listStoreHost.remove(iter)
            self.hosts.remove(self.hostSelected)
            
            self.__clear_fields()
            
            self.hostPathSelected = None
            self.hostSelected = None
            self.hostSelectedChange = False
    
    def on_select_host(self, widget):
        if self.hostSelectedChange:
            self.__dialog_save_changes()
        else:
            self.hostPathSelected = widget.get_cursor()[0][0]
            iter = self.listStoreHost.get_iter(self.hostPathSelected)
            self.hostSelected = self.hosts.get(self.listStoreHost.get_value(iter, 0))
            
            self.__popula_fields()
            self.hostSelectedChange = False
        
    def __popula_fields(self):
        host = self.hostSelected
        self._fields[hosts.Type.FIELD_TYPE].set_active(host.type.get_type())
        self._fields[hosts.Type.FIELD_ADDRESS].set_text(host.address)
        self._fields[hosts.Type.FIELD_USER].set_text(host.user)
        self._fields[hosts.Type.FIELD_PASSWORD].set_text(host.password)
        self._fields[hosts.Type.FIELD_PORT].set_text(host.port)
        
    def __clear_fields(self):
        self._fields[hosts.Type.FIELD_TYPE].set_active(-1)
        self._fields[hosts.Type.FIELD_ADDRESS].set_text("")
        self._fields[hosts.Type.FIELD_USER].set_text("")
        self._fields[hosts.Type.FIELD_PASSWORD].set_text("")
        self._fields[hosts.Type.FIELD_PORT].set_text("")
        
    def on_save_host(self, widget):
        host = self.hostSelected
        host.type = hosts.Type.create_type(self._fields[hosts.Type.FIELD_TYPE].get_active())
        host.address = self._fields[hosts.Type.FIELD_ADDRESS].get_text()
        host.user = self._fields[hosts.Type.FIELD_USER].get_text()
        host.password = self._fields[hosts.Type.FIELD_PASSWORD].get_text()
        host.port = self._fields[hosts.Type.FIELD_PORT].get_text()
        
        self.hosts.save(host)
        
        self.hostSelectedChange = False
        
    def on_change_field(self, widget):
        self.hostSelectedChange = True
        
    def __dialog_save_changes(self):
        message = _("Save modifications ? \n\n Settings for \"%s\" were changed.") % (self.hostSelected.name) 
        dialog = gtk.MessageDialog(self, gtk.DIALOG_DESTROY_WITH_PARENT, 
                                   gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,
                                   message)
        response = dialog.run()
        dialog.destroy()
        
        if gtk.RESPONSE_YES == response:
             self.on_save_host(None)
             self.__asterisco(self.hostPathSelected, False)
             
             self.hostPathSelected = self.listHost.get_cursor()[0][0]
             iter = self.listStoreHost.get_iter(self.hostPathSelected)
             self.hostSelected = self.hosts.get(self.listStoreHost.get_value(iter, 0))
            
             self.__popula_fields()
             self.hostSelectedChange(False)
             
        elif gtk.RESPONSE_NO == response:
            self.hostSelectedChange = False
            self.listHost.set_cursor(self.hostPathSelected)
            self.hostSelectedChange = True
        
        
    def __asterisco(self, pos, add):
        iter = self.listStoreHost.get_iter(pos)
        value = self.listStoreHost.get_value(iter, 0) 
            
        if add == True:
            value += " *" 
        else:
            value = re.sub("\*$", "", value)
        self.listStoreHost.set_value(iter, 0, value)
        
        
    def on_open_host(self, widget):
        self.hide_all()
        Explorer(self.hostSelected)
        
        

class Explorer(gtk.Window):
    
    def __init__(self, host):
        super(Explorer, self).__init__()
        
        self._host = host
        
        self.set_title("Teste")
        
        self.maximize()
        self.connect("destroy", gtk.main_quit)
        
        self.add(self.__vbox())
        self.show()
        
    def __vbox(self):
        vbox = gtk.VBox(False)
        vbox.pack_start(self.__menu(), False, False, 0)
        #hbox.pack_start(self.__bar_tools(), False, False, 0)
        
        vbox.pack_start(self.__select_explorer())
        vbox.pack_start(self.__status(), False, False, 0)
        
        vbox.show()
        return vbox
    
    def __menu(self):
        menu_items = [
            ( "/_File", None, None, 0, "<Branch>" ),
            ( "/File/_Session Manager", "<control>S", None, 0, None ),
            ( "/File/sep1", None, None, 0, "<Separator>" ),
            ( "/File/E_xit", "<control>Q" , gtk.main_quit, 0, None ),
            ( "/_Help", None, None, 0, "<Branch>" ),
            ( "/Help/About", None, self.on_about, 0, None )
            ]
        
        
        accel_group = gtk.AccelGroup()
        item_factory = gtk.ItemFactory(gtk.MenuBar, "<main>", accel_group)
        item_factory.set_data("view", self)
        item_factory.create_items(menu_items)
        
        self.add_accel_group(accel_group)
        
        wid = item_factory.get_widget("<main>")
        wid.show_all()
        return wid
        
    def __bar_tools(self):
         pass
    
    def __select_explorer(self):
        vpaned = gtk.VPaned()
        

        hpaned = gtk.HPaned()
        hpaned.set_position(300)
        vpaned.pack1(hpaned, True)
        
        hpaned.pack1(loadmodule.instance_TreeDbs(self._host))
        hpaned.pack2(self.__manager_db())
        
        vpaned.pack2(self.__log(), False)

        hpaned.show()
        vpaned.show()
        
        return vpaned
    
    def __manager_db(self):
        type = self._host.type.get_type()
        
        manager = loadmodule.instance_manager(self._host)

        container = manager.main_container()
        container.show()
        return container
        
    
    def __log(self):
        buffer = gtk.TextBuffer()
        
        iter = buffer.get_iter_at_offset(0)
        buffer.insert(iter, "sadfs")
        textView = gtk.TextView(buffer)
        textView.set_size_request(-1, 120)
        
        textView.show_all()
        return textView
    
    def __status(self):
        statusBar = gtk.Statusbar()
        statusBar.show_all()
        return statusBar 
    
    def on_about(self, widget):
        pass



class ScrolledWindow(gtk.ScrolledWindow):
    
    def __init__(self):
      super(ScrolledWindow, self).__init__()
      self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
      self.set_shadow_type(gtk.SHADOW_IN)
      #self.add(widget)
