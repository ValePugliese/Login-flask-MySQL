import pymysql
from flask import Flask
from werkzeug.security import check_password_hash, generate_password_hash

from .entities.User import User


class Database:
    """Clase para gestionar la conexión a la base de datos"""
    
    @staticmethod
    def get_db_connection():
        """Obtiene una conexión a la base de datos MySQL"""
        try:
            return pymysql.connect(
                host='localhost',
                user='root',
                password='',
                database='flask_login',
                cursorclass=pymysql.cursors.DictCursor
            )
        except pymysql.MySQLError as e:
            raise Exception(f"Error al conectar a la base de datos: {e}")
        

class ModelUser:
    """Clase para manejar la lógica de negocio del modelo User"""
    
    @classmethod
    def login(cls, user):
        """Método para hacer login de un usuario"""
        connection = None
        try:
            connection = Database.get_db_connection()
            with connection.cursor() as cursor:
                sql = """SELECT id, username, password, fullname FROM user 
                         WHERE username = %s"""
                cursor.execute(sql, (user.username,))
                row = cursor.fetchone()

                if row:
                    stored_password = row['password']  # Usamos acceso por nombre de columna
                    password_correct = User.check_password(stored_password, user.password)

                    if password_correct:
                        # Crear un objeto User, pero sin la contraseña
                        print("correc")
                        return User(row['id'], row['username'], None, row['fullname'])
                    else:
                        return None  # Contraseña incorrecta
                else:
                    return None  # Usuario no encontrado
        except Exception as e:
            raise Exception(f"Error al realizar login: {e}")
        finally:
            if connection:
                connection.close()  # Aseguramos que la conexión se cierre siempre

    @classmethod
    def get_by_id(cls, id):
        """Método para obtener un usuario por ID"""
        connection = None
        try:
            connection = Database.get_db_connection()
            with connection.cursor() as cursor:
                sql = "SELECT id, username, fullname FROM user WHERE id = %s"
                cursor.execute(sql, (id,))
                row = cursor.fetchone()

                if row:
                    return User(row['id'], row['username'], None, row['fullname'])  # No incluimos la contraseña
                else:
                    return None  # No se encontró el usuario
        except Exception as e:
            raise Exception(f"Error inesperado al obtener el usuario por ID: {e}")
        finally:
            if connection:
                connection.close()  # Aseguramos que la conexión se cierre siempre


class User:
    """Modelo de usuario"""

    def __init__(self, id, username, password, fullname, is_active=True):
        self.id = id
        self.username = username
        self._password = password  # Usamos _password para almacenar la contraseña de manera segura
        self.fullname = fullname
        self.is_active = is_active

    @property
    def password(self):
        """No exponer la contraseña directamente"""
        return self._password

    @password.setter
    def password(self, value):
        """Establecer la contraseña (por ejemplo, hash de la contraseña)"""
        self._password = generate_password_hash(value)  # Guardamos la contraseña como hash

    @staticmethod
    def check_password(stored_password, provided_password):
        """Método para verificar la contraseña (deberías usar hashing en producción)"""
        print(stored_password, provided_password)
        print(check_password_hash)
        print(check_password_hash(stored_password, provided_password))
        return check_password_hash(stored_password, provided_password)
    
    def get_id(self):
        """Método que Flask-Login utiliza para obtener el ID del usuario."""
        return str(self.id)
    
    @property
    def is_authenticated(self):
        """Indica si el usuario está autenticado"""
        return True
