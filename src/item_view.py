# Copyright (C) Miłosz Pigłas <milosz@archeocs.com>
#
# Licensed under the European Union Public Licence

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from object_dict import ObjectDict as od
from input_tab2 import *
from lang import tr

SRC_ATTRS = ['chronology_maybe', 'chronology', 'chronology_rel', 'chronology2',
             'culture_maybe', 'culture', 'culture_rel', 'culture2',
             'cls_author', 'cls_pottery', 'cls_glass', 'cls_bones',
             'cls_metal', 'cls_flint', 'cls_clay', 'cls_other', 'cls_remarks',
             'id']

class AttrEditor:

    def __init__(self, label, widget,
                 setHandler=lambda e, v: e.setText(str(v)),
                 getHandler=lambda e: e.text()):
        self.widget = widget
        self.geth = getHandler
        self.seth = setHandler
        self.label = label

    def value(self):
        return self.geth(self.widget)

    def setValue(self, v):
        self.seth(self.widget, v)

    def clear(self):
        self.seth(self.widget, '')

class ItemEditorWidget(QWidget):

    def __init__(self,
                 log,
                 allowedChrono=[],
                 allowedCulture = [],
                 parent=None):
        QWidget.__init__(self, parent)
        lay = QVBoxLayout()
        self.setLayout(lay)
        btn = QPushButton(tr('open_editor'))
        lay.addWidget(btn)
        btn.clicked.connect(self.openEditor)
        self.items = []
        self.log = log
        self.allowedChrono = allowedChrono
        self.allowedCulture = allowedCulture

    def openEditor(self):
        self.log.info('Open editor {}', self.items)
        rows = list(map(self.itToRow, self.items))
        columns = [
            Column({'':None, '?':'?'}, label=tr('maybe'), log=self.log)
            ,Column(self.allowedChrono, label=tr('chronology'), log=self.log)
            ,Column({'R':'-', 'B':'/'}, label=tr('relation'), log=self.log)
            ,Column(self.allowedChrono, label=tr('chronology'), log=self.log)
            ,Column({'':None, '?':'?'}, label=tr('maybe'), log=self.log)
            ,Column(self.allowedCulture, label=tr('culture'), log=self.log)
            ,Column({'R':'-', 'B':'/'}, label=tr('relation'), log=self.log)
            ,Column(self.allowedCulture, label=tr('culture'), log=self.log)
            ,Column(label=tr('author'))
            ,Column(label=tr('pottery'))
            ,Column(label=tr('glass'))
            ,Column(label=tr('bones'))
            ,Column(label=tr('metal'))
            ,Column(label=tr('flint'))
            ,Column(label=tr('clay'))
            ,Column(label=tr('other'))
            ,Column(label=tr('cls_remarks'))
            ,Column(hidden=True, empty=None)
        ]

        itd = InputTabDialog(columns, rows, self, self.log)
        v = itd.exec_()
        self.log.info('Editor: {}', v)
        if v == 1:
            self.items = list(map(self.rowToIt, itd.getRows()))
            self.log.info('Editor input items {}', self.items)
        self.log.info('Editor OK')

    def itToRow(self, it):
        """
        Converts record from AS_SOURCES to row, that is displayed in
        classification editor
        """
        return [it.get(s) for s in SRC_ATTRS]

    def rowToIt(self, row):
        """
        Converts row from editor to AS_SOURCES record
        """
        return dict([(s, row[si])
                     for (si, s) in enumerate(SRC_ATTRS)])

    def setItems(self, items):
        self.log.info('Set source items {}, {}', items, type(items))
        self.items = items

    def getItems(self):
        self.log.info('Classifiaction {}', self.items)
        return self.items


def textEditor(label):
    return AttrEditor(label, QLineEdit())

def itemEditor(label, log, chrono=[], culture=[]):
    return AttrEditor(label,
                      ItemEditorWidget(log, chrono, culture),
                      setHandler=lambda e, v: e.setItems(v),
                      getHandler=lambda e: e.getItems())

class ItemFormWidget(QWidget):
    def __init__(self, log, parent=None):
        QWidget.__init__(self, parent)
        self.input = od({})
        self.lay = QFormLayout(parent)
        self.log = log

    def addText(self, name, label):
        ed = textEditor(label)
        self.input[name] = ed
        self.lay.addRow(ed.label, ed.widget)

    def addItemEditor(self, name, label, chrono=[], culture=[]):
        ed = itemEditor(label, self.log, chrono, culture)
        self.input[name] = ed
        self.lay.addRow(ed.label, ed.widget)

    def setItem(self, item=None):
        self.log.info('Set item {}', item)
        for ed in self.input.values():
            ed.clear()
        if not item:
            return
        for (edName, ed) in self.input.items():
            v = item.value(edName)
            if v is not None:
                self.log.info('Set item attr {}: {}', edName, v)
                ed.setValue(v)

    def mergeItem(self, item):
        for (edName, ed) in self.input.items():
            v = ed.value()
            if v:
                self.log.info('Merge {}:{}', edName,  v)
                item.setValue(edName, ed.value())
        return item
