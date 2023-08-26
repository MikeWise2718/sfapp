import asyncio
import omni.ext
import omni.kit.ui
import carb

from .window import MyWindow

async def _load_layout(layout_file: str, keep_windows_open=True):
    try:
        from omni.kit.quicklayout import QuickLayout
        # few frames delay to avoid the conflict with the layout of omni.kit.mainwindow
        for i in range(3):
            await omni.kit.app.get_app().next_update_async()
        QuickLayout.load_file(layout_file, keep_windows_open)
        print(f"Loaded layout: {layout_file}")

    except Exception as exc:
        pass

        QuickLayout.load_file(layout_file)



class WindowExtension(omni.ext.IExt):

    MENU_PATH = "Window/MyWindow"

    def on_startup(self, ext_id):

        editor_menu = omni.kit.ui.get_editor_menu()

        # Most application have an Window Menu, See MenuLayout to re-organize it
        self._window = None
        self._menu = editor_menu.add_item(WindowExtension.MENU_PATH, self._on_menu_click, toggle=True, value=True)
        self.show_window(True)

        layout_file = carb.tokens.get_tokens_interface().resolve("${my_name.my_app.setup}/layouts/viewport1.json")
        asyncio.ensure_future(_load_layout(layout_file))

    def _on_menu_click(self, menu, toggled):
        self.show_window(toggled)

    def show_window(self, toggled):
        if toggled:
            if self._window is None:
                self._window = MyWindow()
                self._window.set_visibility_changed_fn(self._visiblity_changed_fn)
            else:
                self._window.show()
        else:
            if self._window is not None:
                self._window.hide()

    def _visiblity_changed_fn(self, visible):
        if self._menu:
            omni.kit.ui.get_editor_menu().set_value(WindowExtension.MENU_PATH, visible)
            self.show_window(visible)

    def on_shutdown(self):
        if self._window is not None:
            self._window.destroy()
            self._window = None
        if self._menu is not None:
            editor_menu = omni.kit.ui.get_editor_menu()
            editor_menu.remove_item(self._menu)
            self._menu = None
