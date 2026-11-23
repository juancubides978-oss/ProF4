from reserva import Reserva
from logger import registrar_evento


class SistemaGestion:

    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def agregar_cliente(self, cliente):

        self.clientes.append(cliente)

        registrar_evento(
            f"Cliente agregado: {cliente.get_nombre()}"
        )

    def agregar_servicio(self, servicio):

        self.servicios.append(servicio)

        registrar_evento(
            f"Servicio agregado: {servicio.descripcion()}"
        )

    def crear_reserva(
        self,
        cliente,
        servicio,
        duracion,
        fecha
    ):

        reserva = Reserva(
            cliente,
            servicio,
            duracion,
            fecha
        )

        self.reservas.append(reserva)

        registrar_evento(
            "Reserva creada correctamente."
        )

        return reserva

    def mostrar_clientes(self):

        for cliente in self.clientes:
            print(cliente)

    def mostrar_servicios(self):

        for servicio in self.servicios:
            print(servicio.descripcion())

    def mostrar_reservas(self):

        for reserva in self.reservas:
            print(reserva)
