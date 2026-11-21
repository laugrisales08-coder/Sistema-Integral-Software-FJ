"""Excepciones personalizadas del sistema Software FJ."""

class ErrorSistema(Exception):
    """Excepción base para errores controlados del sistema."""

class DatoInvalidoError(ErrorSistema):
    """Se presenta cuando un dato no cumple las validaciones."""

class ServicioNoDisponibleError(ErrorSistema):
    """Se presenta cuando un servicio no está disponible."""

class ReservaError(ErrorSistema):
    """Se presenta cuando una reserva no puede procesarse."""

class ElementoNoEncontradoError(ErrorSistema):
    """Se presenta cuando no existe un cliente, servicio o reserva."""
