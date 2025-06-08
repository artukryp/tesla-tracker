import teslapy
import telepot
from geopy.distance import geodesic
import config
import json
import os

print("🚗 Iniciando script Tesla-Tracker...")

def guardar_token(token):
    with open('token.json', 'w') as f:
        json.dump(token, f)
    print("🔒 Token guardado en 'token.json'.")

def cargar_token():
    if os.path.exists('token.json'):
        with open('token.json', 'r') as f:
            print("🔓 Token cargado desde 'token.json'.")
            return json.load(f)
    print("⚠️ No se encontró token guardado.")
    return None

token = cargar_token()

tesla = teslapy.Tesla(config.TESLA_EMAIL)
if token:
    tesla.token = token
else:
    print("🔐 No hay token previo, se requiere autenticación.")

with tesla:
    if not tesla.authorized:
        print("🔐 Autenticación necesaria. Abre la siguiente URL:")
        print(tesla.authorization_url())
        url_final = input("Pega la URL final después de iniciar sesión y 2FA: ")
        tesla.fetch_token(authorization_response=url_final)
        guardar_token(tesla.token)

    print("📡 Accediendo a lista de vehículos...")
    vehicles = tesla.vehicle_list()
    if not vehicles:
        print("⚠️ No se encontró ningún vehículo.")
        exit()

    vehicle = vehicles[0]
    print(f"🚙 Vehículo: {vehicle['display_name']}")

    print("🔍 Obteniendo datos...")
    vehicle_data = vehicle.get_vehicle_data()
    drive_state = vehicle_data['drive_state']

    lat = drive_state.get('latitude')
    lon = drive_state.get('longitude')

    if lat is None or lon is None:
        print("⚠️ No se pudo obtener la ubicación.")
        exit()

    print(f"📍 Ubicación actual: ({lat}, {lon})")
    distancia = geodesic(config.ZONA_PERMITIDA, (lat, lon)).km
    print(f"📏 Distancia desde zona permitida: {distancia:.2f} km")

    if distancia > config.RADIO_MAX_KM:
        print("🚨 Fuera de zona permitida. Enviando alerta...")

        km_recorridos = vehicle_data['vehicle_state']['odometer']
        mensaje = f"""*🚨 Uso de vehículo fuera de ubicación permitida*

*Kilómetros recorridos:* {km_recorridos:.1f} km  
*Distancia fuera de zona:* {distancia:.2f} km  
*Ubicación actual:* [{lat}, {lon}]  
[Ver en mapa](https://www.google.com/maps/search/?api=1&query={lat},{lon})
"""
        bot = telepot.Bot(config.TOKEN)
        bot.sendMessage(config.CHAT_ID, mensaje, parse_mode="Markdown")
        print("✅ Mensaje enviado.")
    else:
        print("✅ Vehículo dentro de zona. No se envía alerta.")
