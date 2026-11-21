"""Clases del modelo: entidades, clientes, servicios y reservas."""

from abc import ABC, abstractmethod
from datetime import datetime
from excepciones import (
    DatoInvalidoError, ServicioNoDisponibleError, ReservaError
)


class Entidad(ABC):
    """Clase abstracta que representa una entidad general del sistema."""

    def __init__(self, identificador):
        if not identificador or not str(identificador).strip():
            raise DatoInvalidoError("El identificador no puede estar vacío.")
        self._identificador = str(identificador).strip()

    @property
    def identificador(self):
        return self._identificador

    @abstractmethod
    def describir(self):
        """Cada entidad concreta debe describirse."""


class Cliente(Entidad):
    """Representa a un cliente y protege sus datos mediante propiedades."""

    def __init__(self, identificador, nombre, correo, telefono):
        super().__init__(identificador)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 2:
            raise DatoInvalidoError("El nombre debe tener al menos 2 caracteres.")
        self._nombre = valor.strip()

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str) or "@" not in valor or "." not in valor.split("@")[-1]:
            raise DatoInvalidoError("El correo electrónico no es válido.")
        self._correo = valor.strip()

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        numero = str(valor).strip()
        if not numero.isdigit() or len(numero) < 7:
            raise DatoInvalidoError("El teléfono debe contener al menos 7 dígitos.")
        self._telefono = numero

    def describir(self):
        return f"Cliente: {self.nombre} | Correo: {self.correo} | Teléfono: {self.telefono}"


class Servicio(Entidad, ABC):
    """Clase abstracta para los servicios ofrecidos por Software FJ."""

    def __init__(self, identificador, nombre, precio_base, disponible=True):
        super().__init__(identificador)
        if not nombre or not str(nombre).strip():
            raise DatoInvalidoError("El nombre del servicio no puede estar vacío.")
        if not isinstance(precio_base, (int, float)) or precio_base <= 0:
            raise DatoInvalidoError("El precio base debe ser un número mayor que cero.")
        self.nombre = str(nombre).strip()
        self.precio_base = float(precio_base)
        self.disponible = bool(disponible)

    @abstractmethod
    def calcular_costo(self, duracion=1, impuesto=0, descuento=0):
        """Calcula el costo según el tipo de servicio."""

    @abstractmethod
    def validar_parametros(self, duracion):
        """Valida la duración solicitada."""

    def describir(self):
        return f"{self.nombre} (ID: {self.identificador})"


class ReservaSala(Servicio):
    """Servicio de reserva de salas; el precio se cobra por hora."""

    def validar_parametros(self, duracion):
        if not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatoInvalidoError("La duración de la sala debe ser mayor que cero.")

    def calcular_costo(self, duracion=1, impuesto=0, descuento=0):
        self.validar_parametros(duracion)
        return _calcular_total(self.precio_base * duracion, impuesto, descuento)

    def describir(self):
        return f"Reserva de sala por hora: {self.nombre}"


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos; el precio se cobra por día."""

    def validar_parametros(self, duracion):
        if not isinstance(duracion, int) or duracion <= 0:
            raise DatoInvalidoError("La duración del alquiler debe ser un número entero de días.")

    def calcular_costo(self, duracion=1, impuesto=0, descuento=0):
        self.validar_parametros(duracion)
        return _calcular_total(self.precio_base * duracion, impuesto, descuento)

    def describir(self):
        return f"Alquiler de equipo por día: {self.nombre}"


class Asesoria(Servicio):
    """Servicio de asesoría especializada; el precio se cobra por sesión."""

    def validar_parametros(self, duracion):
        if not isinstance(duracion, int) or duracion <= 0:
            raise DatoInvalidoError("La cantidad de sesiones debe ser un entero positivo.")

    def calcular_costo(self, duracion=1, impuesto=0, descuento=0):
        self.validar_parametros(duracion)
        return _calcular_total(self.precio_base * duracion, impuesto, descuento)

    def describir(self):
        return f"Asesoría especializada por sesión: {self.nombre}"


def _calcular_total(subtotal, impuesto=0, descuento=0):
    """Aplica porcentajes de impuesto y descuento y valida los valores."""
    if not 0 <= impuesto <= 1:
        raise DatoInvalidoError("El impuesto debe expresarse entre 0 y 1.")
    if not 0 <= descuento <= 1:
        raise DatoInvalidoError("El descuento debe expresarse entre 0 y 1.")
    total = subtotal * (1 - descuento) * (1 + impuesto)
    if total < 0:
        raise DatoInvalidoError("El cálculo produjo un total inconsistente.")
    return round(total, 2)


class Reserva:
    """Integra cliente, servicio, duración y estado de una reserva."""

    def __init__(self, identificador, cliente, servicio, duracion):
        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("Debe seleccionar un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("Debe seleccionar un servicio válido.")
        servicio.validar_parametros(duracion)
        self.identificador = str(identificador)
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"
        self.fecha_creacion = datetime.now()

    def confirmar(self):
        if self.estado != "Pendiente":
            raise ReservaError("Solo se pueden confirmar reservas pendientes.")
        if not self.servicio.disponible:
            raise ServicioNoDisponibleError("El servicio seleccionado no está disponible.")
        self.estado = "Confirmada"
        return self.estado

    def cancelar(self):
        if self.estado == "Cancelada":
            raise ReservaError("La reserva ya está cancelada.")
        self.estado = "Cancelada"
        return self.estado

    def procesar(self, impuesto=0, descuento=0):
        if self.estado != "Confirmada":
            raise ReservaError("La reserva debe estar confirmada antes de procesar el pago.")
        try:
            return self.servicio.calcular_costo(self.duracion, impuesto, descuento)
        except DatoInvalidoError as error:
            # Encadenamiento: conserva el error original como causa del nuevo error.
            raise ReservaError("No fue posible calcular el costo de la reserva.") from error

    def describir(self):
        return (f"Reserva {self.identificador} | {self.cliente.nombre} | "
                f"{self.servicio.nombre} | Duración: {self.duracion} | Estado: {self.estado}")
