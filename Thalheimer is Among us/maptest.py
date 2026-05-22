import pygame
import json
import sys
import os

# -- KONSTANTEN --
TILE_SIZE = 24
TILES_VISIBLE = 15
INTERNAL_SIZE = TILE_SIZE * TILES_VISIBLE  # 360x360 Pixel
PLAYER_SPEED = 3

class Player:
    def __init__(self, x, y):
        # Der Spieler ist genau 1 Tile (24x24 px) groß
        self.rect = pygame.Rect(x, y, TILE_SIZE*0.6, TILE_SIZE*0.6)
        self.color = (255, 50, 50) # Rotes Quadrat als Platzhalter für den Spieler
        self.image = pygame.image.load("Assets/Character/All_colors/banana.png")
        self.image = pygame.transform.scale(self.image, (TILE_SIZE*0.6, TILE_SIZE*0.6))

    def move(self, dx, dy, hitboxes):
        # X-Achse bewegen und auf Kollision prüfen
        self.rect.x += dx
        for box in hitboxes:
            if self.rect.colliderect(box):
                if dx > 0: # Rechtsbewegung
                    self.rect.right = box.left
                if dx < 0: # Linksbewegung
                    self.rect.left = box.right

        # Y-Achse bewegen und auf Kollision prüfen
        self.rect.y += dy
        for box in hitboxes:
            if self.rect.colliderect(box):
                if dy > 0: # Abwärtsbewegung
                    self.rect.bottom = box.top
                if dy < 0: # Aufwärtsbewegung
                    self.rect.top = box.bottom

    def draw(self, surface, camera_x, camera_y):
        draw_rect = self.rect.copy()
        draw_rect.x -= camera_x
        draw_rect.y -= camera_y

        surface.blit(self.image, (draw_rect.x, draw_rect.y))

def load_hitboxes(filepath):
    hitboxes = []
    vents = []
    if not os.path.exists(filepath):
        print(f"WARNUNG: Hitbox-Datei nicht gefunden: {filepath}")
        return hitboxes
    
    with open(filepath, "r", encoding="utf-8-sig") as f:
        map_data = json.load(f)
    
    # Map-Breite auslesen (Standard 100, falls nicht angegeben)
    map_width = map_data.get("width", 100)

    # Alle Schichten (Layers) durchsuchen
    for layer in map_data.get("layers", []):
        if layer.get("name") in ["Hitbox", "ObjectsHitbox"]:
            # 1. Fall: Hitboxen sind als Tiled-Objekte definiert
            if "objects" in layer:
                for obj in layer["objects"]:
                    hitboxes.append(pygame.Rect(obj["x"], obj["y"], obj["width"], obj["height"]))
            
            # 2. Fall: Hitboxen sind als normale Tile-Ebene gemalt[cite: 1]
            elif "data" in layer:
                for i, tile_id in enumerate(layer["data"]):
                    if tile_id != 0: # 0 bedeutet leeres Tile
                        x = (i % map_width) * TILE_SIZE
                        y = (i // map_width) * TILE_SIZE
                        hitboxes.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))

        elif layer.get("name") == "VentsHitbox":

            if "objects" in layer:
                for obj in layer["objects"]:
                    vents.append(
                        pygame.Rect(
                            obj["x"],
                            obj["y"],
                            obj["width"],
                            obj["height"]
                        )
                    )
    
    return hitboxes, vents

def get_current_vent(player, vents):
    for vent in vents:
        if player.rect.colliderect(vent):
            return vent
    return None

def main():
    pygame.init()

    # Vollbild-Setup
    screen_info = pygame.display.Info()
    screen_width, screen_height = screen_info.current_w, screen_info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    pygame.display.set_caption("Top-Down Map Explorer")

    # Interne Zeichenfläche (360x360)
    internal_surface = pygame.Surface((INTERNAL_SIZE, INTERNAL_SIZE))

    # Bilder laden
    base_path = "Assets/Map/Map/"
    try:
        floor_img = pygame.image.load(os.path.join(base_path, "Floor.png")).convert_alpha()
        walls_img = pygame.image.load(os.path.join(base_path, "Walls.png")).convert_alpha()
        objects_img = pygame.image.load(os.path.join(base_path, "Objects.png")).convert_alpha()
    except Exception as e:
        print(f"Fehler beim Laden der Bilder: {e}")
        pygame.quit()
        sys.exit()

    # Hitboxen laden
    hitboxes, vents = load_hitboxes(
        os.path.join(base_path, "Hitboxes.json")
    )

    # Spieler instanziieren (Startposition z.B. 100, 100)
    player = Player(100, 100)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # Mit ESC das Vollbild beenden
                    running = False
                if event.key == pygame.K_SPACE:

                    current_vent = get_current_vent(player, vents)

                    if current_vent:

                        current_index = vents.index(current_vent)

                        # Nächsten Vent auswählen
                        next_index = (current_index + 1) % len(vents)

                        next_vent = vents[next_index]

                        # Spieler in Mitte des Zielvents setzen
                        player.rect.center = next_vent.center

        # Eingaben verarbeiten
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:    dy -= PLAYER_SPEED
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:  dy += PLAYER_SPEED
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  dx -= PLAYER_SPEED
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dx += PLAYER_SPEED

        # Spieler bewegen
        if dx != 0 or dy != 0:
            # Diagonalbewegung normalisieren (damit man nicht schneller läuft)
            if dx != 0 and dy != 0:
                dx *= 0.7071
                dy *= 0.7071
            player.move(dx, dy, hitboxes)

        # Kamera-Position berechnen (Spieler zentrieren)
        camera_x = player.rect.x - (INTERNAL_SIZE // 2) + (TILE_SIZE // 2)
        camera_y = player.rect.y - (INTERNAL_SIZE // 2) + (TILE_SIZE // 2)

        # Rendering auf der internen Surface
        internal_surface.fill((40, 40, 40)) # Schwarz als Hintergrund
        
        # Map-Bilder zeichnen
        internal_surface.blit(floor_img, (-camera_x, -camera_y))
        internal_surface.blit(walls_img, (-camera_x, -camera_y))
        internal_surface.blit(objects_img, (-camera_x, -camera_y))

        # Spieler zeichnen
        player.draw(internal_surface, camera_x, camera_y)

        # Interne Surface auf Vollbildgröße skalieren
        # Um das Seitenverhältnis von 1:1 beizubehalten, nutzen wir die Höhe des Bildschirms für beide Seiten
        # und zentrieren es horizontal, falls der Bildschirm breiter ist (Widescreen).
        scaled_size = min(screen_width, screen_height)
        scaled_surface = pygame.transform.scale(internal_surface, (scaled_size, scaled_size))
        
        # Berechnen, wo das zentrierte quadratische Bild platziert werden soll
        draw_x = (screen_width - scaled_size) // 2
        draw_y = (screen_height - scaled_size) // 2

        # Auf den tatsächlichen Bildschirm zeichnen
        screen.fill((40, 40, 40)) # Balken links und rechts abdunkeln
        screen.blit(scaled_surface, (draw_x, draw_y))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()