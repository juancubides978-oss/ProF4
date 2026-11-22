from cliente import Cliente
from servicio import (
    ReservaSala,
    AlquilerEquipo,
    AsesoriaEspecializada
)
# =====================================================
# Este módulo integra clientes, servicios y reservas,
# administra los registros del sistema mediante logs
# y ejecuta las pruebas solicitadas en la actividad.
# =====================================================

import logging

# =====================================================
# CONFIGURACIÓN DEL SISTEMA DE LOGS
# =====================================================
# Se configura un archivo llamado eventos.log en el
# que se almacenarán tanto los eventos exitosos como
# los errores detectados durante la ejecución.

logging.basicConfig(
    filename="eventos.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def registrar_info(mensaje):
    logging.info(mensaje)

def registrar_error(mensaje):
    logging.error(mensaje)


# =====================================================
# CLASE RESERVA
# =====================================================
# Esta clase permite relacionar un cliente con un
# servicio. Además, controla el estado de la reserva,
# calcula su costo y maneja excepciones cuando se
# producen operaciones inválidas.
# =====================================================

class ReservaError(Exception):
    pass


class Reserva:

    def __init__(self, cliente, servicio, cantidad):

        if cliente is None:
            raise ReservaError(
                "Debe existir un cliente."
            )

        if servicio is None:
            raise ReservaError(
                "Debe existir un servicio."
            )

        if cantidad <= 0:
            raise ReservaError(
                "La duración o cantidad debe ser mayor que cero."
            )

        self.cliente = cliente
        self.servicio = servicio
        self.cantidad = cantidad
        self.estado = "Pendiente"

    def confirmar(self):

        if self.estado == "Cancelada":
            raise ReservaError(
                "No se puede confirmar una reserva cancelada."
            )

        self.estado = "Confirmada"

    def cancelar(self):

        if self.estado == "Cancelada":
            raise ReservaError(
                "La reserva ya fue cancelada."
            )

        self.estado = "Cancelada"

    def procesar(self):

        try:

            if self.estado != "Confirmada":
                raise ReservaError(
                    "La reserva debe estar confirmada."
                )

            self.estado = "Procesada"

        except Exception as e:

            raise ReservaError(
                "Error al procesar la reserva."
            ) from e

    def calcular_total(self):

        return self.servicio.calcular_costo(
            self.cantidad
        )

    def __str__(self):

        return (
            f"Cliente: {self.cliente.get_nombre()} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Cantidad: {self.cantidad} | "
            f"Estado: {self.estado}"
        )


# =====================================================
# CLASE SISTEMA DE GESTIÓN
# =====================================================
# Esta clase administra todas las listas internas del
# sistema: clientes, servicios y reservas.
# =====================================================

class SistemaGestion:

    def __init__(self):

        self.clientes = []
        self.servicios = []
        self.reservas = []

    # =================================================
    # AGREGAR CLIENTE
    # =================================================
    def agregar_cliente(self, cliente):

        try:

            self.clientes.append(cliente)

            registrar_info(
                f"Cliente agregado: {cliente.get_nombre()}"
            )

        except Exception as e:

            registrar_error(
                f"Error agregando cliente: {e}"
            )

    # =================================================
    # AGREGAR SERVICIO
    # =================================================
    def agregar_servicio(self, servicio):

        try:

            self.servicios.append(servicio)

            registrar_info(
                f"Servicio agregado: {servicio.nombre}"
            )

        except Exception as e:

            registrar_error(
                f"Error agregando servicio: {e}"
            )

    # =================================================
    # AGREGAR RESERVA
    # =================================================
    def agregar_reserva(self, reserva):

        try:

            self.reservas.append(reserva)

            registrar_info(
                "Reserva agregada correctamente."
            )

        except Exception as e:

            registrar_error(
                f"Error agregando reserva: {e}"
            )

    # =================================================
    # MOSTRAR CLIENTES
    # =================================================
    def mostrar_clientes(self):

        print("\n===== CLIENTES REGISTRADOS =====")

        for cliente in self.clientes:
            print(cliente)

    # =================================================
    # MOSTRAR SERVICIOS
    # =================================================
    def mostrar_servicios(self):

        print("\n===== SERVICIOS REGISTRADOS =====")

        for servicio in self.servicios:

            print("\n--------------------------------")

            print(
                servicio.describir_servicio()
            )

    # =================================================
    # MOSTRAR RESERVAS
    # =================================================
    def mostrar_reservas(self):

        print("\n===== RESERVAS REGISTRADAS =====")

        for reserva in self.reservas:
            print(reserva)


# =====================================================
# INICIO DE LA SIMULACIÓN DEL SISTEMA
# =====================================================
# Se crea la instancia principal encargada de
# gestionar toda la información de Software FJ.
# =====================================================

def main():

    sistema = SistemaGestion()

    print("===================================")
    print("      SISTEMA SOFTWARE FJ")
    print("===================================")

    # =================================================
    # OPERACIÓN 1
    # REGISTRO DE CLIENTE VÁLIDO
    # =================================================

    try:

        cliente1 = Cliente(
            1,
            "Juan Perez",
            "juan@gmail.com",
            "3201111111"
        )

        sistema.agregar_cliente(cliente1)

    except Exception as e:
        registrar_error(e)

    # =================================================
    # OPERACIÓN 2
    # REGISTRO DE CLIENTE VÁLIDO
    # =================================================

    try:

        cliente2 = Cliente(
            2,
            "Maria Lopez",
            "maria@gmail.com",
            "3202222222"
        )

        sistema.agregar_cliente(cliente2)

    except Exception as e:
        registrar_error(e)

    # =================================================
    # OPERACIÓN 3
    # REGISTRO DE CLIENTE INVÁLIDO
    # Se prueba el manejo de excepciones.
    # =================================================

    try:

        cliente3 = Cliente(
            3,
            "",
            "correo_malo",
            "abc123"
        )

        sistema.agregar_cliente(cliente3)

    except Exception as e:
        registrar_error(e)

    # =================================================
    # OPERACIÓN 4
    # CREACIÓN DE SERVICIO RESERVA DE SALA
    # =================================================

    try:

        sala = ReservaSala(
            100,
            30,
            50000
        )

        sistema.agregar_servicio(sala)

    except Exception as e:
        registrar_error(e)

    # =================================================
    # OPERACIÓN 5
    # CREACIÓN DE SERVICIO ALQUILER DE EQUIPO
    # =================================================

    try:

        equipo = AlquilerEquipo(
            101,
            "Video Beam",
            80000
        )

        sistema.agregar_servicio(equipo)

    except Exception as e:
        registrar_error(e)

    # =================================================
    # OPERACIÓN 6
    # CREACIÓN DE SERVICIO DE ASESORÍA
    # =================================================

    try:

        asesoria = AsesoriaEspecializada(
            102,
            "Ingeniero de Sistemas",
            60000
        )

        sistema.agregar_servicio(asesoria)

    except Exception as e:
        registrar_error(e)

    # =================================================
    # OPERACIÓN 7
    # CREACIÓN DE SERVICIO INVÁLIDO
    # =================================================

    try:

        servicio_error = ReservaSala(
            103,
            -5,
            50000
        )

        sistema.agregar_servicio(servicio_error)

    except Exception as e:
        registrar_error(e)

    # =================================================
    # OPERACIÓN 8
    # RESERVA VÁLIDA DE SALA
    # Se confirma y procesa correctamente.
    # =================================================

    try:

        reserva1 = Reserva(
            cliente1,
            sala,
            3
        )

        reserva1.confirmar()

        reserva1.procesar()

        sistema.agregar_reserva(
            reserva1
        )

        print(
            f"\nTotal Reserva 1: ${reserva1.calcular_total()}"
        )

    except Exception as e:
        registrar_error(e)

    # =================================================
    # OPERACIÓN 9
    # RESERVA VÁLIDA DE ASESORÍA
    # =================================================

    try:

        reserva2 = Reserva(
            cliente2,
            asesoria,
            4
        )

        reserva2.confirmar()

        sistema.agregar_reserva(
            reserva2
        )

        print(
            f"Total Reserva 2: ${reserva2.calcular_total()}"
        )

    except Exception as e:
        registrar_error(e)

    # =================================================
    # OPERACIÓN 10
    # RESERVA INVÁLIDA
    # Se intenta registrar una reserva con
    # duración negativa para probar excepciones.
    # =================================================

    try:

        reserva3 = Reserva(
            cliente1,
            equipo,
            -3
        )

        sistema.agregar_reserva(
            reserva3
        )

    except Exception as e:
        registrar_error(e)

    # =================================================
    # REPORTE FINAL DEL SISTEMA
    # =================================================
    # Se muestran todos los clientes, servicios
    # y reservas registrados durante la simulación.
    # =================================================

    print("\n===================================")
    print("     RESUMEN DEL SISTEMA")
    print("===================================")

    sistema.mostrar_clientes()

    sistema.mostrar_servicios()

    sistema.mostrar_reservas()

    # =================================================
    # CIERRE DE LA EJECUCIÓN
    # =================================================

    registrar_info(
        "Simulación finalizada correctamente."
    )

    print(
        "\nRevise el archivo eventos.log para consultar "
        "los registros del sistema."
    )


if __name__ == "__main__":
    main()
