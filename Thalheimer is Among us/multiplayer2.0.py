import pygame
import socket
import threading
import struct
import random

# =========================
# Einstellungen
# =========================
PLAYER_SIZE = 50
SPEED = 300
PORT = 5555

pygame.init()

screen_width, screen_height = 1200, 900
screen = pygame.display.set_mode((screen_width, screen_height))
WIDTH = screen.get_width()
HEIGHT = screen.get_height()

pygame.display.set_caption("WLAN Multiplayer")

clock = pygame.time.Clock()

# =========================
# Bilder laden
# =========================
player1_image = pygame.image.load(
    "Thalheimer is Among us/Assets/Character/All_colors/lime.png"
).convert_alpha()

player1_image = pygame.transform.scale(
    player1_image,
    (PLAYER_SIZE, PLAYER_SIZE)
)

player2_image = pygame.image.load(
    "Thalheimer is Among us/Assets/Character/All_colors/banana.png"
).convert_alpha()

player2_image = pygame.transform.scale(
    player2_image,
    (PLAYER_SIZE, PLAYER_SIZE)
)

# =========================
# Tasks
# =========================
class TaskManager:
    def __init__(self):
        self.tasks = []
        self.active_task = None
        self.message = ""
        self.message_timer = 0

    def add_task(self, task):
        self.tasks.append(task)

    def start_task(self, index):
        if 0 <= index < len(self.tasks):
            self.active_task = self.tasks[index]

    def show_message(self, text, duration=120):
        self.message = text
        self.message_timer = duration

    def handle_event(self, event):
        if self.active_task:
            self.active_task.handle_event(event)

    def update(self):

        # Task Update aufrufen
        if self.active_task and hasattr(self.active_task, "update"):
            self.active_task.update()

        # Prüfen ob fertig
        if self.active_task and self.active_task.is_finished():
            self.active_task = None

        if self.message_timer > 0:
            self.message_timer -= 1

    def draw(self, surface):
        if self.active_task:
            self.active_task.draw()

        if self.message_timer > 0:
            font = pygame.font.SysFont("arial", 40)

            text = font.render(self.message, True, (255, 80, 80))

            surface.blit(text, (WIDTH // 2 - text.get_width() // 2, 40))

class BookSortTask:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()

        # =========================
        # TASK WINDOW
        # =========================

        self.window_width = 1100
        self.window_height = 700

        # Fenster mittig
        self.window_x = (self.screen_width - self.window_width) // 2
        self.window_y = (self.screen_height - self.window_height) // 2

        # Task Bildschirm
        self.task_rect = pygame.Rect(
            self.window_x,
            self.window_y,
            self.window_width,
            self.window_height
        )

        # =========================
        # FARBEN
        # =========================

        self.WHITE = (240, 240, 240)
        self.BLACK = (20, 20, 20)
        self.GREEN = (0, 200, 0)
        self.RED = (200, 50, 50)
        self.BLUE = (80, 120, 255)
        self.YELLOW = (255, 220, 0)
        self.BROWN = (120, 80, 40)
        self.PURPLE = (171, 0, 255)

        # =========================
        # SCHRIFT
        # =========================

        self.font = pygame.font.SysFont("arial", 40)
        self.big_font = pygame.font.SysFont("arial", 70)

        # =========================
        # REGALE
        # =========================

        self.left_shelf = pygame.Rect(
            self.window_x + 120,
            self.window_y + 190,
            300,
            400
        )

        self.right_shelf = pygame.Rect(
            self.window_x + 680,
            self.window_y + 190,
            300,
            400
        )

        # =========================
        # BÜCHER
        # =========================

        self.books = []
        self.create_books()

        # =========================
        # DRAG & DROP
        # =========================

        self.selected_book = None
        self.offset_x = 0
        self.offset_y = 0

        # =========================
        # STATUS
        # =========================

        self.finished = False

    def create_books(self):

        colors = [
            self.RED,
            self.BLUE,
            self.GREEN,
            self.YELLOW,
            self.BROWN,
            self.PURPLE
        ]

        for i in range(len(colors)):

            rect = pygame.Rect(
                random.randint(
                    self.left_shelf.x + 30,
                    self.left_shelf.x + 180
                ),

                random.randint(
                    self.left_shelf.y + 30,
                    self.left_shelf.y + 250
                ),

                80,
                110
            )

            self.books.append({
                "rect": rect,
                "color": colors[i]
            })

    def draw(self):

        # Hintergrund
        self.screen.fill((20, 20, 30))

        # =========================
        # TASK WINDOW
        # =========================

        pygame.draw.rect(
            self.screen,
            self.WHITE,
            self.task_rect,
            border_radius=20
        )

        # Schwarzer Rand
        pygame.draw.rect(
            self.screen,
            self.BLACK,
            self.task_rect,
            width=5,
            border_radius=20
        )

        # =========================
        # TITEL
        # =========================

        title = self.big_font.render(
            "SORT BOOKS",
            True,
            self.BLACK
        )

        self.screen.blit(
            title,
            (
                self.window_x + 340,
                self.window_y + 20
            )
        )

        info = self.font.render(
            "Ziehe alle Bücher ins rechte Regal",
            True,
            self.BLACK
        )

        self.screen.blit(
            info,
            (
                self.window_x + 250,
                self.window_y + 90
            )
        )

        # =========================
        # REGALE
        # =========================

        pygame.draw.rect(
            self.screen,
            self.BROWN,
            self.left_shelf,
            8
        )

        pygame.draw.rect(
            self.screen,
            self.BROWN,
            self.right_shelf,
            8
        )

        # Regal Texte

        left_text = self.font.render(
            "UNSORTIERT",
            True,
            self.BLACK
        )

        right_text = self.font.render(
            "SORTIERT",
            True,
            self.BLACK
        )

        self.screen.blit(
            left_text,
            (
                self.left_shelf.x + 40,
                self.left_shelf.y - 50
            )
        )

        self.screen.blit(
            right_text,
            (
                self.right_shelf.x + 70,
                self.right_shelf.y - 50
            )
        )

        # =========================
        # BÜCHER
        # =========================

        for book in self.books:

            pygame.draw.rect(
                self.screen,
                book["color"],
                book["rect"],
                border_radius=8
            )

            pygame.draw.rect(
                self.screen,
                self.BLACK,
                book["rect"],
                width=3,
                border_radius=8
            )

        # =========================
        # TASK FINISHED
        # =========================

        if self.finished:

            finished = self.big_font.render(
                "TASK FINISHED",
                True,
                self.GREEN
            )

            self.screen.blit(
                finished,
                (
                    self.window_x + 250,
                    self.window_y + 300
                )
            )

    def handle_event(self, event):

        if self.finished:
            return

        # =========================
        # MAUS KLICK
        # =========================

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_pos = pygame.mouse.get_pos()

            for book in reversed(self.books):

                if book["rect"].collidepoint(mouse_pos):

                    self.selected_book = book

                    self.offset_x = (
                        book["rect"].x - mouse_pos[0]
                    )

                    self.offset_y = (
                        book["rect"].y - mouse_pos[1]
                    )

                    break

        # =========================
        # BUCH BEWEGEN
        # =========================

        elif event.type == pygame.MOUSEMOTION:

            if self.selected_book:

                mouse_pos = pygame.mouse.get_pos()

                self.selected_book["rect"].x = (
                    mouse_pos[0] + self.offset_x
                )

                self.selected_book["rect"].y = (
                    mouse_pos[1] + self.offset_y
                )

        # =========================
        # LOSLASSEN
        # =========================

        elif event.type == pygame.MOUSEBUTTONUP:

            self.selected_book = None
            self.check_finished()

    def check_finished(self):

        all_correct = True

        for book in self.books:

            if not self.right_shelf.contains(book["rect"]):
                all_correct = False

        if all_correct:
            self.finished = True

    def is_finished(self):
        return self.finished

class ChairStackTask:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()

        # =========================
        # TASK WINDOW
        # =========================

        self.window_width = 1200
        self.window_height = 750

        self.window_x = (self.screen_width - self.window_width) // 2
        self.window_y = (self.screen_height - self.window_height) // 2

        self.task_rect = pygame.Rect(
            self.window_x,
            self.window_y,
            self.window_width,
            self.window_height
        )

        # =========================
        # FARBEN
        # =========================

        self.WHITE = (240, 240, 240)
        self.BLACK = (20, 20, 20)
        self.BROWN = (120, 80, 40)
        self.LIGHT_BROWN = (170, 120, 70)
        self.BLUE = (80, 120, 255)
        self.GREEN = (0, 200, 0)
        self.RED = (200, 50, 50)

        # =========================
        # SCHRIFT
        # =========================

        self.font = pygame.font.SysFont("arial", 36)
        self.big_font = pygame.font.SysFont("arial", 65)

        # =========================
        # TISCHE
        # =========================

        self.tables = []

        self.create_tables()

        # =========================
        # STÜHLE
        # =========================

        self.chairs = []

        self.create_chairs()

        # =========================
        # DRAG & DROP
        # =========================

        self.selected_chair = None

        self.offset_x = 0
        self.offset_y = 0

        # =========================
        # STATUS
        # =========================

        self.finished = False

    def create_tables(self):

        # 4 bis 6 Tische
        self.table_count = random.randint(4, 6)

        spacing = 170

        start_x = self.window_x + 120
        y = self.window_y + 320

        for i in range(self.table_count):

            table_rect = pygame.Rect(
                start_x + i * spacing,
                y,
                120,
                80
            )

            self.tables.append({
                "rect": table_rect,
                "occupied": False
            })

    def create_chairs(self):

        for i in range(self.table_count):

            chair_rect = pygame.Rect(
                random.randint(
                    self.window_x + 80,
                    self.window_x + 950
                ),

                random.randint(
                    self.window_y + 470,
                    self.window_y + 580
                ),

                60,
                60
            )

            self.chairs.append({
                "rect": chair_rect,
                "placed": False
            })

    def draw(self):

        # Hintergrund
        self.screen.fill((25, 25, 35))

        # =========================
        # TASK WINDOW
        # =========================

        pygame.draw.rect(
            self.screen,
            self.WHITE,
            self.task_rect,
            border_radius=20
        )

        pygame.draw.rect(
            self.screen,
            self.BLACK,
            self.task_rect,
            width=5,
            border_radius=20
        )

        # =========================
        # TITEL
        # =========================

        title = self.big_font.render(
            "STACK CHAIRS",
            True,
            self.BLACK
        )

        self.screen.blit(
            title,
            (
                self.window_x + 320,
                self.window_y + 20
            )
        )

        info = self.font.render(
            "Stelle alle Stühle auf die Tische",
            True,
            self.BLACK
        )

        self.screen.blit(
            info,
            (
                self.window_x + 320,
                self.window_y + 100
            )
        )

        # =========================
        # TISCHE ZEICHNEN
        # =========================

        for table in self.tables:

            rect = table["rect"]

            # Tischplatte
            pygame.draw.rect(
                self.screen,
                self.BROWN,
                rect,
                border_radius=10
            )

            pygame.draw.rect(
                self.screen,
                self.BLACK,
                rect,
                width=4,
                border_radius=10
            )

            # Tischbeine
            leg_width = 12
            leg_height = 60

            pygame.draw.rect(
                self.screen,
                self.LIGHT_BROWN,
                (
                    rect.x + 10,
                    rect.y + rect.height,
                    leg_width,
                    leg_height
                )
            )

            pygame.draw.rect(
                self.screen,
                self.LIGHT_BROWN,
                (
                    rect.x + rect.width - 22,
                    rect.y + rect.height,
                    leg_width,
                    leg_height
                )
            )

        # =========================
        # STÜHLE ZEICHNEN
        # =========================

        for chair in self.chairs:

            rect = chair["rect"]

            # Sitzfläche
            pygame.draw.rect(
                self.screen,
                self.BLUE,
                rect,
                border_radius=8
            )

            pygame.draw.rect(
                self.screen,
                self.BLACK,
                rect,
                width=3,
                border_radius=8
            )

            # Lehne
            pygame.draw.rect(
                self.screen,
                self.BLUE,
                (
                    rect.x + 10,
                    rect.y - 20,
                    40,
                    20
                ),
                border_radius=5
            )

        # =========================
        # FERTIG
        # =========================

        if self.finished:

            finished_text = self.big_font.render(
                "TASK FINISHED",
                True,
                self.GREEN
            )

            self.screen.blit(
                finished_text,
                (
                    self.window_x + 260,
                    self.window_y + 620
                )
            )

    def handle_event(self, event):

        if self.finished:
            return

        # =========================
        # MAUSKLICK
        # =========================

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_pos = pygame.mouse.get_pos()

            for chair in reversed(self.chairs):

                if chair["rect"].collidepoint(mouse_pos):

                    self.selected_chair = chair

                    self.offset_x = (
                        chair["rect"].x - mouse_pos[0]
                    )

                    self.offset_y = (
                        chair["rect"].y - mouse_pos[1]
                    )

                    break

        # =========================
        # STUHL BEWEGEN
        # =========================

        elif event.type == pygame.MOUSEMOTION:

            if self.selected_chair:

                mouse_pos = pygame.mouse.get_pos()

                self.selected_chair["rect"].x = (
                    mouse_pos[0] + self.offset_x
                )

                self.selected_chair["rect"].y = (
                    mouse_pos[1] + self.offset_y
                )

        # =========================
        # LOSLASSEN
        # =========================

        elif event.type == pygame.MOUSEBUTTONUP:

            if self.selected_chair:

                self.snap_chair_to_table(
                    self.selected_chair
                )

            self.selected_chair = None

            self.check_finished()

    def snap_chair_to_table(self, chair):

        for table in self.tables:

            table_rect = table["rect"]

            # Prüfen ob Stuhl auf Tisch
            if table_rect.colliderect(chair["rect"]):

                # Nur wenn Tisch frei
                if not table["occupied"]:

                    chair["rect"].centerx = table_rect.centerx
                    chair["rect"].bottom = table_rect.top + 25

                    chair["placed"] = True
                    table["occupied"] = True

                    return

    def check_finished(self):

        all_done = True

        for chair in self.chairs:

            if not chair["placed"]:
                all_done = False

        if all_done:
            self.finished = True

    def is_finished(self):
        return self.finished

class WindowTask:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()

        # =========================
        # TASK WINDOW
        # =========================

        self.window_width = 1200
        self.window_height = 750

        self.window_x = (
            self.screen_width - self.window_width
        ) // 2

        self.window_y = (
            self.screen_height - self.window_height
        ) // 2

        self.task_rect = pygame.Rect(
            self.window_x,
            self.window_y,
            self.window_width,
            self.window_height
        )

        # =========================
        # FARBEN
        # =========================

        self.WHITE = (240, 240, 240)
        self.BLACK = (20, 20, 20)
        self.BLUE = (120, 180, 255)
        self.GRAY = (120, 120, 120)
        self.DARK_GRAY = (70, 70, 70)
        self.BROWN = (120, 80, 40)
        self.GREEN = (0, 200, 0)
        self.RED = (200, 50, 50)
        self.YELLOW = (255, 220, 0)

        # =========================
        # SCHRIFT
        # =========================

        self.font = pygame.font.SysFont("arial", 38)
        self.big_font = pygame.font.SysFont("arial", 65)

        # =========================
        # MODUS
        # =========================

        # True = Fenster öffnen
        # False = Fenster schließen

        self.must_open = random.choice([True, False])

        # =========================
        # FENSTER
        # =========================

        self.windows = []

        self.create_windows()

        # =========================
        # STATUS
        # =========================

        self.finished = False

    def create_windows(self):

        start_x = self.window_x + 120
        start_y = self.window_y + 180

        spacing_x = 260
        spacing_y = 220

        for row in range(2):

            for col in range(3):

                rect = pygame.Rect(
                    start_x + col * spacing_x,
                    start_y + row * spacing_y,
                    160,
                    140
                )

                # Zufälliger Zustand
                opened = random.choice([True, False])

                self.windows.append({
                    "rect": rect,
                    "open": opened
                })

    def draw(self):

        # Hintergrund
        self.screen.fill((25, 25, 35))

        # =========================
        # TASK WINDOW
        # =========================

        pygame.draw.rect(
            self.screen,
            self.WHITE,
            self.task_rect,
            border_radius=20
        )

        pygame.draw.rect(
            self.screen,
            self.BLACK,
            self.task_rect,
            width=5,
            border_radius=20
        )

        # =========================
        # TITEL
        # =========================

        title = self.big_font.render(
            "WINDOW TASK",
            True,
            self.BLACK
        )

        self.screen.blit(
            title,
            (
                self.window_x + 320,
                self.window_y + 20
            )
        )

        # =========================
        # AUFGABE
        # =========================

        if self.must_open:

            task_text = "Öffne alle Fenster"

        else:

            task_text = "Schließe alle Fenster"

        info = self.font.render(
            task_text,
            True,
            self.BLACK
        )

        self.screen.blit(
            info,
            (
                self.window_x + 370,
                self.window_y + 100
            )
        )

        # =========================
        # FENSTER ZEICHNEN
        # =========================

        for window in self.windows:

            rect = window["rect"]

            # Rahmen
            pygame.draw.rect(
                self.screen,
                self.BROWN,
                rect,
                border_radius=8
            )

            pygame.draw.rect(
                self.screen,
                self.BLACK,
                rect,
                width=4,
                border_radius=8
            )

            # Zustand
            if window["open"]:

                # Geöffnet
                pygame.draw.rect(
                    self.screen,
                    self.BLUE,
                    (
                        rect.x + 15,
                        rect.y + 15,
                        rect.width - 30,
                        rect.height - 30
                    ),
                    border_radius=5
                )

                # Offener Flügel
                pygame.draw.line(
                    self.screen,
                    self.DARK_GRAY,
                    (
                        rect.centerx,
                        rect.y + 15
                    ),
                    (
                        rect.right - 20,
                        rect.bottom - 20
                    ),
                    6
                )

                state_text = self.font.render(
                    "OFFEN",
                    True,
                    self.GREEN
                )

            else:

                # Geschlossen
                pygame.draw.rect(
                    self.screen,
                    self.GRAY,
                    (
                        rect.x + 15,
                        rect.y + 15,
                        rect.width - 30,
                        rect.height - 30
                    ),
                    border_radius=5
                )

                # Kreuz
                pygame.draw.line(
                    self.screen,
                    self.DARK_GRAY,
                    (
                        rect.centerx,
                        rect.y + 15
                    ),
                    (
                        rect.centerx,
                        rect.bottom - 15
                    ),
                    5
                )

                pygame.draw.line(
                    self.screen,
                    self.DARK_GRAY,
                    (
                        rect.x + 15,
                        rect.centery
                    ),
                    (
                        rect.right - 15,
                        rect.centery
                    ),
                    5
                )

                state_text = self.font.render(
                    "ZU",
                    True,
                    self.RED
                )

            self.screen.blit(
                state_text,
                (
                    rect.x + 35,
                    rect.y + 150
                )
            )

        # =========================
        # TASK FINISHED
        # =========================

        if self.finished:

            finished = self.big_font.render(
                "TASK FINISHED",
                True,
                self.GREEN
            )

            self.screen.blit(
                finished,
                (
                    self.window_x + 260,
                    self.window_y + 650
                )
            )

    def handle_event(self, event):

        if self.finished:
            return

        # =========================
        # MAUSKLICK
        # =========================

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_pos = pygame.mouse.get_pos()

            for window in self.windows:

                if window["rect"].collidepoint(mouse_pos):

                    # Zustand wechseln
                    window["open"] = not window["open"]

                    self.check_finished()

                    break

    def check_finished(self):

        all_correct = True

        for window in self.windows:

            # Alle müssen offen sein
            if self.must_open:

                if not window["open"]:
                    all_correct = False

            # Alle müssen geschlossen sein
            else:

                if window["open"]:
                    all_correct = False

        if all_correct:
            self.finished = True

    def is_finished(self):
        return self.finished

class CleanBoardTask:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()

        # =========================
        # TASK WINDOW
        # =========================

        self.window_width = 1200
        self.window_height = 750

        self.window_x = (
            self.screen_width - self.window_width
        ) // 2

        self.window_y = (
            self.screen_height - self.window_height
        ) // 2

        self.task_rect = pygame.Rect(
            self.window_x,
            self.window_y,
            self.window_width,
            self.window_height
        )

        # =========================
        # FARBEN
        # =========================

        self.WHITE = (240, 240, 240)
        self.BLACK = (20, 20, 20)
        self.GREEN = (0, 200, 0)
        self.BROWN = (120, 80, 40)
        self.BOARD_GREEN = (40, 100, 40)
        self.CHALK = (230, 230, 230)
        self.YELLOW = (255, 220, 0)

        # =========================
        # SCHRIFT
        # =========================

        self.font = pygame.font.SysFont("arial", 36)
        self.big_font = pygame.font.SysFont("arial", 65)

        # =========================
        # TAFEL
        # =========================

        self.board_rect = pygame.Rect(
            self.window_x + 180,
            self.window_y + 170,
            820,
            420
        )

        # =========================
        # SCHMUTZ / KREIDE
        # =========================

        self.dirt_spots = []

        self.create_dirt()

        # =========================
        # SCHWAMM
        # =========================

        self.sponge_rect = pygame.Rect(
            self.window_x + 520,
            self.window_y + 620,
            140,
            60
        )

        self.cleaning = False

        # =========================
        # STATUS
        # =========================

        self.finished = False

    def create_dirt(self):

        for i in range(40):

            x = random.randint(
                self.board_rect.x + 20,
                self.board_rect.right - 20
            )

            y = random.randint(
                self.board_rect.y + 20,
                self.board_rect.bottom - 20
            )

            radius = random.randint(10, 22)

            self.dirt_spots.append({
                "x": x,
                "y": y,
                "radius": radius
            })

    def draw(self):

        # Hintergrund
        self.screen.fill((25, 25, 35))

        # =========================
        # TASK WINDOW
        # =========================

        pygame.draw.rect(
            self.screen,
            self.WHITE,
            self.task_rect,
            border_radius = 20
        )

        pygame.draw.rect(
            self.screen,
            self.BLACK,
            self.task_rect,
            width = 5,
            border_radius = 20
        )

        # =========================
        # TITEL
        # =========================

        title = self.big_font.render(
            "CLEAN BOARD",
            True,
            self.BLACK
        )

        self.screen.blit(
            title,
            (
                self.window_x + 310,
                self.window_y + 20
            )
        )

        info = self.font.render(
            "Lösche die ganze Tafel",
            True,
            self.BLACK
        )

        self.screen.blit(
            info,
            (
                self.window_x + 390,
                self.window_y + 100
            )
        )

        # =========================
        # TAFEL
        # =========================

        pygame.draw.rect(
            self.screen,
            self.BOARD_GREEN,
            self.board_rect,
            border_radius = 10
        )

        pygame.draw.rect(
            self.screen,
            self.BROWN,
            self.board_rect,
            width = 12,
            border_radius = 10
        )

        # =========================
        # KREIDEFLECKEN
        # =========================

        for dirt in self.dirt_spots:

            pygame.draw.circle(
                self.screen,
                self.CHALK,
                (
                    dirt["x"],
                    dirt["y"]
                ),
                dirt["radius"]
            )

        # =========================
        # SCHWAMM
        # =========================

        pygame.draw.rect(
            self.screen,
            self.YELLOW,
            self.sponge_rect,
            border_radius = 10
        )

        pygame.draw.rect(
            self.screen,
            self.BLACK,
            self.sponge_rect,
            width = 4,
            border_radius = 10
        )

        # =========================
        # FERTIG
        # =========================

        if self.finished:

            finished = self.big_font.render(
                "TASK FINISHED",
                True,
                self.GREEN
            )

            self.screen.blit(
                finished,
                (
                    self.window_x + 250,
                    self.window_y + 670
                )
            )

    def handle_event(self, event):

        if self.finished:
            return

        # =========================
        # MAUS GEDRÜCKT
        # =========================

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_pos = pygame.mouse.get_pos()

            if self.sponge_rect.collidepoint(mouse_pos):

                self.cleaning = True

        # =========================
        # MAUS LOSGELASSEN
        # =========================

        elif event.type == pygame.MOUSEBUTTONUP:

            self.cleaning = False

        # =========================
        # SCHWAMM BEWEGEN
        # =========================

        elif event.type == pygame.MOUSEMOTION:

            if self.cleaning:

                mouse_pos = pygame.mouse.get_pos()

                self.sponge_rect.center = mouse_pos

                self.clean_board()

    def clean_board(self):

        remaining_dirt = []

        for dirt in self.dirt_spots:

            dirt_rect = pygame.Rect(
                dirt["x"] - dirt["radius"],
                dirt["y"] - dirt["radius"],
                dirt["radius"] * 2,
                dirt["radius"] * 2
            )

            if not self.sponge_rect.colliderect(dirt_rect):

                remaining_dirt.append(dirt)

        self.dirt_spots = remaining_dirt

        # Task fertig
        if len(self.dirt_spots) == 0:

            self.finished = True

    def is_finished(self):
        return self.finished

class DownloadDataTask:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()

        # =========================
        # TASK WINDOW
        # =========================

        self.window_width = 1200
        self.window_height = 750

        self.window_x = (
            self.screen_width - self.window_width
        ) // 2

        self.window_y = (
            self.screen_height - self.window_height
        ) // 2

        self.task_rect = pygame.Rect(
            self.window_x,
            self.window_y,
            self.window_width,
            self.window_height
        )

        # =========================
        # FARBEN
        # =========================

        self.WHITE = (240, 240, 240)
        self.BLACK = (20, 20, 20)
        self.GREEN = (0, 220, 0)
        self.RED = (220, 60, 60)
        self.BLUE = (80, 140, 255)
        self.DARK_BLUE = (30, 50, 90)
        self.GRAY = (120, 120, 120)
        self.DARK_GRAY = (60, 60, 60)
        self.YELLOW = (255, 220, 0)

        # =========================
        # SCHRIFT
        # =========================

        self.font = pygame.font.SysFont("consolas", 36)
        self.big_font = pygame.font.SysFont("consolas", 60)

        # =========================
        # PC
        # =========================

        self.monitor_rect = pygame.Rect(
            self.window_x + 250,
            self.window_y + 170,
            700,
            350
        )

        self.screen_rect = pygame.Rect(
            self.window_x + 280,
            self.window_y + 200,
            640,
            290
        )

        # =========================
        # DOWNLOAD BUTTON
        # =========================

        self.download_button = pygame.Rect(
            self.window_x + 450,
            self.window_y + 570,
            320,
            80
        )

        # =========================
        # DOWNLOAD STATUS
        # =========================

        self.downloading = False

        self.progress = 0

        self.finished = False

        self.last_update = pygame.time.get_ticks()

    def draw(self):

        # Hintergrund
        self.screen.fill((20, 20, 30))

        # =========================
        # TASK WINDOW
        # =========================

        pygame.draw.rect(
            self.screen,
            self.WHITE,
            self.task_rect,
            border_radius=20
        )

        pygame.draw.rect(
            self.screen,
            self.BLACK,
            self.task_rect,
            width=5,
            border_radius=20
        )

        # =========================
        # TITEL
        # =========================

        title = self.big_font.render(
            "DOWNLOAD DATA",
            True,
            self.BLACK
        )

        self.screen.blit(
            title,
            (
                self.window_x + 260,
                self.window_y + 30
            )
        )

        # =========================
        # PC MONITOR
        # =========================

        pygame.draw.rect(
            self.screen,
            self.DARK_GRAY,
            self.monitor_rect,
            border_radius=15
        )

        pygame.draw.rect(
            self.screen,
            self.BLACK,
            self.monitor_rect,
            width=6,
            border_radius=15
        )

        # Bildschirm
        pygame.draw.rect(
            self.screen,
            self.DARK_BLUE,
            self.screen_rect,
            border_radius=10
        )

        # =========================
        # DOWNLOAD TEXT
        # =========================

        if self.downloading and not self.finished:
            status = self.font.render(
                "Downloading files...",
                True,
                self.GREEN
            )

        elif self.finished:
            status = self.font.render(
                "Download Complete!",
                True,
                self.GREEN
            )

        else:
            status = self.font.render(
                "Ready to download",
                True,
                self.YELLOW
            )

        self.screen.blit(
            status,
            (
                self.screen_rect.x + 140,
                self.screen_rect.y + 40
            )
        )

        # =========================
        # PROGRESS BAR
        # =========================

        bar_x = self.screen_rect.x + 70
        bar_y = self.screen_rect.y + 140
        bar_width = 500
        bar_height = 45

        # Hintergrund
        pygame.draw.rect(
            self.screen,
            self.GRAY,
            (
                bar_x,
                bar_y,
                bar_width,
                bar_height
            ),
            border_radius=10
        )

        # Fortschritt
        pygame.draw.rect(
            self.screen,
            self.GREEN,
            (
                bar_x,
                bar_y,
                int(bar_width * (self.progress / 100)),
                bar_height
            ),
            border_radius=10
        )

        pygame.draw.rect(
            self.screen,
            self.BLACK,
            (
                bar_x,
                bar_y,
                bar_width,
                bar_height
            ),
            width=4,
            border_radius=10
        )

        # Prozentzahl
        percent_text = self.big_font.render(
            f"{self.progress}%",
            True,
            self.WHITE
        )

        self.screen.blit(
            percent_text,
            (
                self.screen_rect.x + 250,
                self.screen_rect.y + 210
            )
        )

        # =========================
        # DOWNLOAD BUTTON
        # =========================

        if not self.downloading and not self.finished:

            pygame.draw.rect(
                self.screen,
                self.BLUE,
                self.download_button,
                border_radius=15
            )

            pygame.draw.rect(
                self.screen,
                self.BLACK,
                self.download_button,
                width=5,
                border_radius=15
            )

            button_text = self.font.render(
                "START DOWNLOAD",
                True,
                self.WHITE
            )

            self.screen.blit(
                button_text,
                (
                    self.download_button.x + 25,
                    self.download_button.y + 20
                )
            )

        # =========================
        # TASK FINISHED
        # =========================

        if self.finished:

            finished = self.big_font.render(
                "TASK FINISHED",
                True,
                self.GREEN
            )

            self.screen.blit(
                finished,
                (
                    self.window_x + 270,
                    self.window_y + 660
                )
            )

    def update(self):

        if self.downloading and not self.finished:

            current_time = pygame.time.get_ticks()

            # Alle 80ms Fortschritt erhöhen
            if current_time - self.last_update > 80:

                self.progress += 1

                self.last_update = current_time

                if self.progress >= 100:

                    self.progress = 100

                    self.finished = True

                    self.downloading = False

    def handle_event(self, event):

        if self.finished:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_pos = pygame.mouse.get_pos()

            if (self.download_button.collidepoint(mouse_pos) and not self.downloading and not self.finished):
                self.downloading = True
                self.progress = 0
                self.last_update = pygame.time.get_ticks()

    def is_finished(self):
        return self.finished

# =========================
# Wände
# =========================
walls = [
    pygame.Rect(200, 150, 300, 40),
    pygame.Rect(100, 400, 500, 40),
]

# =========================
# Spieler Klasse
# =========================
class Player:
    def __init__(self, x, y, image):
        self.x = float(x)
        self.y = float(y)

        self.image = image

        self.rect = pygame.Rect(
            int(self.x),
            int(self.y),
            PLAYER_SIZE,
            PLAYER_SIZE
        )

    def move(self, keys, dt, walls):
        moved = False

        old_x = self.x
        old_y = self.y

        dx = 0
        dy = 0

        if keys[pygame.K_w]:
            dy -= SPEED * dt

        if keys[pygame.K_s]:
            dy += SPEED * dt

        if keys[pygame.K_a]:
            dx -= SPEED * dt

        if keys[pygame.K_d]:
            dx += SPEED * dt

        # =========================
        # X Bewegung
        # =========================
        self.x += dx
        self.rect.x = int(self.x)

        for wall in walls:
            if self.rect.colliderect(wall):
                self.x = old_x
                self.rect.x = int(self.x)

        # =========================
        # Y Bewegung
        # =========================
        self.y += dy
        self.rect.y = int(self.y)

        for wall in walls:
            if self.rect.colliderect(wall):
                self.y = old_y
                self.rect.y = int(self.y)

        # Bildschirmgrenzen
        self.x = max(0, min(self.x, WIDTH - PLAYER_SIZE))
        self.y = max(0, min(self.y, HEIGHT - PLAYER_SIZE))

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

        if int(old_x) != int(self.x) or int(old_y) != int(self.y):
            moved = True

        return moved

    def draw(self, win):
        win.blit(self.image, (int(self.x), int(self.y)))

# =========================
# Button Klasse
# =========================
class Button:
    def __init__(self, x, y, w, h, text, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 200, 255), self.rect, border_radius=10)
        label = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(
            label,
            (
                self.rect.x + (self.rect.width - label.get_width()) // 2,
                self.rect.y + (self.rect.height - label.get_height()) // 2
            )
        )

    def clicked(self, pos):
        return self.rect.collidepoint(pos)

class TextInput:
    def __init__(self, x, y, w, h, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.font = font
        self.text = ""
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect, border_radius=8)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2, border_radius=8)

        txt = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(txt, (self.rect.x + 10, self.rect.y + 10))

