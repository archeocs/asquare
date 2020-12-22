from sys import argv

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Cell:

    def __init__(self, display, key=None):
        self.displayText = display
        self.editText = key

    def __str__(self):
        return 'd={}, k={}'.format(self.displayText, self.editText)


class Column:

    def __init__(self, allowedValues=None):
        self.allowed = allowedValues
        self.combo = allowedValues is not None

    def modelItem(self, val):
        if self.combo and val in self.allowed:
            return newItem(Cell(self.allowed[val], val))
        else:
            return newItem(Cell(val))

    def getValue(self, item):
        if self.combo:
            return item.data(role=Qt.EditRole)
        else:
            return item.data(role=Qt.DisplayRole)

class InputTabWidget(QWidget):

    def __init__(self, modelDef, rows, parent=None):
        QWidget.__init__(self, parent)
        lay = QVBoxLayout()
        self.setLayout(lay)

        self.tab = self.initView(modelDef)
        self.model = self.initModel(modelDef, rows)
        self.tab.setModel(self.model)

        for (ci, c) in enumerate(modelDef):
            if c.combo:
                print(ci, c.allowed)
                self.tab.setItemDelegateForColumn(ci, mapComboBoxDelegate(c.allowed, self.tab))
        lay.addWidget(self.tab)
        lay.addWidget(self.createButtons())

    def initView(self, modelDef):
        tab = QTableView(self)
        modelDef = modelDef
        return tab

    def initModel(self, modelDef, rows):
        model = QStandardItemModel(0, len(modelDef))
        for (ri, r) in enumerate(rows):
            md = modelDef[ri]
            mrow = list(map(md.modelItem, r))
            print(mrow)
            model.appendRow(mrow)
        return model

    def addRowAction(self):
        self.model.appendRow([newItem(Cell('', '?')), newItem(Cell(''))])

    def delRowAction(self):
        selModel = self.tab.selectionModel()
        if selModel.hasSelection():
            idx = selModel.currentIndex()
            self.model.removeRow(idx.row())

    def createButtons(self):
        buttons = QGroupBox(self)
        lay = QHBoxLayout()
        buttons.setLayout(lay)

        addBtn = QPushButton('+')
        addBtn.clicked.connect(self.addRowAction)

        delBtn = QPushButton('-')
        delBtn.clicked.connect(self.delRowAction)

        okBtn = QPushButton('OK')
        cancelBtn = QPushButton('Cancel')

        lay.addWidget(addBtn)
        lay.addWidget(delBtn)
        lay.addWidget(okBtn)
        lay.addWidget(cancelBtn)

        return buttons


class InputTabWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        columns = [
            Column({'a': 'A', 'b': 'B', '?': ''})
            ,Column()
            ,Column()
            ,Column({'x': 'X', 'y': 'YYYYYY', '?': ''})
        ]
        rows = [
            ['a', '1111', '5555', '?']
        ]
        self.setCentralWidget(InputTabWidget(columns, rows, self))

def newItem(value):
    print(value)
    if value.editText:
        sit = TypedItem()
        sit.setData(value.editText, role=Qt.EditRole)
    else:
        sit = QStandardItem()
    sit.setEditable(True)
    sit.setData(value.displayText, role=Qt.DisplayRole)
    return sit

def mapComboBoxDelegate(options, parent):
    delegate = MapComboBoxDelegate(options, parent) 
    return delegate

class MapComboBoxDelegate(QStyledItemDelegate):

    def __init__(self, options, parent=None):
        QStyledItemDelegate.__init__(self, parent)
        self.options = options

    def createEditor(self, parent, opts, index):
        cb = MapComboBox(parent)
        for (k, v) in self.options.items():
            cb.addItem(v, userData=k)
        return cb

    def setEditorData(self, ed, index):
        v = index.data(Qt.EditRole)
        ed.setKey(v)

    def setModelData(self, ed, model, index):
        v = ed.key()
        model.setData(index, v, role=Qt.EditRole)
        model.setData(index, ed.itemData(ed.currentIndex(), Qt.DisplayRole), role=Qt.DisplayRole)

class MapComboBox(QComboBox):

    def __init__(self, parent=None):
        QComboBox.__init__(self, parent)

    def setKey(self, k):
        self.setCurrentIndex(self.findData(k))

    def key(self):
        return self.itemData(self.currentIndex())

class TypedItem(QStandardItem):

    def __init__(self):
        QStandardItem.__init__(self)
        self.variants = {}

    def setData(self, v, role=Qt.UserRole + 1):
        self.variants[role] = v
        self.emitDataChanged()

    def data(self, role=Qt.UserRole + 1):
        v = self.variants.get(role, QVariant())
        return v

def main():
    app = QApplication(argv)
    win = InputTabWindow()
    win.show()
    app.exec_()

if __name__ == '__main__':
    main()
