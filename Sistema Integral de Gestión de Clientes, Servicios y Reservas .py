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


from abc import ABC, abstractmethod


# CLASE ABSTRACTA PRINCIPAL
class Servicio(ABC):

    def __init__(self, id_servicio, nombre, costo_base):
        self.id_servicio = id_servicio
        self.nombre = nombre
        self.costo_base = costo_base

    @abstractmethod
    def calcular_costo(self, cantidad=1, descuento=0, impuesto=0):
        pass

    @abstractmethod
    def describir_servicio(self):
        pass

    @abstractmethod
    def validar_parametros(self):
        pass

    # Método auxiliar para calcular descuentos e impuestos
    def aplicar_descuentos_impuestos(self, subtotal, descuento=0, impuesto=0):
        if not 0 <= descuento <= 100:
            raise ValueError("El descuento debe estar entre 0 y 100.")

        if not 0 <= impuesto <= 100:
            raise ValueError("El impuesto debe estar entre 0 y 100.")

        valor_descuento = subtotal * (descuento / 100)
        subtotal_descuento = subtotal - valor_descuento
        valor_impuesto = subtotal_descuento * (impuesto / 100)

        return round(subtotal_descuento + valor_impuesto, 2)


# CLASE RESERVA DE SALA
class ReservaSala(Servicio):

    def __init__(self, id_servicio, capacidad, costo_hora):
        super().__init__(id_servicio, "Reserva de sala", costo_hora)
        self.capacidad = capacidad
        self.costo_hora = costo_hora
        self.validar_parametros()

    def validar_parametros(self):
        if not isinstance(self.capacidad, int) or isinstance(self.capacidad, bool) or self.capacidad <= 0:
            raise ValueError("La capacidad debe ser un número entero positivo.")

        if self.costo_hora <= 0:
            raise ValueError("El costo por hora debe ser positivo.")

    def calcular_costo(self, cantidad=1, descuento=0, impuesto=0):
        self.validar_parametros()

        if cantidad <= 0:
            raise ValueError("Las horas deben ser mayores que cero.")

        subtotal = cantidad * self.costo_hora

        return self.aplicar_descuentos_impuestos(
            subtotal, descuento, impuesto
        )

    def describir_servicio(self):
        return (
            f"Servicio: {self.nombre}\n"
            f"ID: {self.id_servicio}\n"
            f"Capacidad: {self.capacidad} personas\n"
            f"Costo por hora: ${self.costo_hora}"
        )


# CLASE ALQUILER DE EQUIPOS
class AlquilerEquipo(Servicio):

    def __init__(self, id_servicio, tipo_equipo, costo_dia):
        super().__init__(id_servicio, "Alquiler de equipo", costo_dia)
        self.tipo_equipo = tipo_equipo
        self.costo_dia = costo_dia
        self.validar_parametros()

    def validar_parametros(self):
        if not isinstance(self.tipo_equipo, str) or not self.tipo_equipo.strip():
            raise ValueError("Debe especificar un tipo de equipo.")

        if self.costo_dia <= 0:
            raise ValueError("El costo por día debe ser positivo.")

    def calcular_costo(self, cantidad=1, descuento=0, impuesto=0):
        self.validar_parametros()

        if cantidad <= 0:
            raise ValueError("Los días deben ser mayores que cero.")

        subtotal = cantidad * self.costo_dia

        return self.aplicar_descuentos_impuestos(
            subtotal, descuento, impuesto
        )

    def describir_servicio(self):
        return (
            f"Servicio: {self.nombre}\n"
            f"ID: {self.id_servicio}\n"
            f"Tipo de equipo: {self.tipo_equipo}\n"
            f"Costo por día: ${self.costo_dia}"
        )


# CLASE ASESORÍA ESPECIALIZADA
class AsesoriaEspecializada(Servicio):

    def __init__(self, id_servicio, especialista, tarifa_hora):
        super().__init__(id_servicio, "Asesoría especializada", tarifa_hora)
        self.especialista = especialista
        self.tarifa_hora = tarifa_hora
        self.validar_parametros()

    def validar_parametros(self):
        if not isinstance(self.especialista, str) or not self.especialista.strip():
            raise ValueError("Debe especificar el nombre del especialista.")

        if self.tarifa_hora <= 0:
            raise ValueError("La tarifa por hora debe ser positiva.")

    def calcular_costo(self, cantidad=1, descuento=0, impuesto=0):
        self.validar_parametros()

        if cantidad <= 0:
            raise ValueError("Las horas deben ser mayores que cero.")

        subtotal = cantidad * self.tarifa_hora

        return self.aplicar_descuentos_impuestos(
            subtotal, descuento, impuesto
        )

    def describir_servicio(self):
        return (
            f"Servicio: {self.nombre}\n"
            f"ID: {self.id_servicio}\n"
            f"Especialista: {self.especialista}\n"
            f"Tarifa por hora: ${self.tarifa_hora}"
        )


# PRUEBAS DEL SISTEMA
if __name__ == "__main__":

    sala = ReservaSala(1, 30, 50000)
    equipo = AlquilerEquipo(2, "Video Beam", 80000)
    asesoria = AsesoriaEspecializada(3, "Ingeniero de sistemas", 60000)

    servicios = [sala, equipo, asesoria]
    cantidades = [3, 2, 4]

    for servicio, cantidad in zip(servicios, cantidades):
        print("\n---------------------------")
        print(servicio.describir_servicio())
        print("Costo normal: $", servicio.calcular_costo(cantidad))
        print("Costo con descuento e impuesto: $",
              servicio.calcular_costo(cantidad, 10, 19))




class ParametroInvalidoError(Exception):
    """
    Se genera cuando un parámetro obligatorio es inválido o está vacío.
    """
    pass