# =========================
# Netzwerk
# =========================
other_player_pos = [300, 300]

def receive_data(sock):
    global other_player_pos

    while True:
        try:
            data = b""
            while len(data) < 8:
                packet = sock.recv(8 - len(data))
                if not packet:
                    return
                data += packet

            other_player_pos = list(struct.unpack('!ii', data))

        except:
            break

def setup_socket(sock):
    sock.setsockopt(
        socket.IPPROTO_TCP,
        socket.TCP_NODELAY,
        1
    )

    return sock

# =========================
# Server / Client Setup
# =========================
def start_server():
    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    # richtige lokale IP holen
    temp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        temp.connect(("8.8.8.8", 80))
        host_ip = temp.getsockname()[0]

    finally:
        temp.close()

    server.bind((host_ip, PORT))
    server.listen(1)

    print(f"\nServer gestartet!")
    print(f"Lobby-IP: {host_ip}")
    print(f"Port: {PORT}")
    print("Warte auf Verbindung...\n")

    conn, addr = server.accept()

    print(f"Verbunden mit: {addr}")

    return setup_socket(conn)

def connect_to_server(ip):
    client = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    client.connect((ip, PORT))

    print("Verbunden!")

    return setup_socket(client)

# =========================================
# TASK SYSTEM
# =========================================

