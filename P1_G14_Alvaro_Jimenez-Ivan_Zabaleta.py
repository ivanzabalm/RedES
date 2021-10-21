__author__ = 'Alvaro_Jimenez_&_Ivan_Zabaleta'

import time
from pymongo import MongoClient, GEO2D
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
        self.clase = model_class
        self.cursor = command_cursor
    
    def next(self):
        """ Devuelve el siguiente documento en forma de modelo
        """
        return self.clase(**self.cursor.next())

    @property
    def alive(self):
        """True si existen más modelos por devolver, False en caso contrario
        """
        return self.cursor.alive

class Persona:
    required_vars = []
    admissible_vars = []
    db = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def save(self):
        qr = {"telefono":self.__dict__.get('telefono')} # identificar
        qper = self.db.find(qr,{"_id":0}) # no salga el id

        for persona in qper:
            ins = {} # Se guardan las que se van a actualizar.
            l1 = set(persona.keys())
            l2 = set(self.__dict__.keys())
            resl = list(sorted(l2-l1)) # Busca las que se necesitan actualizar.

            if len(resl) > 0:
                for p in resl:
                    ins[p] = self.__dict__.get(p) # Coge las que necesita actualizar.
            
            for k in persona.keys():
                if self.__dict__.get(k) != persona[k]:
                    ins[k] = self.__dict__.get(k) # Cambia las que necesitan actualizar.
            
            self.db.update_one(qr,{"$set":ins})

        if qper.count() == 0:
            ert = {}
            for we in self.__dict__.keys():
                ert[we] = self.__dict__.get(we)
            self.db.insert_one(ert) # Si no existe introduce uno nuevo.

    def set(self, **kwargs):
        valido = True

        # Comprobacion de variables requeridas.
        for n in self.required_vars:
            if not (kwargs.get(n)):
                valido = False
                print("Error: el documento no contiene las variables requeridas.")

        # Comprobacion de variables admitidas.
        for n in kwargs:
            if not n in self.required_vars:
                if not n in self.admissible_vars:
                    valido = False
                    print("Error: el documento contiene una o varias variables no admitidas.")
                
        # En caso de que las comprobaciones sean exitosas se almacenara en el diccionario de la clase.
        if(valido):
            if not(bool(self.__dict__)):
                self.__dict__.update(kwargs)
            else:
                if(self.__dict__ != kwargs):
                    for n in kwargs:
                        if n in self.__dict__:
                            if(self.__dict__[n] != kwargs[n]):
                                self.__dict__[n] = kwargs[n]
                        else:
                            self.__dict__[n] = kwargs[n]

            # Añadimos el geoJson de tipo punto al documento
            self.__dict__["geolocalizacion"] = getCityGeoJSON(self.__dict__.get("ciudad"))

    @classmethod
    def find(cls, query):
        """ Devuelve un cursor de modelos        
        """ 
        return ModelCursor(cls,cls.db.find(query))

    @classmethod
    def init_class(cls, db, vars_path="persona.vars"):
        """ Inicializa las variables de clase en la inicializacion del sistema.
        Argumentos:
            db (MongoClient) -- Conexion a la base de datos.
            vars_path (str) -- ruta al archivo con la definicion de variables
            del modelo.
        """
        cls.db = db

        with open(vars_path, "r") as f:
            listReqVars = f.readlines(1)
            listAdmVars = f.readlines(1)

        # Para deshacerse de los "\n" y reformar la lista con cada una de las variables ordenadas.
        listReqVars = list(map(str.strip,listReqVars))[0].split(",")
        listAdmVars = list(map(str.strip,listAdmVars))[0].split(",")

        # Aplicando la diferencia de la teoria de conjuntos (B-A) le aplicamos las nuevas variables.
        cls.required_vars.extend(list(set(listReqVars) - set(cls.required_vars)))
        cls.admissible_vars.extend(list(set(listAdmVars) - set(cls.admissible_vars)))

