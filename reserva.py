from datetime import datetime
from exceptions import (
    ReservaError,
    ParametroInvalidoError
)


class Reserva:

    ESTADOS_VALIDOS = [
        "Pendiente",
        "Confirmada",
        "Procesada",
        "Cancelada"
    ]

    def __init__(self, cliente, servicio, duracion, fecha):

        if cliente is None:
            raise ReservaError(
                "La reserva debe tener un cliente."
            )

        if servicio is None:
            raise ReservaError(
                "La reserva debe tener un servicio."
            )

        if duracion <= 0:
            raise ParametroInvalidoError(
                "La duración debe ser mayor que cero."
            )

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.fecha = fecha
        self.estado = "Pendiente"
      
    # Confirmar reserva
 

    def confirmar(self):

        try:

            if self.estado == "Cancelada":
                raise ReservaError(
                    "No se puede confirmar una reserva cancelada."
                )

            self.estado = "Confirmada"

        except ReservaError:
            raise


    # Cancelar reserva
   

    def cancelar(self):

        self.estado = "Cancelada"

    # Procesar reserva
  

    def procesar(self):

        try:

            if self.estado == "Cancelada":
                raise ReservaError(
                    "No se puede procesar una reserva cancelada."
                )

            if self.estado != "Confirmada":
                raise ReservaError(
                    "La reserva debe estar confirmada antes de procesarse."
                )

        except ReservaError:
            raise

        else:
            self.estado = "Procesada"

  
    # Calcular total
  

    def calcular_total(self,descuento=0, impuesto=0):

        try:
            return self.servicio.calcular_costo(
                cantidad=self.duracion,
                descuento=descuento,
                impuesto=inpuesto
            )

        except Exception as e:

            raise ReservaError(
                "Error al calcular el valor total de la reserva."
            ) from e

        finally:
            print(
                "Proceso de cálculo finalizado."
            )


    # Mostrar información
  

    def mostrar_detalle(self):

        return (
            f"Cliente: {self.cliente.get_nombre()}\n"
            f"Servicio: {self.servicio.descripcion()}\n"
            f"Duración: {self.duracion}\n"
            f"Fecha: {self.fecha}\n"
            f"Estado: {self.estado}"
        )

    def __str__(self):

        return (
            f"Reserva("
            f"Cliente={self.cliente.get_nombre()}, "
            f"Servicio={self.servicio.nombre}, "
            f"Estado={self.estado})"
        )
        
