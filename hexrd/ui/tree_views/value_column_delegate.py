from PySide2.QtWidgets import (
    QStyledItemDelegate,
    QItemEditorFactory,
    QPushButton
)

from PySide2.QtCore import QEvent

from hexrd.ui.scientificspinbox import ScientificDoubleSpinBox
from hexrd.ui.calibration.panel_buffer_dialog import PanelBufferDialog
from hexrd.ui.tree_views.base_tree_item_model import BaseTreeItemModel
from hexrd.ui import constants
from hexrd.ui.utils import EventBlocker

BUTTON_LABEL = 'Configure Panel Buffer'


class ValueColumnDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

        editor_factory = ValueColumnEditorFactory(parent)
        self.setItemEditorFactory(editor_factory)

    def createEditor(self, parent, option, index):
        model = self.parent().model()
        item = model.get_item(index)
        key = item.data(BaseTreeItemModel.KEY_COL)
        if key == constants.BUFFER_KEY:
            edit_btn = QPushButton(BUTTON_LABEL, parent)

            def _clicked():
                def _set_enable(enabled):
                    # We need to block the event here, otherwise setData(...)
                    # gets called with the buttons boolean value!
                    with EventBlocker(edit_btn, QEvent.FocusOut):
                        edit_btn.setEnabled(enabled)
                # Disable to prevent creating multiple dialogs
                _set_enable(False)

                # Extract out the detector, so we can update the right config
                path = model.get_path_from_root(item, index.column())
                detector = path[path.index('detectors') + 1]
                dialog = PanelBufferDialog(detector, self)
                dialog.show()

                def _enable(_):
                    _set_enable(True)

                # Re-enable the edit button
                dialog.finished.connect(_enable)

            edit_btn.clicked.connect(_clicked)

            return edit_btn
        else:
            return super().createEditor(parent, option, index)


class ValueColumnEditorFactory(QItemEditorFactory):
    def __init__(self, parent=None):
        super().__init__(self, parent)

    def createEditor(self, user_type, parent):
        # Normally in Qt, we'd use QVariant (like QVariant::Double) to compare
        # with the user_type integer. However, QVariant is not available in
        # PySide2, making us use roundabout methods to get the integer like
        # below.
        float_type = (
            ScientificDoubleSpinBox.staticMetaObject.userProperty().userType()
        )
        if user_type == float_type:
            return ScientificDoubleSpinBox(parent)

        return super().createEditor(user_type, parent)