class Empresa:
    required_vars = []
    admissible_vars = []
    db = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def save(self):
        qr = {"ID":self.__dict__.get('ID')} # identificar
        qemp = self.db.find(qr,{"_id":0}) # no salga el id

        for empresa in qemp:
            ins = {} # Se guardan las que se van a actualizar.
            l1 = set(empresa.keys())
            l2 = set(self.__dict__.keys())
            resl = list(sorted(l2-l1)) # Busca las que se necesitan actualizar.

            if len(resl) > 0:
                for p in resl:
                    ins[p] = self.__dict__.get(p) # Coge las que necesita actualizar.
            
            for k in empresa.keys():
                if self.__dict__.get(k) != empresa[k]:
                    ins[k] = self.__dict__.get(k) # Cambia las que necesitan actualizar.
            
            self.db.update_one(qr,{"$set":ins})

        if qemp.count() == 0:
            ert = {}
            for we in self.__dict__.keys():
                ert[we] = self.__dict__.get(we)
            self.db.insert_one(ert) # Si no existe introduce uno nuevo.

    def set(self, **kwargs):
        valido = True

        # Comprobacion de variables requeridas.
        for n in self.required_vars:
            if not (kwargs.get(n)):
                valido = False
                print("Error: el documento no contiene las variables requeridas.")

        # Comprobacion de variables admitidas.
        for n in kwargs:
            if not n in self.required_vars:
                if not n in self.admissible_vars:
                    valido = False
                    print("Error: el documento contiene una o varias variables no admitidas.")
                
        # En caso de que las comprobaciones sean exitosas se almacenara en el diccionario de la clase.
        if(valido):
            if not(bool(self.__dict__)):
                self.__dict__.update(kwargs)
            else:
                if(self.__dict__ != kwargs):
                    for n in kwargs:
                        if n in self.__dict__:
                            if(self.__dict__[n] != kwargs[n]):
                                self.__dict__[n] = kwargs[n]
                        else:
                            self.__dict__[n] = kwargs[n]

    @classmethod
    def find(cls, query):
        """ Devuelve un cursor de modelos        
        """ 
        return ModelCursor(cls,cls.find(query))

    @classmethod
    def init_class(cls, db, vars_path="vars-empresa.txt"):
        """ Inicializa las variables de clase en la inicializacion del sistema.
        Argumentos:
            db (MongoClient) -- Conexion a la base de datos.
            vars_path (str) -- ruta al archivo con la definicion de variables
            del modelo.
        """
        cls.db = db

        with open(vars_path, "r") as f:
            listReqVars = f.readlines(1)
            listAdmVars = f.readlines(1)

        # Para deshacerse de los "\n" y reformar la lista con cada una de las variables ordenadas.
        listReqVars = list(map(str.strip,listReqVars))[0].split(",")
        listAdmVars = list(map(str.strip,listAdmVars))[0].split(",")

        # Aplicando la diferencia de la teoria de conjuntos (B-A) le aplicamos las nuevas variables.
        cls.required_vars.extend(list(set(listReqVars) - set(cls.required_vars)))
        cls.admissible_vars.extend(list(set(listAdmVars) - set(cls.admissible_vars)))



class Centro:
    required_vars = []
    admissible_vars = []
    db = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def save(self):
        qr = {"ID":self.__dict__.get('ID')} # identificar
        qcen = self.db.find(qr,{"_id":0}) # no salga el id

        for centro in qcen:
            ins = {} # Se guardan las que se van a actualizar.
            l1 = set(centro.keys())
            l2 = set(self.__dict__.keys())
            resl = list(sorted(l2-l1)) # Busca las que se necesitan actualizar.

            if len(resl) > 0:
                for p in resl:
                    ins[p] = self.__dict__.get(p) # Coge las que necesita actualizar.
            
            for k in centro.keys():
                if self.__dict__.get(k) != centro[k]:
                    ins[k] = self.__dict__.get(k) # Cambia las que necesitan actualizar.
            
            self.db.update_one(qr,{"$set":ins})

        if qcen.count() == 0:
            ert = {}
            for we in self.__dict__.keys():
                ert[we] = self.__dict__.get(we)
            self.db.insert_one(ert) # Si no existe introduce uno nuevo.

    def set(self, **kwargs):
        valido = True

        # Comprobacion de variables requeridas.
        for n in self.required_vars:
            if not (kwargs.get(n)):
                valido = False
                print("Error: el documento no contiene las variables requeridas.")

        # Comprobacion de variables admitidas.
        for n in kwargs:
            if not n in self.required_vars:
                if not n in self.admissible_vars:
                    valido = False
                    print("Error: el documento contiene una o varias variables no admitidas.")
                
        # En caso de que las comprobaciones sean exitosas se almacenara en el diccionario de la clase.
        if(valido):
            if not(bool(self.__dict__)):
                self.__dict__.update(kwargs)
            else:
                if(self.__dict__ != kwargs):
                    for n in kwargs:
                        if n in self.__dict__:
                            if(self.__dict__[n] != kwargs[n]):
                                self.__dict__[n] = kwargs[n]
                        else:
                            self.__dict__[n] = kwargs[n]

    @classmethod
    def find(cls, query):
        """ Devuelve un cursor de modelos        
        """ 
        return ModelCursor(cls,cls.find(query))

    @classmethod
    def init_class(cls, db, vars_path="vars-centro_educativo.txt"):
        """ Inicializa las variables de clase en la inicializacion del sistema.
        Argumentos:
            db (MongoClient) -- Conexion a la base de datos.
            vars_path (str) -- ruta al archivo con la definicion de variables
            del modelo.
        """
        cls.db = db

        with open(vars_path, "r") as f:
            listReqVars = f.readlines(1)
            listAdmVars = f.readlines(1)

        # Para deshacerse de los "\n" y reformar la lista con cada una de las variables ordenadas.
        listReqVars = list(map(str.strip,listReqVars))[0].split(",")
        listAdmVars = list(map(str.strip,listAdmVars))[0].split(",")

        # Aplicando la diferencia de la teoria de conjuntos (B-A) le aplicamos las nuevas variables.
        cls.required_vars.extend(list(set(listReqVars) - set(cls.required_vars)))
        cls.admissible_vars.extend(list(set(listAdmVars) - set(cls.admissible_vars)))

