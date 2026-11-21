"""Punto de entrada del programa Software FJ."""

from sistema import SistemaSoftwareFJ, logger
from modelos import Cliente, ReservaSala, AlquilerEquipo, Asesoria
from excepciones import ErrorSistema


def ejecutar_demostracion():
    """Ejecuta más de 10 operaciones, incluyendo casos correctos e incorrectos."""
    sistema = SistemaSoftwareFJ()
    print("=== DEMOSTRACIÓN DEL SISTEMA SOFTWARE FJ ===")

    # 1. Registro válido de cliente.
    try:
        sistema.registrar_cliente(Cliente("C01", "Ana Pérez", "ana@email.com", "3001234567"))
        print("1. Cliente válido registrado.")
    except ErrorSistema as error:
        print("1. Error:", error)

    # 2. Registro inválido de cliente.
    try:
        sistema.registrar_cliente(Cliente("C02", "A", "correo incorrecto", "123"))
    except ErrorSistema as error:
        logger.exception("Operación 2: registro inválido de cliente")
        print("2. Cliente inválido controlado:", error)

    # 3. Segundo cliente válido.
    try:
        sistema.registrar_cliente(Cliente("C03", "Carlos Ruiz", "carlos@email.com", "3115556677"))
        print("3. Segundo cliente registrado.")
    except ErrorSistema as error:
        print("3. Error:", error)

    # 4. Creación correcta de servicio de sala.
    try:
        sistema.registrar_servicio(ReservaSala("S01", "Sala de reuniones", 50000))
        print("4. Servicio de sala registrado.")
    except ErrorSistema as error:
        print("4. Error:", error)

    # 5. Creación correcta de alquiler de equipo.
    try:
        sistema.registrar_servicio(AlquilerEquipo("S02", "Portátil", 80000))
        print("5. Servicio de equipo registrado.")
    except ErrorSistema as error:
        print("5. Error:", error)

    # 6. Creación correcta de asesoría.
    try:
        sistema.registrar_servicio(Asesoria("S03", "Asesoría de software", 100000))
        print("6. Servicio de asesoría registrado.")
    except ErrorSistema as error:
        print("6. Error:", error)

    # 7. Intento de crear servicio con precio inválido.
    try:
        servicio_invalido = ReservaSala("S04", "Sala inválida", -100)
        sistema.registrar_servicio(servicio_invalido)
    except ErrorSistema as error:
        logger.exception("Operación 7: servicio con precio inválido")
        print("7. Servicio inválido controlado:", error)

    # 8. Crear reserva correctamente.
    try:
        reserva = sistema.crear_reserva("R01", "C01", "S01", 2)
        print("8. Reserva creada:", reserva.identificador)
    except ErrorSistema as error:
        print("8. Error:", error)

    # 9. Confirmar reserva.
    try:
        reserva.confirmar()
        print("9. Reserva confirmada.")
    except ErrorSistema as error:
        print("9. Error:", error)

    # 10. Procesar reserva y calcular costo con impuesto.
    try:
        total = reserva.procesar(impuesto=0.19)
        print(f"10. Reserva procesada. Total con impuesto: ${total:,.2f}")
    except ErrorSistema as error:
        print("10. Error:", error)

    # 11. Intento de reserva con cliente inexistente.
    try:
        sistema.crear_reserva("R02", "NO_EXISTE", "S02", 1)
    except ErrorSistema as error:
        logger.exception("Operación 11: reserva con cliente inexistente")
        print("11. Reserva fallida controlada:", error)

    # 12. Cancelar una reserva.
    try:
        reserva.cancelar()
        print("12. Reserva cancelada.")
    except ErrorSistema as error:
        print("12. Error:", error)

    # Ejemplo de try/except/else/finally.
    try:
        print("\\nVerificando cantidad de reservas...")
        cantidad = len(sistema.reservas)
    except Exception as error:
        logger.exception("Error al contar reservas")
        print("No fue posible contar las reservas:", error)
    else:
        print("Verificación correcta. Reservas creadas:", cantidad)
    finally:
        print("La verificación terminó.")

    sistema.listar_datos()
    print("\\nLos eventos y errores se guardaron en software_fj.log")


def menu():
    """Menú sencillo para ejecutar la demostración o consultar información."""
    sistema = SistemaSoftwareFJ()
    while True:
        print("\\n===== SOFTWARE FJ =====")
        print("1. Ejecutar demostración de 12 operaciones")
        print("2. Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            ejecutar_demostracion()
        elif opcion == "2":
            print("Gracias por utilizar Software FJ.")
            break
        else:
            print("Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\\nPrograma finalizado por el usuario.")
    except Exception as error:
        logger.exception("Error inesperado en la aplicación")
        print("Se controló un error inesperado:", error)
