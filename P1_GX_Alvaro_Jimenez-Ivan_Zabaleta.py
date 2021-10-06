__author__ = 'Alvaro_Jimenez_&_Ivan_Zabaleta'

from pymongo import MongoClient
from pymongo.command_cursor import CommandCursor
from geojson import Point

def getCityGeoJSON(address):
    """ Devuelve las coordenadas de una direcciion a partir de un str de la direccion
    Cuidado, la API tiene un limite de peticiones.
    Argumentos:
        address (str) -- Direccion
    Return:
        (str) -- GeoJSON
    """
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent="RedES")
    location = geolocator.geocode(address)
    
    # Devolver GeoJSON de tipo punto con la latitud y longitud almacenadas
    # en las variables location.latitude y location.longitude
    return Point((location.latitude, location.longitude))

class ModelCursor:
    """ Cursor para iterar sobre los documentos del resultado de una
    consulta. Los documentos deben ser devueltos en forma de objetos
    modelo.
    """                             

    def __init__(self, model_class, command_cursor):
        """ Inicializa ModelCursor
        Argumentos:
            model_class (class) -- Clase para crear los modelos del 
            documento que se itera.
            command_cursor (CommandCursor) -- Cursor de pymongo
        """
        #TODO


        pass 
    
    def next(self):
        """ Devuelve el siguiente documento en forma de modelo
        """
        # TODO
        # command_cursor.next()
        
        pass 

    @property
    def alive(self):
        """True si existen más modelos por devolver, False en caso contrario
        """
        #TODO
        # command_cursor.alive()

        pass 

class Persona:
    """ Prototipo de la clase modelo
        Copiar y pegar tantas veces como modelos se deseen crear (cambiando
        el nombre Model, por la entidad correspondiente), o bien crear tantas
        clases como modelos se deseen que hereden de esta clase. Este segundo 
        metodo puede resultar mas compleja
    """
    required_vars = []
    admissible_vars = []

    db = None
    __dict = {}

    def __init__(self, **kwargs):
        self.__dict.update(kwargs)
        
    def save(self):
        
        pass

    def borradoTmp(self):
        "Funcion temporal, no es necesaria"
        self.db.delete_many({})

    def change(self, **kwargs):

        pass 
    
    @classmethod
    def find(cls, query):
        """ Devuelve un cursor de modelos        
        """ 
        
        pass

    @classmethod
    def init_class(cls, db, vars_path="persona.vars"):
        """ Inicializa las variables de clase en la inicializacion del sistema.
        Argumentos:
            db (MongoClient) -- Conexion a la base de datos.
            vars_path (str) -- ruta al archivo con la definicion de variables
            del modelo.
        """
        cls.db = db

# Q1: Listado de todas las compras de un cliente
nombre = "Definir"
Q1 = []

# Q2: etc...

"""
    Test main - getCityGeoJSON(address) 
    -------------------------------------
    geoJson = getCityGeoJSON("175 5th Avenue NYC")
    print(geoJson)
"""

if __name__ == '__main__':
    client = MongoClient()
    db = client.test.personas
    persona = Persona()
    persona.init_class(db)
    
    