personasJSON = [
    {"nombre": "Julian","apellido": "Fernandez","telefono" : 674165642,"ciudad" : "Paris","estudios": {"universidad": "UPM", "inicio": "2005-03-24", "final": "2012-04-19", "numEstudios" : 3}, "trabajo": "UPM"},
    {"nombre": "Sergio","apellido": "Diaz","telefono" : 619421988,"ciudad" : "Huelva","estudios": {"universidad": "UAM", "inicio": "2001-05-23", "final": "2005-08-24", "numEstudios" : 4},"trabajo": "UPM"},
    {"nombre": "Javier","apellido": "Cortes","telefono" : 669197778,"ciudad" : "Santander","estudios": {"universidad": "U-tad", "inicio": "2000-08-30", "final": "2010-09-11", "numEstudios" : 1},"trabajo": "UPM"},
    {"nombre": "Carmen","apellido": "Cortes","telefono" : 629755914,"ciudad" : "Huelva","estudios": {"universidad": "UPM", "inicio": "2005-24-03", "final": "2012-04-19"}},
    {"nombre": "Alberto","apellido": "Rayo","telefono" : 685646527,"ciudad" : "Santander","estudios": {"universidad": "UAM", "inicio": "2005-03-24", "final": "2012-04-19"}},
    {"nombre": "Pedro","apellido": "Diéguez","telefono" : 660706957,"ciudad" : "Huelva","estudios": {"universidad": "U-tad", "inicio": "2005-03-24", "final": "2012-19-04", "numEstudios" : 2},"trabajo": "UPM"},
    {"nombre": "Alberto","apellido": "Rayo","telefono" : 609304424,"ciudad" : "Sevilla","estudios": {"universidad": "U-tad", "inicio": "2002-06-02", "final": "2016-06-11"}},
    {"nombre": "José","apellido": "Hernández","telefono" : 693401628,"ciudad" : "Santander","estudios": {"universidad": "UAM", "inicio": "2009-12-08", "final": "2018-07-18", "numEstudios" : 3},"trabajo": "UPM"},
    {"nombre": "Teresa","apellido": "Colmenero","telefono" : 669567032,"ciudad" : "Bilbao","estudios": {"universidad": "UV", "inicio": "2001-03-15", "final": "2017-08-30"}},
    {"nombre": "Luis","apellido": "Izquierdo","telefono" : 691999884,"ciudad" : "Bilbao","estudios": {"universidad": "UAM", "inicio": "2001-03-15", "final": "2017-08-30"}}
]

empresasJSON = [
    {"nombre": "McDonalds","sector" : "Comida","ciudad" : "Madrid","ceo": "Sech"},
    {"nombre": "Nike","sector" : "Ropa","ciudad" : "Barcelona","ceo": "Myke"},
    {"nombre": "Adidas","sector" : "Ropa","ciudad" : "Alicante","ceo": "Ivan"},
    {"nombre": "Apple","sector" : "Tecnologia","ciudad" : "Paris","ceo": "Steve"},
    {"nombre": "Samsung","sector" : "Tecnologia","ciudad" : "Sevilla","ceo": "Xokas"},
    {"nombre": "FIFA","sector" : "Deporte","ciudad" : "Londres","ceo": "Iniesta"},
    {"nombre": "Burger King","sector" : "Comida","ciudad" : "Valencia","ceo": "Gordo"},
    {"nombre": "Riot Games","sector" : "Videojuegos","ciudad" : "Roma","ceo": "Teemo"},
    {"nombre": "JBL","sector" : "Musica","ciudad" : "Amsterdam","ceo": "Stormzy"},
    {"nombre": "BOSE","sector" : "Musica","ciudad" : "Brasil","ceo": "Miguel"}
]

