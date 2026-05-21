import pygame
import random
import math

pygame.init()

# =========================================
# BOOK SORT TASK (Among Us Style)
# =========================================

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

            if (self.download_button.collidepoint(mouse_pos) and not self.downloading):
                self.downloading = True
                self.progress = 0
                self.last_update = pygame.time.get_ticks()

    def is_finished(self):
        return self.finished

class ProjectorWiresTask:
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

        self.RED = (220, 60, 60)
        self.BLUE = (60, 120, 255)
        self.GREEN = (60, 200, 100)
        self.YELLOW = (255, 220, 0)

        self.GRAY = (120, 120, 120)

        # =========================
        # SCHRIFT
        # =========================

        self.font = pygame.font.SysFont(
            "arial",
            40
        )

        self.big_font = pygame.font.SysFont(
            "arial",
            70
        )

        # =========================
        # KABEL
        # =========================

        self.left_points = []
        self.right_points = []

        self.create_wire_points()

        # Verbindungslinien
        self.connections = []

        # Aktuelles Kabel
        self.selected_wire = None

        # =========================
        # STATUS
        # =========================

        self.finished = False

    def create_wire_points(self):

        colors = [
            self.RED,
            self.BLUE,
            self.GREEN,
            self.YELLOW
        ]

        # LINKE SEITE
        for i in range(4):

            x = self.window_x + 220
            y = self.window_y + 220 + (i * 110)

            self.left_points.append({
                "pos": (x, y),
                "color": colors[i],
                "connected": False
            })

        # RECHTE SEITE (gemischt)

        shuffled = colors.copy()
        random.shuffle(shuffled)

        for i in range(4):

            x = self.window_x + 950
            y = self.window_y + 220 + (i * 110)

            self.right_points.append({
                "pos": (x, y),
                "color": shuffled[i],
                "connected": False
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
            "CONNECT PROJECTOR",
            True,
            self.BLACK
        )

        self.screen.blit(
            title,
            (
                self.window_x + 250,
                self.window_y + 20
            )
        )

        info = self.font.render(
            "Verbinde die richtigen Kabel",
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
        # PROJEKTOR
        # =========================

        projector_rect = pygame.Rect(
            self.window_x + 870,
            self.window_y + 600,
            220,
            90
        )

        pygame.draw.rect(
            self.screen,
            self.GRAY,
            projector_rect,
            border_radius = 15
        )

        projector_text = self.font.render(
            "PROJECTOR",
            True,
            self.BLACK
        )

        self.screen.blit(
            projector_text,
            (
                projector_rect.x + 10,
                projector_rect.y + 20
            )
        )

        # =========================
        # PC
        # =========================

        pc_rect = pygame.Rect(
            self.window_x + 120,
            self.window_y + 600,
            180,
            90
        )

        pygame.draw.rect(
            self.screen,
            self.GRAY,
            pc_rect,
            border_radius=15
        )

        pc_text = self.font.render(
            "PC",
            True,
            self.BLACK
        )

        self.screen.blit(
            pc_text,
            (
                pc_rect.x + 60,
                pc_rect.y + 20
            )
        )

        # =========================
        # VERBINDUNGEN
        # =========================

        for connection in self.connections:

            pygame.draw.line(
                self.screen,
                connection["color"],
                connection["start"],
                connection["end"],
                8
            )

        # =========================
        # AKTUELLES KABEL
        # =========================

        if self.selected_wire:

            mouse_pos = pygame.mouse.get_pos()

            pygame.draw.line(
                self.screen,
                self.selected_wire["color"],
                self.selected_wire["pos"],
                mouse_pos,
                8
            )

        # =========================
        # PUNKTE
        # =========================

        for point in self.left_points:

            pygame.draw.circle(
                self.screen,
                point["color"],
                point["pos"],
                25
            )

            pygame.draw.circle(
                self.screen,
                self.BLACK,
                point["pos"],
                25,
                4
            )

        for point in self.right_points:

            pygame.draw.circle(
                self.screen,
                point["color"],
                point["pos"],
                25
            )

            pygame.draw.circle(
                self.screen,
                self.BLACK,
                point["pos"],
                25,
                4
            )

        # =========================
        # TASK FINISHED
        # =========================

        if self.finished:

            finished = self.big_font.render(
                "PROJECTOR CONNECTED",
                True,
                self.GREEN
            )

            self.screen.blit(
                finished,
                (
                    self.window_x + 170,
                    self.window_y + 320
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

            for point in self.left_points:

                distance = math.hypot(
                    mouse_pos[0] - point["pos"][0],
                    mouse_pos[1] - point["pos"][1]
                )

                if distance < 25 and not point["connected"]:

                    self.selected_wire = point
                    break

        # =========================
        # LOSLASSEN
        # =========================

        elif event.type == pygame.MOUSEBUTTONUP:

            if self.selected_wire:

                mouse_pos = pygame.mouse.get_pos()

                for point in self.right_points:

                    distance = math.hypot(
                        mouse_pos[0] - point["pos"][0],
                        mouse_pos[1] - point["pos"][1]
                    )

                    if distance < 25:

                        # Richtige Farbe?
                        if (
                            point["color"]
                            ==
                            self.selected_wire["color"]
                            and
                            not point["connected"]
                        ):

                            self.connections.append({
                                "start": self.selected_wire["pos"],
                                "end": point["pos"],
                                "color": point["color"]
                            })

                            self.selected_wire["connected"] = True
                            point["connected"] = True

                            break

                self.selected_wire = None
                self.check_finished()

    def check_finished(self):

        all_connected = True

        for point in self.left_points:

            if not point["connected"]:
                all_connected = False

        if all_connected:
            self.finished = True

    def is_finished(self):
        return self.finished

class VirusScanTask:
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

        self.RED = (220, 60, 60)
        self.GREEN = (60, 200, 100)
        self.BLUE = (80, 120, 255)

        self.GRAY = (100, 100, 100)

        # =========================
        # SCHRIFT
        # =========================

        self.font = pygame.font.SysFont(
            "arial",
            25
        )

        self.big_font = pygame.font.SysFont(
            "arial",
            65
        )

        # =========================
        # DATEIEN
        # =========================

        self.files = []

        self.create_files()

        # =========================
        # STATUS
        # =========================

        self.finished = False

        self.virus_count = 0

        for file in self.files:
            if file["virus"]:
                self.virus_count += 1

    def create_files(self):

        names = [
            "Münzwurf.js",
            "Tutorial_Docker2.pdf",
            "HuRenRef.exe",
            "PasswortManager2.pdf",
            "Free_Robux.exe",
            "Energieschema.png",
            "Schöne_Frau.jpg.exe",
            "Hacker_Tool.exe",
            "AA_Hexenverfolgung.docx",
            "E_Spannungsreihe.docx"
        ]

        virus_files = []

        for y in range(6):
            virus_files.append(names[random.randint(0, len(names) - 1)])       

        start_x = self.window_x + 120
        start_y = self.window_y + 180

        index = 0

        for row in range(2):

            for col in range(5):

                name = names[index]

                rect = pygame.Rect(
                    start_x + (col * 210),
                    start_y + (row * 240),
                    140,
                    140
                )

                self.files.append({
                    "name": name,
                    "rect": rect,
                    "virus": name in virus_files,
                    "removed": False
                })

                index += 1

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
            "VIRUS SCAN",
            True,
            self.BLACK
        )

        self.screen.blit(
            title,
            (
                self.window_x + 360,
                self.window_y + 20
            )
        )

        info = self.font.render(
            "Entferne alle verdächtigen Dateien",
            True,
            self.BLACK
        )

        self.screen.blit(
            info,
            (
                self.window_x + 280,
                self.window_y + 100
            )
        )

        # =========================
        # PC RAHMEN
        # =========================

        monitor_rect = pygame.Rect(
            self.window_x + 70,
            self.window_y + 150,
            1060,
            500
        )

        pygame.draw.rect(
            self.screen,
            (40, 40, 50),
            monitor_rect,
            border_radius=15
        )

        # =========================
        # DATEIEN
        # =========================

        for file in self.files:

            if file["removed"]:
                continue

            # Datei Icon

            pygame.draw.rect(
                self.screen,
                self.BLUE,
                file["rect"],
                border_radius = 10
            )

            pygame.draw.rect(
                self.screen,
                self.BLACK,
                file["rect"],
                width = 3,
                border_radius = 10
            )

            # Datei Text

            text = self.font.render(
                file["name"],
                True,
                self.WHITE
            )

            text_rect = text.get_rect(
                center=(
                    file["rect"].centerx,
                    file["rect"].bottom + 25
                )
            )

            self.screen.blit(
                text,
                text_rect
            )

            # Warnsymbol für Virus-Dateien

            if file["virus"]:

                pygame.draw.circle(
                    self.screen,
                    self.RED,
                    (
                        file["rect"].right - 15,
                        file["rect"].y + 15
                    ),
                    12
                )

        # =========================
        # TASK FINISHED
        # =========================

        if self.finished:

            finished = self.big_font.render(
                "SCAN COMPLETE",
                True,
                self.GREEN
            )

            self.screen.blit(
                finished,
                (
                    self.window_x + 260,
                    self.window_y + 320
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

            for file in self.files:

                if file["removed"]:
                    continue

                if file["rect"].collidepoint(mouse_pos):

                    # Nur Virus-Dateien entfernen

                    if file["virus"]:

                        file["removed"] = True

                        self.check_finished()

                    break

    def check_finished(self):

        removed_count = 0

        for file in self.files:

            if file["virus"] and file["removed"]:
                removed_count += 1

        if removed_count >= self.virus_count:
            self.finished = True

    def is_finished(self):
        return self.finished

# =========================================
# TEST
# =========================================

if __name__ == "__main__":

    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h
    screen = pygame.display.set_mode(size = (screen_width, screen_height), flags = pygame.FULLSCREEN | pygame.SCALED)

    pygame.display.set_caption("Among Us School Task")

    clock = pygame.time.Clock()

    task = VirusScanTask(screen)

    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            task.handle_event(event)

        task.draw()

        pygame.display.update()
        clock.tick(60)

    pygame.quit()