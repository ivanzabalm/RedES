__author__ = 'Alvaro_Jimenez_&_Ivan_Zabaleta'

from pymongo import MongoClient
import json

def getCityGeoJSON(address):
    """ Devuelve las coordenadas de una direcciion a partir de un str de la direccion
    Cuidado, la API tiene un limite de peticiones.
    Argumentos:
        address (str) -- Direccion
    Return:
        (str) -- GeoJSON
    """
    from geopy.geocoders import Nominatim
    geolocator = Nominatim()
    location = geolocator.geocode(address)
    #TODO
    # Devolver GeoJSON de tipo punto con la latitud y longitud almacenadas
    # en las variables location.latitude y location.longitude

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
        pass #No olvidar eliminar esta li__dictnea una vez implementado
    
    def next(self):
        """ Devuelve el siguiente documento en forma de modelo
        """
        #TODO
        pass #No olvidar eliminar esta linea una vez implementado

    @property
    def alive(self):
        """True si existen más modelos por devolver, False en caso contrario
        """
        #TODO
        pass #No olvidar eliminar esta linea una vez implementado

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
    __dict = {"nombre": {"nombre": "Adrián", "apellido": "Valiente"}, "telefonos": [639861561, 691078391],"ciudad": "Huelva", "estudios": [{"universidad": "USAL", "inicio": "19/04/2012", "final": "24/03/2005"},{"universidad": "USAL", "inicio": "13/09/2011", "final": "17/03/2002"}],"trabajo": [{"empresa": "UPM", "inicio": "28/09/2018", "final": "21/07/2005"},{"empresa": "UPM", "inicio": "12/05/2005", "final": "08/05/2007"}]}

    def __init__(self, **kwargs):
        self.__dict.update(kwargs)
        
    def save(self):
        if(db.find_one(self.__dict)):
            print("Existe")
            db.update(self.__dict)
        else:
            print("No existe")
            db.insert_one(self.__dict)

        for x in db.find():
            print(x)

    def borradoTmp(self):
        "Funcion temporal, no es necesaria"
        self.db.delete_many({})

    def change(self, **kwargs):
        """
        with open('redES.json') as file:
            __dict = json.load(file)
        db.insert_many(__dict)
        """

        pass #No olvidar eliminar esta linea una vez implementado
    
    @classmethod
    def find(cls, query):
        """ Devuelve un cursor de modelos        
        """ 

        pass #No olvidar eliminar esta linea una vez implementado

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

if __name__ == '__main__':
    client = MongoClient()
    db = client.test.personas
    persona = Persona()
    persona.init_class(db)
    persona.save()