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
