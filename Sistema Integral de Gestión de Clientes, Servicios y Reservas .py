import re

from exceptions import (
    ClienteError,
    CorreoInvalidoError,
    TelefonoInvalidoError,
    ParametroInvalidoError
)


class Cliente:

    def __init__(self, id_cliente, nombre, correo, telefono):
        self.__id_cliente = None
        self.__nombre = None
        self.__correo = None
        self.__telefono = None

        self.set_id_cliente(id_cliente)
        self.set_nombre(nombre)
        self.set_correo(correo)
        self.set_telefono(telefono)

    # GETTERS

    def get_id_cliente(self):
        return self.__id_cliente

    def get_nombre(self):
        return self.__nombre

    def get_correo(self):
        return self.__correo

    def get_telefono(self):
        return self.__telefono

    # SETTERS

    def set_id_cliente(self, id_cliente):
        if id_cliente is None:
            raise ParametroInvalidoError(
                "El ID del cliente es obligatorio."
            )

        if not str(id_cliente).isdigit():
            raise ParametroInvalidoError(
                "El ID del cliente debe ser numérico."
            )

        self.__id_cliente = int(id_cliente)

    def set_nombre(self, nombre):
        if not nombre or nombre.strip() == "":
            raise ClienteError(
                "El nombre del cliente no puede estar vacío."
            )

        self.__nombre = nombre.strip()

    def set_correo(self, correo):
        if not correo or correo.strip() == "":
            raise CorreoInvalidoError(
                "El correo es obligatorio."
            )

        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if not re.match(patron, correo):
            raise CorreoInvalidoError(
                "Formato de correo inválido."
            )

        self.__correo = correo

    def set_telefono(self, telefono):
        if not telefono or str(telefono).strip() == "":
            raise TelefonoInvalidoError(
                "El teléfono es obligatorio."
            )

        if not str(telefono).isdigit():
            raise TelefonoInvalidoError(
                "El teléfono solo puede contener números."
            )

        self.__telefono = str(telefono)

    def __str__(self):
        return (
            f"Cliente(ID: {self.__id_cliente}, "
            f"Nombre: {self.__nombre}, "
            f"Correo: {self.__correo}, "
            f"Teléfono: {self.__telefono})"
        )
class ClienteError(Exception):
    """
    Excepción base para errores relacionados con clientes.
    """
    pass


class CorreoInvalidoError(ClienteError):
    """
    Se genera cuando el correo no tiene un formato válido.
    """
    pass


class TelefonoInvalidoError(ClienteError):
    """
    Se genera cuando el teléfono contiene caracteres no numéricos.
    """
    pass


class ServicioError(Exception):
    """
    Excepción base para errores relacionados con servicios.
    """
    pass


class ReservaError(Exception):
    """
    Excepción base para errores relacionados con reservas.
    """
    pass


class ParametroInvalidoError(Exception):
    """
    Se genera cuando un parámetro obligatorio es inválido o está vacío.
    """
    pass