task_manager = TaskManager()

task_manager.add_task(BookSortTask(screen))
task_manager.add_task(ChairStackTask(screen))
task_manager.add_task(WindowTask(screen))
task_manager.add_task(DownloadDataTask(screen))
task_manager.add_task(CleanBoardTask(screen))

task_buttons = [
    pygame.Rect(420, 90, 60, 60),
    pygame.Rect(600, 200, 60, 60),
    pygame.Rect(300, 350, 60, 60),
    pygame.Rect(700, 400, 60, 60),
    pygame.Rect(500, 500, 60, 60),
]

font = pygame.font.SysFont("arial", 30)

font = pygame.font.SysFont("arial", 40)

# =========================
# HOST ODER JOIN
# =========================

mode = input("Hosten (h) oder Joinen (j)? ").lower()

sock = None

if mode == "h":

    sock = start_server()

    my_player = Player(
        100,
        100,
        player1_image
    )

    other_image = player2_image

else:

    ip = input("Server IP eingeben: ")

    sock = connect_to_server(ip)

    my_player = Player(
        100,
        100,
        player2_image
    )

    other_image = player1_image

# Empfangs-Thread
threading.Thread(
    target = receive_data,
    args = (sock,),
    daemon = True
).start()

# =========================
# Spielschleife
# =========================
running = True

