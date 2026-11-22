from cliente import Cliente
from servicio import (
    ReservaSala,
    AlquilerEquipos,
    AsesoriaEspecializada
)
from sistema import SistemaGestion
from logger import registrar_error


def main():

    sistema = SistemaGestion()

    print("=== INICIO DE PRUEBAS ===")

    # ----------------------------------
    # CLIENTES VÁLIDOS
    # ----------------------------------

    try:

        cliente1 = Cliente(
            1,
            "Carlos Gómez",
            "carlos@gmail.com",
            "3001234567"
        )

        cliente2 = Cliente(
            2,
            "Ana Torres",
            "ana@gmail.com",
            "3012223344"
        )

        cliente3 = Cliente(
            3,
            "Luis Rojas",
            "luis@gmail.com",
            "3109876543"
        )

        sistema.agregar_cliente(cliente1)
        sistema.agregar_cliente(cliente2)
        sistema.agregar_cliente(cliente3)

    except Exception as e:
        registrar_error(str(e))

    # ----------------------------------
    # CLIENTE INVÁLIDO
    # ----------------------------------

    try:

        cliente_error = Cliente(
            4,
            "Pedro",
            "correo_invalido",
            "3001234567"
        )

        sistema.agregar_cliente(cliente_error)

    except Exception as e:

        registrar_error(str(e))

        print("Error controlado:", e)

    # ----------------------------------
    # SERVICIOS VÁLIDOS
    # ----------------------------------

    try:

        sala = ReservaSala(
            "S01",
            "Sala Empresarial",
            100,
            20
        )

        equipos = AlquilerEquipos(
            "E01",
            "Computadores",
            50,
            5
        )

        asesoria = AsesoriaEspecializada(
            "A01",
            "Consultoría",
            80,
            3
        )

        sistema.agregar_servicio(sala)
        sistema.agregar_servicio(equipos)
        sistema.agregar_servicio(asesoria)

    except Exception as e:
        registrar_error(str(e))

    # ----------------------------------
    # SERVICIO INVÁLIDO
    # ----------------------------------

    try:

        servicio_error = ReservaSala(
            "S02",
            "Sala inválida",
            -10,
            10
        )

    except Exception as e:

        registrar_error(str(e))

        print("Error controlado:", e)

    # ----------------------------------
    # RESERVA CORRECTA
    # ----------------------------------

    try:

        reserva1 = sistema.crear_reserva(
            cliente1,
            sala,
            2,
            "2026-11-16"
        )

        reserva1.confirmar()

        reserva1.procesar()

        print(
            "Total reserva:",
            reserva1.calcular_total()
        )

    except Exception as e:

        registrar_error(str(e))

    # ----------------------------------
    # RESERVA INVÁLIDA
    # ----------------------------------

    try:

        sistema.crear_reserva(
            cliente1,
            sala,
            -3,
            "2026-11-16"
        )

    except Exception as e:

        registrar_error(str(e))

        print("Error controlado:", e)

    # ----------------------------------
    # RESULTADOS
    # ----------------------------------

    print("\nCLIENTES")
    sistema.mostrar_clientes()

    print("\nSERVICIOS")
    sistema.mostrar_servicios()

    print("\nRESERVAS")
    sistema.mostrar_reservas()

    print("\n=== FIN DE PRUEBAS ===")


if __name__ == "__main__":
    main()
