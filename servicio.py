from abc import ABC, abstractmethod

# CLASE ABSTRACTA PRINCIPAL
class Servicio(ABC):

    def __init__(self,
                 id_servicio,
                 nombre,
                 costo_base,):
                     
        self.id_servicio = id_servicio
        self.nombre = nombre
        self.costo_base = costo_base

    @abstractmethod
    def calcular_costo(self, cantidad=1, descuento=0, impuesto=0):
        pass

    @abstractmethod
    def descripcion(self):
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

    def __init__(
        self,
        id_servicio,
        nombre,
        costo_hora,
        capacidad
    ):
        super().__init__(
            id_servicio,
            nombre,
            costo_hora
        )
        
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

    def descripcion(self):
        return (
            f"Servicio: {self.nombre}\n"
            f"ID: {self.id_servicio}\n"
            f"Capacidad: {self.capacidad} personas\n"
            f"Costo por hora: ${self.costo_hora}"
        )


# CLASE ALQUILER DE EQUIPOS

class AlquilerEquipos(Servicio):

    def __init__(
        self,
        id_servicio,
        nombre,
        costo_dia,
        cantidad
    ):
        
        super().__init__(
            id_servicio,
            nombre,
            costo_dia
        )
        self.cantidad = cantidad
        self.costo_dia = costo_dia
        self.validar_parametros()

    def validar_parametros(self):
        if self.cantidad <= 0:
            
            raise ValueError("la cantidad deve ser positiva."
            )

        if self.costo_dia <= 0:
            raise ValueError("El costo por día debe ser positivo.")

    def calcular_costo(self, cantidad=1, descuento=0, impuesto=0):
        self.validar_parametros()
        cantidad_num = float(cantidad)

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        subtotal = cantidad_num * float(self.costo_dia)

        return self.aplicar_descuentos_impuestos(
            subtotal,
            float(descuento),
            float(impuesto)
        )

    def descripcion(self):
        return (
            f"Servicio: {self.nombre}\n"
            f"ID: {self.id_servicio}\n"
            f"cantidad: {self.cantidad}\n"
            f"Costo por día: ${self.costo_dia}"
        )


# CLASE ASESORÍA ESPECIALIZADA

class AsesoriaEspecializada(Servicio):

    def __init__(
        self,
        id_servicio,
        nombre,
        tarifa_hora,
        horas
    ):
        super().__init__(
            id_servicio,
            nombre,
            tarifa_hora
        )
        self.horas = horas
        self.tarifa_hora = tarifa_hora
        self.validar_parametros()

    def validar_parametros(self):
        if self.horas <= 0: 
            
            raise ValueError("las horas deben ser positivas."
            )

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

    def descripcion(self):
        return (
            f"Servicio: {self.nombre}\n"
            f"ID: {self.id_servicio}\n"
            f"horas: {self.horas}\n"
            f"Tarifa por hora: ${self.tarifa_hora}"
        )

        