centrosJSON = [
    {"universidad": "U-tad","carrera" : "INSO","ciudad" : "Madrid","alumnos": 15890},
    {"universidad": "CEU","carrera" : "ADE","ciudad" : "Madrid","alumnos": 32341},
    {"universidad": "UA","carrera" : "Derecho","ciudad" : "Alicante","alumnos": 20000},
    {"universidad": "UV","carrera" : "Arquitectura","ciudad" : "Valencia","alumnos": 64483},
    {"universidad": "Complutense","carrera" : "Arte y Diseño","ciudad" : "Madrid","alumnos": 87832},
    {"universidad": "Universidad de Salamanca","carrera" : "Historia","ciudad" : "Salamnca","alumnos": 9500},
    {"universidad": "UAM","carrera" : "Economia","ciudad" : "Madrid","alumnos": 35000},
    {"universidad": "UPF","carrera" : "Bioquimica","ciudad" : "Barcelona","alumnos": 3400},
    {"universidad": "Oxford","carrera" : "Bussines","ciudad" : "Londres","alumnos": 40000},
    {"universidad": "UPM","carrera" : "Relaciones Internacionales","ciudad" : "Madrid","alumnos": 40000}
]

Q1 = []
Q2 = []
Q3 = []
Q4 = []
Q5 = []
Q6 = []
Q7 = []

if __name__ == '__main__':
    client = MongoClient()
    db = client.test

    listaPersonas = [Persona() for i in range(10)]
    i=0

    db.personas.create_index([("geolocalizacion.coordinates", GEO2D)])
    for n in listaPersonas:
        n.init_class(db.personas,"vars-persona.txt")
        n.set(**personasJSON[i])
        n.save()
        time.sleep(0.25)
        i += 1

    listaEmpresas = [Empresa() for i in range(10)]
    i=0
    for n in listaEmpresas:
        n.init_class(db.empresas,"vars-empresa.txt")
        n.set(**empresasJSON[i])
        n.save()
        i += 1

    listaCentros = [Centro() for i in range(10)]
    i=0
    for n in listaCentros:
        n.init_class(db.centros,"vars-centro_educativo.txt")
        n.set(**centrosJSON[i])
        n.save()
        i += 1

    Q1 = listaPersonas[0].find({"ciudad": "Huelva"})
    print("Resultado de la Q1:")
    while Q1.alive:
        print(Q1.next().__dict__)
    print("\n")

    Q2 = listaPersonas[0].find({ "$or" : [{"estudios.universidad" : "UPM"}, {"estudios.universidad" : "UAM"}]})
    print("Resultado de la Q2:")
    while Q2.alive:
        print(Q2.next().__dict__)
    print("\n")

    Q3 = db.personas.distinct("ciudad")
    print("Resultado de la Q3:")
    for x in Q3:
        print(x) 
    print("\n")

    Q4 = listaPersonas[0].find({"geolocalizacion.coordinates" : {"$near" : [ -73.9667, 40.78 ]}})
    print("Resultado de la Q4:")
    while Q4.alive:
        print(Q4.next().__dict__)
    print("\n")

    pipeline = [{"$match" : {"estudios.final" : {"$gte" : "2017-01-01"}}},{"$group": {"_id":"$nombre"}},{"$out": {"db" : "test", "coll": "query5"}}]    
    Q5 = list(db.personas.aggregate(pipeline))
    quer5 = db.query5.find()

    print("Resultado de la Q5:")
    for x in quer5:
        print(x)
    print("\n")
    
    num = db.personas.find({"trabajo" : "UPM"}).count()
    pipeline = [ 
        {"$group": {"_id" : "Null", "Num_Trab" : {"$sum" : "$estudios.numEstudios"}}},
        {"$project": {"_id": 0, "average" : {"$divide": [ "$Num_Trab", num]}}}         
    ]
    Q6 = db.personas.aggregate(pipeline)

    print("Resultado de la Q6:")
    for x in Q6:
        print(x) 
    print("\n")

    pipeline =[ 
        {"$group": {"_id": "$estudios.universidad", "suma": {"$sum":1} }},
        {"$sort": {"suma": -1}},
        {"$limit": 3}]

    Q7 = list(db.personas.aggregate(pipeline))

    print("Resultado de la Q7:")
    for x in Q7:
        print(x)
    print("\n")