import uuid
import random
from datetime import datetime, timezone
from typing import Dict, Any

PRODUCTOS = [
    {"id": "PROD-001", "nombre": "Laptop Pro", "precio": 25000.0},
    {"id": "PROD-002", "nombre": "Monitor 4K", "precio": 8500.0},
    {"id": "PROD-003", "nombre": "Teclado Mec", "precio": 2200.0},
    {"id": "PROD-004", "nombre": "Mouse Inal",  "precio": 1500.0},
    {"id": "PROD-005", "nombre": "Webcam HD",   "precio": 3200.0},
]

CLIENTES = [f"CLI-{str(i).zfill(4)}" for i in range(1, 51)]

ESTATUS_PAGO = ["aprobado", "rechazado", "pendiente"]
ESTATUS_STOCK = ["disponible", "agotado", "reservado"]

def generar_evento_compra() -> Dict[str, Any]:
    """
    Simula un evento de compra desde al app movil
    """

    producto = random.choice(PRODUCTOS)
    cantidad = random.randint(1, 9)

    return {
        "id_venta": str(uuid.uuid4()),
        "id_cliente": random.choice(CLIENTES),
        "id_producto": producto["id"],
        "cantidad": cantidad,
        "monto": round(producto["precio"] * cantidad, 2),
        "ts": datetime.now(timezone.utc).isoformat(),
        "fuente": "app_movil"
    }

def generar_evento_pago() -> Dict[str, Any]:
    """Simula una confirmación de pago desde Stripe."""
    return {
        "id_pago":    str(uuid.uuid4()),
        "id_venta":   str(uuid.uuid4()),  # referencia a la venta
        "monto":      round(random.uniform(500, 30000), 2),
        "estatus":    random.choice(ESTATUS_PAGO),
        "ts":         datetime.now(timezone.utc).isoformat(),
        "fuente":     "stripe"
    }


def generar_evento_inventario() -> Dict[str, Any]:
    """Simula un cambio de inventario via CDC."""
    producto = random.choice(PRODUCTOS)
    return {
        "id_cambio":   str(uuid.uuid4()),
        "id_producto": producto["id"],
        "stock":       random.randint(0, 500),
        "estatus":     random.choice(ESTATUS_STOCK),
        "operacion":   random.choice(["INSERT", "UPDATE"]),  # CDC operation
        "ts":          datetime.now(timezone.utc).isoformat(),
        "fuente":      "inventario_cdc"
    }

def generar_batch(n: int = 100) -> Dict[str, list]:
    """
    Genera un batch de eventos mixtos de las 3 fuentes.
    Args:
        n: número total de eventos por generar

    Returns:
        Dict con eventos separados por fuente
    """

    compras = [generar_evento_compra() for _ in range(int(n * 0.6))]
    pagos = [generar_evento_pago() for _ in range(int(n * 0.3))]
    inventario = [generar_evento_inventario() for _ in range(int(n * 0.1))]

    return {
        "compras": compras,
        "pagos": pagos,
        "inventario": inventario,
        "total": len(compras) + len(pagos) + len(inventario)
    }
