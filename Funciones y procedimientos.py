# =====================================================================
# TEMA 4: Funciones y Procedimientos (Parte 4) - Buenas Prácticas
# Ejercicio 1: Clínica Médica | Ejercicio 2: E-Commerce
# =====================================================================

import logging
from datetime import datetime

# Configuración básica de logs para auditoría y trazabilidad
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s]: %(message)s')


# =====================================================================
# EJERCICIO 1: Sistema de Gestión de Pacientes para una Clínica
# Arquitectura en capas: Datos, Lógica de Negocio y Presentación
# =====================================================================

class ClinicaDataLayer:
    """Capa de acceso a datos (Simulada con repositorios en memoria seguros)."""
    def __init__(self):
        self.pacientes = {}  # {id_paciente: {datos_personales, historial}}
        self.citas = []      # Lista de citas programadas

class PacienteService:
    """Capa de lógica de negocio para la gestión de pacientes e historiales."""
@staticmethod
def id_valido(id_paciente):  # <--- Agrega 'def' aquí
    return isinstance(id_paciente, str) and len(id_paciente.strip()) > 0

    @staticmethod
    def registrar_paciente(db, id_paciente, nombre, edad, historial_inicial=""):
        if not PacienteService.id_valido(id_paciente):
            raise ValueError("El ID del paciente no es válido.")
        if id_paciente in db.pacientes:
            raise ValueError(f"El paciente con ID {id_paciente} ya se encuentra registrado.")
        
        db.pacientes[id_paciente] = {
            "nombre": nombre,
            "edad": edad,
            "historial": [historial_inicial] if historial_inicial else []
        }
        logging.info(f"Paciente {nombre} registrado exitosamente.")

    @staticmethod
    def agregar_historial(db, id_paciente, nota_medica):
        if id_paciente not in db.pacientes:
            raise KeyError("Paciente no encontrado en el sistema.")
        db.pacientes[id_paciente]["historial"].append(nota_medica)
        logging.info(f"Historial actualizado para el paciente ID: {id_paciente}")

class CitaService:
    """Capa de lógica de negocio para la programación y validación de agendas."""
    @staticmethod
    def programar_cita(db, id_paciente, doctor, horario):
        if id_paciente not in db.pacientes:
            raise KeyError("No se puede agendar cita: El paciente no existe.")
        
        # Validar cruce de horarios (Manejo de concurrencia y conflictos)
        for cita in db.citas:
            if cita["doctor"] == doctor and cita["horario"] == horario:
                raise ValueError(f"Conflicto de agenda: El doctor {doctor} ya tiene una cita a las {horario}.")
        
        nueva_cita = {"id_paciente": id_paciente, "doctor": doctor, "horario": horario, "estado": "Confirmada"}
        db.citas.append(nueva_cita)
        logging.info(f"Cita agendada con éxito para el Dr. {doctor} a las {horario}.")
        return nueva_cita


# =====================================================================
# EJERCICIO 2: Plataforma de Comercio E-Commerce Robustecida
# =====================================================================

class EcommerceDataLayer:
    """Capa de datos para inventario, usuarios y transacciones."""
    def __init__(self):
        self.catalogo = {
            "PROD01": {"nombre": "Laptop Pro", "precio": 1200.0, "stock": 5, "categoria": "Tecnología"},
            "PROD02": {"nombre": "Mouse Inalámbrico", "precio": 25.0, "stock": 20, "categoria": "Accesorios"}
        }
        self.usuarios = {}

class InventarioService:
    """Gestiona stock de productos con control de integridad transaccional."""
    @staticmethod
    def verificar_y_reservar(db, codigo_producto, cantidad):
        if codigo_producto not in db.catalogo:
            raise KeyError(f"El producto {codigo_producto} no existe en el catálogo.")
        
        prod = db.catalogo[codigo_producto]
        if prod["stock"] < cantidad:
            raise ValueError(f"Stock insuficiente para '{prod['nombre']}'. Disponibles: {prod['stock']}")
        
        # Transacción crítica de descuento de stock
        prod["stock"] -= cantidad
        logging.info(f"Inventario actualizado: -{cantidad} unidades de {prod['nombre']}. Stock restante: {prod['stock']}")
        return True

class CheckoutService:
    """Gestiona el procesamiento seguro de pagos y órdenes."""
    @staticmethod
    def procesar_pago_y_pedido(db, codigo_producto, cantidad, token_pago):
        # Simulación de verificación de seguridad en pasarela externa
        if not token_pago or token_pago != "TOKEN_SEGURO_VALIDO":
            raise PermissionError("Error de seguridad: Pago rechazado por la pasarela externa.")
        
        # Ejecución controlada con el servicio de inventario
        try:
            InventarioService.verificar_y_reservar(db, codigo_producto, cantidad)
            total = db.catalogo[codigo_producto]["precio"] * cantidad
            logging.info(f"Transacción completada exitosamente. Total cobrado: ${total:.2f}")
            return {"estado": "EXITO", "total": total}
        except Exception as e:
            logging.error(f"Fallo crítico en transacción de pago: {str(e)}")
            raise e


# =====================================================================
# BLOQUE DE PRUEBAS INTEGRALES (VERIFICACIÓN)
# =====================================================================
if __name__ == "__main__":
    print("=== EJECUCIÓN DE PRUEBAS DE CALIDAD E INGENIERÍA ===")
    
    # Prueba Ejercicio 1
    db_clinica = ClinicaDataLayer()
    try:
        PacienteService.registrar_paciente(db_clinica, "P001", "Esteban Quijia", 25, "Consulta inicial general")
        CitaService.programar_cita(db_clinica, "P001", "Dra. Gomez", "2026-06-10 10:00")
        # Intentar cruce de horario (Debe lanzar excepción controlada)
        CitaService.programar_cita(db_clinica, "P002", "Dra. Gomez", "2026-06-10 10:00")
    except Exception as e:
        print(f"[Ejecución Clínica - Excepción Capturada]: {e}")
        
    print("-" * 50)
    
    # Prueba Ejercicio 2
    db_shop = EcommerceDataLayer()
    try:
        # Intento de compra exitosa
        CheckoutService.procesar_pago_y_pedido(db_shop, "PROD01", 2, "TOKEN_SEGURO_VALIDO")
        # Intento de compra con stock excedido
        CheckoutService.procesar_pago_y_pedido(db_shop, "PROD01", 10, "TOKEN_SEGURO_VALIDO")
    except Exception as e:
        print(f"[Ejecución E-Commerce - Excepción Capturada]: {e}")