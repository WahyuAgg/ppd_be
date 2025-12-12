# routes.py - Script untuk melihat daftar semua endpoint
from app.main import app

print("\n" + "="*80)
print("DAFTAR SEMUA ENDPOINTS")
print("="*80)
print(f"{'METHOD':<12} {'PATH':<40} {'NAME'}")
print("-"*80)

for route in app.routes:
    if hasattr(route, "methods"):
        methods = ", ".join(sorted(route.methods - {"HEAD", "OPTIONS"}))
        print(f"{methods:<12} {route.path:<40} {route.name or '-'}")

print("="*80 + "\n")
