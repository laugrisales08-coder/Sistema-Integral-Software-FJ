"""Lógica de administración del sistema y registro de eventos."""

import logging
from excepciones import ElementoNoEncontradoError, DatoInvalidoError
from modelos import Cliente, Servicio, Reserva


logging.basicConfig(
    filename="software_fj.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8"
)
logger = logging.getLogger("SoftwareFJ")


class SistemaSoftwareFJ:
    """Administra listas internas de clientes, servicios y reservas."""

    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, cliente):
        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("El objeto no corresponde a un cliente.")
        if any(c.identificador == cliente.identificador for c in self.clientes):
            raise DatoInvalidoError("Ya existe un cliente con ese identificador.")
        self.clientes.append(cliente)
        logger.info("Cliente registrado: %s", cliente.identificador)
        return cliente

    def registrar_servicio(self, servicio):
        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("El objeto no corresponde a un servicio.")
        if any(s.identificador == servicio.identificador for s in self.servicios):
            raise DatoInvalidoError("Ya existe un servicio con ese identificador.")
        self.servicios.append(servicio)
        logger.info("Servicio registrado: %s", servicio.identificador)
        return servicio

    def crear_reserva(self, identificador, id_cliente, id_servicio, duracion):
        cliente = next((c for c in self.clientes if c.identificador == str(id_cliente)), None)
        servicio = next((s for s in self.servicios if s.identificador == str(id_servicio)), None)
        if cliente is None:
            raise ElementoNoEncontradoError("No se encontró el cliente solicitado.")
        if servicio is None:
            raise ElementoNoEncontradoError("No se encontró el servicio solicitado.")
        if any(r.identificador == str(identificador) for r in self.reservas):
            raise DatoInvalidoError("Ya existe una reserva con ese identificador.")
        reserva = Reserva(identificador, cliente, servicio, duracion)
        self.reservas.append(reserva)
        logger.info("Reserva creada: %s", identificador)
        return reserva

    def buscar_reserva(self, identificador):
        reserva = next((r for r in self.reservas if r.identificador == str(identificador)), None)
        if reserva is None:
            raise ElementoNoEncontradoError("No se encontró la reserva.")
        return reserva

    def listar_datos(self):
        print("\\n--- CLIENTES ---")
        for cliente in self.clientes:
            print(cliente.describir())
        print("\\n--- SERVICIOS ---")
        for servicio in self.servicios:
            print(servicio.describir(), "| Precio:", servicio.precio_base)
        print("\\n--- RESERVAS ---")
        for reserva in self.reservas:
            print(reserva.describir())
