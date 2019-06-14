from PySide2.QtCore import QObject

from hexrd.xrd import spacegroup
from hexrd.xrd.material import Material

from hexrd.ui.ui_loader import UiLoader

class AddMaterialDialog(QObject):

    def __init__(self, parent=None):
        super(AddMaterialDialog, self).__init__(parent)

        loader = UiLoader()
        self.ui = loader.load_file('add_material_dialog.ui', parent)

        self.material = Material()

        self.setup_space_group_widgets()

        self.setup_connections()

        # Start with space group 255
        self.ui.space_group.setCurrentIndex(522)

    def setup_connections(self):
        for widget in self.lattice_widgets:
            widget.valueChanged.connect(self.set_lattice_params)

        for widget in self.space_group_setters:
            widget.currentIndexChanged.connect(self.set_space_group)
            widget.currentIndexChanged.connect(self.enable_lattice_params)

    def setup_space_group_widgets(self):
        for k in spacegroup.sgid_to_hall:
            self.ui.space_group.addItem(k)
            self.ui.hall_symbol.addItem(spacegroup.sgid_to_hall[k])
            self.ui.hermann_mauguin.addItem(spacegroup.sgid_to_hm[k])

    @property
    def lattice_widgets(self):
        return [
            self.ui.lattice_a,
            self.ui.lattice_b,
            self.ui.lattice_c,
            self.ui.lattice_alpha,
            self.ui.lattice_beta,
            self.ui.lattice_gamma
        ]

    @property
    def space_group_setters(self):
        return [
            self.ui.space_group,
            self.ui.hall_symbol,
            self.ui.hermann_mauguin
        ]

    def block_lattice_signals(self, block=True):
        for widget in self.lattice_widgets:
            widget.blockSignals(block)

    def block_sgs_signals(self, block=True):
        for widget in self.space_group_setters:
            widget.blockSignals(block)

    def set_space_group(self, val):
        try:
            self.block_sgs_signals(True)
            self.ui.space_group.setCurrentIndex(val)
            self.ui.hall_symbol.setCurrentIndex(val)
            self.ui.hermann_mauguin.setCurrentIndex(val)
            sgid = int(self.ui.space_group.currentText().split(':')[0])
            for sgids, lg in spacegroup._pgDict.items():
                if sgid in sgids:
                    self.ui.laue_group.setText(lg[0])
                    break
            self.ui.lattice_type.setText(spacegroup._ltDict[lg[1]])
        finally:
            self.block_sgs_signals(False)

    def enable_lattice_params(self):
        """enable independent lattice parameters"""
        # lattice parameters are stored in the old "ValUnit" class
        self.block_lattice_signals(True)
        try:
            m = self.material
            sgid = int(self.ui.space_group.currentText().split(':')[0])
            self.material.sgnum = sgid
            reqp = m.spaceGroup.reqParams
            lprm = m.latticeParameters
            for i, widget in enumerate(self.lattice_widgets):
                widget.setEnabled(i in reqp)
                u = 'angstrom' if i < 3 else 'degrees'
                widget.setValue(lprm[i].getVal(u))
        finally:
            self.block_lattice_signals(False)

    def set_lattice_params(self):
        """update all the lattice parameter boxes when one changes"""
        # note: material takes reduced set of lattice parameters but outputs
        #       all six
        self.block_lattice_signals(True)
        try:
            m = self.material
            reqp = m.spaceGroup.reqParams
            nreq = len(reqp)
            lp_red = nreq*[0.0]
            for i in range(nreq):
                boxi = self.lpboxes[reqp[i]]
                lp_red[i] = boxi.value()
            m.latticeParameters = lp_red
            lprm = m.latticeParameters
            for i, widget in enumerate(self.lattice_widgets):
                u = 'angstrom' if i < 3 else 'degrees'
                widget.setValue(lprm[i].getVal(u))
        finally:
            self.block_lattice_signals(False)

    def set_name(self, name):
        self.material.name = self.material_name.text()

    def show(self):
        self.ui.show()