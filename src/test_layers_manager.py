import unittest

from qgis.core import *
from layers_manager import LayersManager
from main import StdOutLogAdapter

class QgsProj:

    def __init__(self, layers):
        self.layers = layers
        self._handlers = {}
        self.layerAdded = self

    def connect(self, fun):
        self._handlers['layers_added'] = fun
    
    def mapLayers(self):
        return self.layers

    def testAddLayer(self, name, lay):
        self.layers[name] = lay
        self._handlers['layers_added']([lay])

class DataProvider:

    def __init__(self, db):
        self._db = db

    def database(self):
        return self._db

    def uri(self):
        return QgsDataSourceUri(self._db)

RECORDS_URI = 'dbname=\'test.sqlite\' table="AS_RECORDS" sql='
    
class Layer:

    def __init__(self, valid=True, type=QgsMapLayer.VectorLayer, name='AS_records', db=RECORDS_URI):
        self._valid = valid
        self._type = type
        self._name = name
        self._dataProvider = DataProvider(db)
        self.selectionChanged = self
        self.handlers = {}

    def getFeature(self, args):
        return args
        
    def connect(self, fun):
        self.handlers['selection_changed'] = fun
        
    def isValid(self):
        return self._valid

    def type(self):
        return self._type

    def name(self):
        return self._name

    def dataProvider(self):
        return self._dataProvider
    
class LayersManagerTest(unittest.TestCase):

    def test_init_layer_is_loaded(self):
        qgsProj = QgsProj(layers={'as_records': Layer(), 'grid50': Layer(name='grid50')})
        man = LayersManager(qgsProj, StdOutLogAdapter(), lambda x: print(x))
        self.assertEqual(man.managed, {'AS_RECORDS', 'GRID50'})

    def test_init_layer_selection_event_attached(self):
        qgsProj = QgsProj(layers={'as_records': Layer(), 'grid50': Layer(name='grid50')})
        feats = []
        man = LayersManager(qgsProj, StdOutLogAdapter(), lambda x: print(x))
        man.handlers['grid_selected'] = lambda x: feats.append(x)

        qgsProj.layers['grid50'].handlers['selection_changed'](['test_selected_feature'],'b','c')

        self.assertEqual(feats, ['test_selected_feature'])    
        
    def test_init_layer_sources_loaded(self):
        src = []
        def layerFactory(s):
            src.append(s)
            return QgsVectorLayer(s, providerLib='test')
        qgsProj = QgsProj(layers={'as_records': Layer(), 'grid50': Layer(name='grid50')})
        man = LayersManager(qgsProj, StdOutLogAdapter(), layerFactory)

        self.assertTrue(isinstance(man.sources, QgsVectorLayer))
        self.assertEqual(src[1], RECORDS_URI.replace('RECORDS','SOURCES'))

    def test_init_layer_squares_loaded(self):
        src = []
        def layerFactory(s):
            src.append(s)
            return QgsVectorLayer(s, providerLib='test')
        qgsProj = QgsProj(layers={'as_records': Layer(), 'grid50': Layer(name='grid50')})
        man = LayersManager(qgsProj, StdOutLogAdapter(), layerFactory)

        self.assertTrue(isinstance(man.sources, QgsVectorLayer))
        self.assertEqual(src[0], RECORDS_URI.replace('RECORDS','SQUARES'))

    def test_records_added_layer_loaded(self):
        qgsProj = QgsProj(layers={'grid50': Layer(name='grid50')})
        man = LayersManager(qgsProj, StdOutLogAdapter(), lambda x: print(x))

        qgsProj.testAddLayer('as_records', Layer())
        
        self.assertEqual(man.managed, {'AS_RECORDS', 'GRID50'})

    def test_grid_added_layer_loaded(self):
        qgsProj = QgsProj(layers={'as_records': Layer()})
        man = LayersManager(qgsProj, StdOutLogAdapter(), lambda x: print(x))

        qgsProj.testAddLayer('Grid50', Layer(name='Grid50'))
        
        self.assertEqual(man.managed, {'AS_RECORDS', 'GRID50'})

    def test_records_added_layer_sources_loaded(self):
        src = []
        def layerFactory(s):
            src.append(s)
            return QgsVectorLayer(s, providerLib='test')
        qgsProj = QgsProj(layers={'grid50': Layer(name='grid50')})
        man = LayersManager(qgsProj, StdOutLogAdapter(), layerFactory)

        qgsProj.testAddLayer('as_records', Layer())

        self.assertTrue(isinstance(man.sources, QgsVectorLayer))
        self.assertEqual(src[1], RECORDS_URI.replace('RECORDS','SOURCES'))

    def test_records_added_layer_squares_loaded(self):
        src = []
        def layerFactory(s):
            src.append(s)
            return QgsVectorLayer(s, providerLib='test')
        qgsProj = QgsProj(layers={'grid50': Layer(name='grid50')})
        man = LayersManager(qgsProj, StdOutLogAdapter(), layerFactory)

        qgsProj.testAddLayer('as_records', Layer())
        self.assertTrue(isinstance(man.sources, QgsVectorLayer))
        self.assertEqual(src[0], RECORDS_URI.replace('RECORDS','SQUARES'))