import socket
import threading
import struct

PORT = 5555
MAX_PLAYERS = 15

# Speichert die Verbindungen: {player_id: conn_socket}
clients = {}
# Speichert die aktuellen Positionen: {player_id: (x, y)}
player_positions = {}

player_names = {}
game_started = False
host_id = 0

def send_lobby_update():

    player_count = len(clients)

    for pid, conn in clients.items():

        try:

            # Packet Typ 1
            conn.sendall(
                struct.pack(
                    "!BBB",
                    1,
                    player_count,
                    host_id
                )
            )

            for other_id, pname in player_names.items():

                name_bytes = pname.encode()

                conn.sendall(
                    struct.pack(
                        f"!BB{len(name_bytes)}s",
                        other_id,
                        len(name_bytes),
                        name_bytes
                    )
                )

        except:
            pass

def broadcast_to_all(data, exclude_id = None):
    """Sendet Daten an alle verbundenen Spieler."""
    for player_id, conn in list(clients.items()):
        if player_id != exclude_id:
            try:
                conn.sendall(data)
            except:
                disconnect_client(player_id)

def disconnect_client(player_id):
    """Entfernt einen Spieler, wenn er das Spiel verlässt."""
    if player_id in clients:
        print(f"Spieler {player_id} hat die Verbindung verloren.")
        clients[player_id].close()
        del clients[player_id]
    if player_id in player_positions:
        del player_positions[player_id]
        # Ein "Disconnect-Paket" an alle senden (z.B. X und Y auf -1000 setzen)
        disconnect_packet = struct.pack('!BBii', 2, player_id, -1000, -1000)
        broadcast_to_all(disconnect_packet)

    send_lobby_update()

def handle_client(conn, player_id):
    global player_positions
    print(f"Thread für Spieler {player_id} gestartet.")
    
    # Aktiviert TCP_NODELAY für minimale Verzögerung
    conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    while True:
        try:
            packet_type = struct.unpack("!B", conn.recv(1))[0]
            # =========================
            # SPIEL STARTEN
            # =========================
            if packet_type == 99:
                if player_id == host_id:
                    print("Spiel gestartet!")
                    broadcast_to_all(struct.pack("!B", 3))

            # =========================
            # POSITIONSDATEN
            # =========================
            elif packet_type == 2:
                data = b""

                while len(data) < 8:
                    packet = conn.recv(8 - len(data))

                    if not packet:
                        break

                    data += packet

                if len(data) < 8:
                    break

                x, y = struct.unpack("!ii", data)
                player_positions[player_id] = (x, y)
                update_packet = struct.pack("!BBii", 2, player_id, x, y)
                broadcast_to_all(update_packet, exclude_id = player_id)

        except:
            break

    disconnect_client(player_id)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Lokale IP ermitteln
    temp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        temp.connect(("8.8.8.8", 80))
        host_ip = temp.getsockname()[0]
    finally:
        temp.close()

    server.bind((host_ip, PORT))
    server.listen(MAX_PLAYERS)
    print(f"Zentraler Server gestartet auf IP: {host_ip} : {PORT}")

    player_id_counter = 0

    while True:
        conn, addr = server.accept()

        if len(clients) >= MAX_PLAYERS:
            conn.close() # Server voll
            continue

        print(f"Neuer Spieler verbunden von: {addr} -> Erhält ID: {player_id_counter}")

        # Namen empfangen
        name_length = struct.unpack("!B", conn.recv(1))[0]
        player_name = conn.recv(name_length).decode()

        player_names[player_id_counter] = player_name
        
        # 1. Dem Client seine eigene ID schicken, damit er weiß, wer er ist
        conn.sendall(struct.pack('!B', player_id_counter))
        
        # 2. Dem neuen Client die Positionen aller bereits existierenden Spieler schicken
        for existing_id, pos in player_positions.items():
            conn.sendall(struct.pack('!Bii', existing_id, pos[0], pos[1]))

        clients[player_id_counter] = conn
        send_lobby_update()
        
        # Thread für diesen Spieler starten
        threading.Thread(target = handle_client, args = (conn, player_id_counter), daemon = True).start()
        player_id_counter += 1

if __name__ == "__main__":
    start_server()