from core.utils import success_response, error_response
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

MOCK_ERP = {
    "orders": [
        {"id": "ORD-001", "supplier": "PT Baja Nusantara", "material": "Steel Sheet",
         "qty": 500, "unit": "kg", "status": "Pending", "eta": "2026-04-01"},
        {"id": "ORD-002", "supplier": "CV Alumindo", "material": "Aluminum",
         "qty": 1000, "unit": "kg", "status": "Shipped", "eta": "2026-03-28"},
        {"id": "ORD-003", "supplier": "PT Kawat Mas", "material": "Copper Wire",
         "qty": 200, "unit": "meter", "status": "Delivered", "eta": "2026-03-20"},
    ],
    "customers": [
        {"id": "CUST-01", "name": "PT Astra Manufacturing", "pending_orders": 3,
         "value": "Rp 450.000.000", "status": "Active"},
        {"id": "CUST-02", "name": "CV Maju Jaya", "pending_orders": 1,
         "value": "Rp 120.000.000", "status": "Active"},
    ],
    "suppliers": [
        {"id": "SUP-01", "name": "PT Baja Nusantara", "rating": 4.5, "on_time_delivery": "92%"},
        {"id": "SUP-02", "name": "CV Alumindo", "rating": 4.2, "on_time_delivery": "88%"},
    ]
}

def query_erp(query_type: str, status_filter: str = None) -> dict:
    """Query ERP system for orders, customers, suppliers."""
    if query_type not in MOCK_ERP:
        return error_response(f"Unknown query type: {query_type}. Use: orders, customers, suppliers")
    data = MOCK_ERP[query_type]
    if status_filter:
        data = [d for d in data if d.get("status", "").lower() == status_filter.lower()]
    return success_response(data, len(data))