while running:

    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:

                # Wenn Task offen -> nur Task schließen
                if task_manager.active_task:
                    task_manager.active_task = None

                # Sonst Spiel schließen
                else:
                    running = False
                    pygame.quit()
                    exit()

            if event.key == pygame.K_e:

                for i, btn in enumerate(task_buttons):

                    distance_x = my_player.rect.centerx - btn.centerx
                    distance_y = my_player.rect.centery - btn.centery

                    if abs(distance_x) < 100 and abs(distance_y) < 100:

                        if task_manager.active_task is None:
                            if task_manager.tasks[i].finished:
                                task_manager.show_message("Task already completed")
                            else:
                                task_manager.start_task(i)

                        break

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_pos = pygame.mouse.get_pos()

            for i, btn in enumerate(task_buttons):
                distance_x = my_player.rect.centerx - btn.centerx
                distance_y = my_player.rect.centery - btn.centery

                if abs(distance_x) < 100 and abs(distance_y) < 100:
                    if btn.collidepoint(event.pos):
                        if task_manager.active_task is None:
                            if task_manager.tasks[i].finished:
                                task_manager.show_message("Task already completed")
                            else:
                                task_manager.start_task(i)

        # =========================
        # TASK EVENTS
        # =========================
        task_manager.handle_event(event)

    keys = pygame.key.get_pressed()

    # Bewegung
    has_moved = False

    if task_manager.active_task is None:

        has_moved = my_player.move(
            keys,   
            dt,
            walls
        )

    # Netzwerk senden
    if has_moved:
        try:
            data = struct.pack('!ii', int(my_player.x), int(my_player.y))
            sock.sendall(data)
        except Exception as e:
            print(f"Verbindung verloren: {e}")
            running = False

    # =========================
    # Zeichnen
    # =========================
    screen.fill((30, 30, 30))

    # Wände
    for wall in walls:
        pygame.draw.rect(
            screen,
            (100, 100, 100),
            wall
        )

    for btn in task_buttons:
        pygame.draw.rect(
            screen,
            (0, 200, 255),
            btn,
            border_radius=10
        )

    # Gegner
    screen.blit(
        other_image,
        (
            other_player_pos[0],
            other_player_pos[1]
        )
    )

    # Task hint
    for btn in task_buttons:

        distance_x = (
            my_player.rect.centerx
            - btn.centerx
        )

        distance_y = (
            my_player.rect.centery
            - btn.centery
        )

        near_task = (
            abs(distance_x) < 100
            and
            abs(distance_y) < 100
        )

        if near_task and not task_manager.active_task:

            text = font.render(
                "Drücke E für Task",
                True,
                (255, 255, 255)
            )

            screen.blit(
                text,
                (
                    btn.x - 50,
                    btn.y - 40
                )
            )

    # Eigener Spieler
    my_player.draw(screen)

    # draw & update task
    task_manager.draw(screen)
    task_manager.update()

    pygame.display.update()

# =========================
# Beenden
# =========================
try:
    sock.close()

except:
    pass

pygame.quit()