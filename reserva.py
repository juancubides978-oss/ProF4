"""
Módulo: reserva.py
Descripción: Clase Reserva del sistema Software FJ. Integra cliente, servicio, 
             duración y estado. Implementa confirmación, cancelación, procesamiento 
             y encadenamiento de excepciones.
Autor: Estudiante 3
Curso: Programación 213023 - Fase 4
"""

from enum import Enum
from datetime import datetime
import uuid

# Importamos las excepciones creadas por el Estudiante 1
# (Asegúrate de que los nombres coincidan con lo que hay en exceptions.py)
try:
    from exceptions import ReservaInvalidaError, ServicioNoDisponibleError
except ImportError:
    # Respaldo por si el archivo se llama diferente
    class ReservaInvalidaError(Exception): pass
    class ServicioNoDisponibleError(Exception): pass

# Clase Logger básica por si el Estudiante 4 aún no ha subido su módulo
try:
    from logger import logger
except ImportError:
    import logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)


class EstadoReserva(Enum):
    """Estados posibles de una reserva."""
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"
    PROCESADA = "PROCESADA"
    FALLIDA = "FALLIDA"


class Reserva:
    """
    Representa una reserva en el sistema.
    """

    def __init__(self, cliente, servicio, duracion, id_reserva=None):
        # Atributos encapsulados (privados)
        self.__id_reserva = id_reserva or f"RES-{uuid.uuid4().hex[:8].upper()}"
        self.__cliente = None
        self.__servicio = None
        self.__duracion = None
        self.__estado = EstadoReserva.PENDIENTE
        self.__costo_final = 0.0
        self.__fecha_creacion = datetime.now()

        # Validaciones iniciales
        self.set_cliente(cliente)
        self.set_servicio(servicio)
        self.set_duracion(duracion)

    # ---------- Setters con validación y Encapsulamiento ----------
    def set_cliente(self, cliente):
        if cliente is None:
            raise ReservaInvalidaError("El cliente no puede ser None")
        # Validación tipo 'Duck Typing' (verifica que tenga el método describir)
        if not hasattr(cliente, "describir"):
            raise ReservaInvalidaError(f"Objeto inválido como cliente: {type(cliente).__name__}")
        self.__cliente = cliente

    def set_servicio(self, servicio):
        if servicio is None:
            raise ReservaInvalidaError("El servicio no puede ser None")
        if not hasattr(servicio, "calcular_costo"):
            raise ReservaInvalidaError(f"Objeto inválido como servicio: {type(servicio).__name__}")
        self.__servicio = servicio

    def set_duracion(self, duracion):
        try:
            duracion = int(duracion)
        except (ValueError, TypeError) as e:
            # 🔗 ENCADENAMIENTO #1: Se envuelve el error original de conversión
            raise ReservaInvalidaError(f"Duración inválida: {duracion!r} no es un entero") from e
        if duracion <= 0:
            raise ReservaInvalidaError(f"Duración debe ser positiva, recibido: {duracion}")
        if duracion > 24:
            raise ReservaInvalidaError(f"Duración excede el máximo permitido (24h): {duracion}")
        self.__duracion = duracion

    # ---------- Propiedades (Getters) ----------
    @property
    def estado(self):
        return self.__estado

    @property
    def costo_final(self):
        return self.__costo_final

    @property
    def id_reserva(self):
        return self.__id_reserva

    # ---------- Métodos de Procesamiento ----------

    def confirmar(self, impuesto=0.19, descuento=0.0):
        """
        Confirma la reserva si el servicio está disponible.
        Usa try/except/else
        """
        try:
            # Validaciones
            self.__servicio.validar_parametros(self.__duracion)
            costo = self.__servicio.calcular_costo(self.__duracion, impuesto=impuesto, descuento=descuento)
            
            if costo <= 0:
                raise ServicioNoDisponibleError(f"Costo inconsistente calculado: {costo}")
                
        except ServicioNoDisponibleError as e:
            # 🔗 ENCADENAMIENTO #2: Se relanza como excepción de reserva
            self.__estado = EstadoReserva.FALLIDA
            logger.error(f"Reserva {self.__id_reserva} falló: {e}")
            raise ReservaInvalidaError(f"No se pudo confirmar la reserva {self.__id_reserva}") from e
        except Exception as e:
            self.__estado = EstadoReserva.FALLIDA
            raise ReservaInvalidaError(f"Error inesperado al confirmar reserva: {e}") from e
        else:
            # ✅ Solo se ejecuta si NO hubo excepciones
            self.__costo_final = costo
            self.__estado = EstadoReserva.CONFIRMADA
            logger.info(f"Reserva {self.__id_reserva} CONFIRMADA | Cliente: {self.__cliente.describir()} | Costo: ${costo:,.2f}")
            return True

    def cancelar(self, motivo="Sin motivo"):
        """Cancela la reserva si el estado lo permite."""
        if self.__estado == EstadoReserva.CANCELADA:
            raise ReservaInvalidaError(f"La reserva {self.__id_reserva} ya está cancelada")
        if self.__estado == EstadoReserva.PROCESADA:
            raise ReservaInvalidaError(f"No se puede cancelar reserva ya procesada")
        
        self.__estado = EstadoReserva.CANCELADA
        logger.warning(f"Reserva {self.__id_reserva} CANCELADA | Motivo: {motivo}")
        return True

    def procesar(self):
        """
        Procesa una reserva confirmada.
        Usa try/except/finally (el finally registra la auditoría siempre)
        """
        resultado = None
        try:
            if self.__estado != EstadoReserva.CONFIRMADA:
                raise ReservaInvalidaError(f"Solo se procesan reservas CONFIRMADAS. Estado actual: {self.__estado.value}")
            
            if self.__costo_final <= 0:
                raise ServicioNoDisponibleError(f"Costo inválido al procesar: {self.__costo_final}")
                
            self.__estado = EstadoReserva.PROCESADA
            resultado = {
                "id": self.__id_reserva,
                "cliente": self.__cliente.describir(),
                "servicio": self.__servicio.describir() if hasattr(self.__servicio, "describir") else "Servicio",
                "duracion": self.__duracion,
                "costo": self.__costo_final,
                "estado": self.__estado.value
            }
            logger.info(f"Reserva {self.__id_reserva} PROCESADA | ${self.__costo_final:,.2f}")
            
        except ReservaInvalidaError as e:
            self.__estado = EstadoReserva.FALLIDA
            logger.error(f"Reserva {self.__id_reserva} no procesada: {e}")
            raise
        except Exception as e:
            # 🔗 ENCADENAMIENTO #3: Excepción genérica envuelta
            self.__estado = EstadoReserva.FALLIDA
            logger.critical(f"Error inesperado procesando {self.__id_reserva}: {e}")
            raise ReservaInvalidaError(f"Error inesperado al procesar reserva {self.__id_reserva}") from e
        finally:
            # ✅ SIEMPRE se ejecuta
            logger.debug(f"[AUDITORÍA] Reserva {self.__id_reserva} | Estado final: {self.__estado.value} | Timestamp: {datetime.now().isoformat()}")
            
        return resultado

    # ---------- Representación ----------
    def __str__(self):
        return (f"Reserva[{self.__id_reserva}] {self.__cliente.describir()} | "
                f"Estado: {self.__estado.value} | Costo: ${self.__costo_final:,.2f}")
