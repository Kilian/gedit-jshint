from gettext import gettext as _

import gtk
import gedit
import os
import simplejson
import urllib


jshint_settings = "/* curly: true, eqeqeq: true, forin: true, undef: true,*/\n"
jshint_globals = "/* */\n"

ui_str = """<ui>
  <menubar name="MenuBar">
    <menu name="ToolsMenu" action="Tools">
      <placeholder name="ToolsOps_2">
        <menuitem name="JSHint" action="JSHint"/>
      </placeholder>
    </menu>
  </menubar>
</ui>
"""

class JSHintWindowHelper:
    def __init__(self, plugin, window):
        self._window = window
        self._plugin = plugin
        self.tab = None
        self.pane = None

        # Insert menu items
        self._insert_menu()

    def deactivate(self):
        # Remove any installed menu items
        self._remove_menu()

        self._window = None
        self._plugin = None
        self._action_group = None

    def _insert_menu(self):
        # Get the GtkUIManager
        manager = self._window.get_ui_manager()

        # Create a new action group
        self._action_group = gtk.ActionGroup("JSHintPluginActions")
        self._action_group.add_actions([("JSHint", None, _("JSHint Check"),
                                         "<Shift><Ctrl>J", _("JSHint Check"),
                                         self.on_jshint_activate)])

        # Insert the action group
        manager.insert_action_group(self._action_group, -1)

        # Merge the UI
        self._ui_id = manager.add_ui_from_string(ui_str)

    def _remove_menu(self):
        # Get the GtkUIManager
        manager = self._window.get_ui_manager()

        # Remove the ui
        manager.remove_ui(self._ui_id)

        # Remove the action group
        manager.remove_action_group(self._action_group)

        # Make sure the manager updates
        manager.ensure_update()

    def update_ui(self):
        self._action_group.set_sensitive(self._window.get_active_document() != None)
        if self.pane:
            if self.tab != self._window.get_active_tab():
                self.lines = []
                self.errorlines.clear()
                self._window.get_bottom_panel().remove_item(self.pane)
                self.pane = None


    def row_clicked(self, treeview, path, view_column, doc):
        lineno, charno = self.lines[path[0]]
        view = self._window.get_active_view()
        bf = view.get_buffer()
        try:
            lineiter = bf.get_iter_at_line_offset(lineno-3, 0 + charno)
        except:
            lineiter = view.get_line_at_y(lineno)
        bf.place_cursor(lineiter)
        view.scroll_to_iter(lineiter, within_margin=0.25)
        view.grab_focus()

    # Menu activate handlers
    def on_jshint_activate(self, action):
        doc = self._window.get_active_document()
        self.tab = self._window.get_active_tab()
        if not doc:
            return

        rhinojs_path = os.path.join(os.path.split(__file__)[0], "rhino.js")
        tmpfile_path = os.path.join(os.path.split(__file__)[0], "jshint.tmp")
        jsondata = doc.get_text(doc.get_iter_at_line(0), doc.get_end_iter())

        tmpfile = open(tmpfile_path,"w")
        tmpfile.writelines(jshint_settings)
        tmpfile.writelines(jshint_globals)
        tmpfile.writelines(jsondata)
        tmpfile.close()

        command = 'js -f ' + rhinojs_path + ' jshint.js ' + tmpfile_path
        fin,fout = os.popen4(command)
        result = fout.read()
        if result:
          jshint_results = simplejson.loads(result)
        else:
          jshint_results = simplejson.loads('{"errors": [{"reason": "Not a single error, awesome!", "line": 2, "character": 0}]}')

        if not self.pane:
            self.errorlines = gtk.ListStore(int,int,str)
            self.pane = gtk.ScrolledWindow()
            treeview = gtk.TreeView(model=self.errorlines)
            lineno = gtk.TreeViewColumn('Line')
            charno = gtk.TreeViewColumn('Char')
            message = gtk.TreeViewColumn('Message')
            treeview.append_column(lineno)
            treeview.append_column(charno)
            treeview.append_column(message)
            cell1 = gtk.CellRendererText()
            cell2 = gtk.CellRendererText()
            cell3 = gtk.CellRendererText()
            lineno.pack_start(cell1,True)
            charno.pack_start(cell2, True)
            message.pack_start(cell3, True)
            lineno.set_attributes(cell1, text=0)
            charno.set_attributes(cell2, text=1)
            message.set_attributes(cell3, text=2)
            bottom = self._window.get_bottom_panel()
            image = gtk.Image()
            image.set_from_icon_name('stock_mark', gtk.ICON_SIZE_MENU)
            self.pane.add(treeview)
            bottom.add_item(self.pane, 'JSHint', image)
            treeview.connect("row-activated", self.row_clicked, doc)
            self.pane.show_all()

        self.errorlines.clear()
        self.lines = []
        for e in jshint_results['errors']:
            self.errorlines.append([e['line']-2, e['character'], urllib.unquote(e['reason'])])
            self.lines.append([int(e['line']), int(e['character'])])

        self._window.get_bottom_panel().set_property("visible", True)


class JSHintPlugin(gedit.Plugin):
    def __init__(self):
        gedit.Plugin.__init__(self)
        self._instances = {}

    def activate(self, window):
        self._instances[window] = JSHintWindowHelper(self, window)

    def deactivate(self, window):
        self._instances[window].deactivate()
        del self._instances[window]

    def update_ui(self, window):
        self._instances[window].update_ui()
    # configuration
    def is_configurable(self):
        return True

    def create_configure_dialog(self):
        dialog = gtk.Dialog("JSHint configuration")
        # ...code to add widgets to your dialog and connect signal handlers
        return dialog

