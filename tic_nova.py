import pygame
import json
import os

pygame.init()

# ============================================================
# WINDOW
# ============================================================

WIDTH = 850
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TicNova")


# ============================================================
# COLORS
# ============================================================

BACKGROUND = (30, 30, 30)
WHITE = (255, 255, 255)
RED = (220, 60, 60)
BLUE = (60, 120, 255)
GREEN = (60, 200, 100)
YELLOW = (255, 220, 60)
GRAY = (80, 80, 80)
DARK_GRAY = (45, 45, 45)


# ============================================================
# BOARD
# ============================================================

BOARD_SIZE = 600
CELL_SIZE = BOARD_SIZE // 3
LINE_WIDTH = 5


# ============================================================
# FONTS
# ============================================================

player_font = pygame.font.Font(None, 150)
message_font = pygame.font.Font(None, 70)
small_font = pygame.font.Font(None, 32)
history_title_font = pygame.font.Font(None, 55)
history_font = pygame.font.Font(None, 28)
input_font = pygame.font.Font(None, 38)


# ============================================================
# SAVE FILE
# ============================================================

SAVE_FILE = "data.json"


# ============================================================
# PLAYER DATABASE
# ============================================================

players = {}


# ============================================================
# CURRENT MATCH PLAYERS
# ============================================================

player_x_name = ""
player_o_name = ""


# ============================================================
# MENU VARIABLES
# ============================================================

menu_screen = True

menu_mode = "main"

selected_player_slot = "X"

new_player_name = ""

selected_x_player = None
selected_o_player = None

player_list_scroll = 0


# ============================================================
# GAME VARIABLES
# ============================================================

board = [
    ["", "", ""],
    ["", "", ""],
    ["", "", ""]
]

current_player = "X"

winner = None
draw = False

winning_cells = []

current_game_moves = []


# ============================================================
# SESSION VARIABLES
# ============================================================

session_finished = False

session_history = []


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    global players

    if not os.path.exists(SAVE_FILE):
        players = {}
        return

    try:

        with open(
            SAVE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        players = data.get("players", {})

    except (json.JSONDecodeError, OSError):

        players = {}


# ============================================================
# SAVE DATA
# ============================================================

def save_data():

    data = {
        "players": players
    }

    try:

        with open(
            SAVE_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

    except OSError:

        print("Could not save data.")


# ============================================================
# CREATE PLAYER
# ============================================================

def create_player(name):

    name = name.strip()

    if name == "":
        return False

    if name in players:
        return False

    players[name] = {
        "wins": 0,
        "losses": 0,
        "draws": 0,
        "games": 0,
        "history": []
    }

    save_data()

    return True


# ============================================================
# CHECK PLAYER NAME
# ============================================================

def player_exists(name):

    return name in players


# ============================================================
# CHECK WINNER
# ============================================================

def check_winner():

    # Rows
    for row in range(3):

        if (
            board[row][0] != ""
            and board[row][0] == board[row][1]
            and board[row][1] == board[row][2]
        ):

            return board[row][0], [
                (row, 0),
                (row, 1),
                (row, 2)
            ]


    # Columns
    for col in range(3):

        if (
            board[0][col] != ""
            and board[0][col] == board[1][col]
            and board[1][col] == board[2][col]
        ):

            return board[0][col], [
                (0, col),
                (1, col),
                (2, col)
            ]


    # Main diagonal
    if (
        board[0][0] != ""
        and board[0][0] == board[1][1]
        and board[1][1] == board[2][2]
    ):

        return board[0][0], [
            (0, 0),
            (1, 1),
            (2, 2)
        ]


    # Other diagonal
    if (
        board[0][2] != ""
        and board[0][2] == board[1][1]
        and board[1][1] == board[2][0]
    ):

        return board[0][2], [
            (0, 2),
            (1, 1),
            (2, 0)
        ]


    return None, []


# ============================================================
# CHECK DRAW
# ============================================================

def check_draw():

    for row in board:

        for cell in row:

            if cell == "":
                return False

    return True


# ============================================================
# GET PLAYER NAME
# ============================================================

def get_player_name(symbol):

    if symbol == "X":
        return player_x_name

    return player_o_name


# ============================================================
# GET CELL CENTER
# ============================================================

def get_cell_center(row, col):

    return (
        col * CELL_SIZE + CELL_SIZE // 2,
        row * CELL_SIZE + CELL_SIZE // 2
    )


# ============================================================
# RESET GAME
# ============================================================

def reset_game():

    global board
    global current_player
    global winner
    global draw
    global winning_cells
    global current_game_moves
    global session_finished

    board = [
        ["", "", ""],
        ["", "", ""],
        ["", "", ""]
    ]

    current_player = "X"

    winner = None
    draw = False

    winning_cells = []

    current_game_moves = []

    session_finished = False


# ============================================================
# SAVE COMPLETED GAME
# ============================================================

def save_completed_game():

    if winner is not None:

        winner_name = get_player_name(winner)

        loser_symbol = "O" if winner == "X" else "X"

        loser_name = get_player_name(loser_symbol)

        # Winner statistics
        players[winner_name]["wins"] += 1
        players[winner_name]["games"] += 1

        # Loser statistics
        players[loser_name]["losses"] += 1
        players[loser_name]["games"] += 1

        # Winner history
        players[winner_name]["history"].append({
            "opponent": loser_name,
            "result": "WIN",
            "moves": len(current_game_moves)
        })

        # Loser history
        players[loser_name]["history"].append({
            "opponent": winner_name,
            "result": "LOSS",
            "moves": len(current_game_moves)
        })


        # Session history
        session_history.append({
            "level": len(session_history) + 1,
            "player_x": player_x_name,
            "player_o": player_o_name,
            "winner": winner_name,
            "result": winner_name + " WINS",
            "moves": len(current_game_moves)
        })


    elif draw:

        players[player_x_name]["draws"] += 1
        players[player_x_name]["games"] += 1

        players[player_o_name]["draws"] += 1
        players[player_o_name]["games"] += 1


        # Player X history
        players[player_x_name]["history"].append({
            "opponent": player_o_name,
            "result": "DRAW",
            "moves": len(current_game_moves)
        })


        # Player O history
        players[player_o_name]["history"].append({
            "opponent": player_x_name,
            "result": "DRAW",
            "moves": len(current_game_moves)
        })


        session_history.append({
            "level": len(session_history) + 1,
            "player_x": player_x_name,
            "player_o": player_o_name,
            "winner": "DRAW",
            "result": "DRAW",
            "moves": len(current_game_moves)
        })


    # Save immediately
    save_data()


# ============================================================
# DRAW MAIN MENU
# ============================================================

def draw_main_menu():

    screen.fill(BACKGROUND)

    title = message_font.render(
        "TICNOVA",
        True,
        YELLOW
    )

    title_rect = title.get_rect(
        center=(WIDTH // 2, 80)
    )

    screen.blit(title, title_rect)


    subtitle = small_font.render(
        "Two Player Tic-Tac-Toe",
        True,
        WHITE
    )

    screen.blit(
        subtitle,
        subtitle.get_rect(
            center=(WIDTH // 2, 130)
        )
    )


    # X player
    x_text = history_font.render(
        f"Player X: {selected_x_player or 'Not Selected'}",
        True,
        RED
    )

    screen.blit(
        x_text,
        (180, 210)
    )


    # O player
    o_text = history_font.render(
        f"Player O: {selected_o_player or 'Not Selected'}",
        True,
        BLUE
    )

    screen.blit(
        o_text,
        (180, 250)
    )


    # Buttons
    pygame.draw.rect(
        screen,
        GRAY,
        (180, 320, 490, 55)
    )

    select_x = small_font.render(
        "1 - Select Player X",
        True,
        WHITE
    )

    screen.blit(
        select_x,
        select_x.get_rect(
            center=(WIDTH // 2, 347)
        )
    )


    pygame.draw.rect(
        screen,
        GRAY,
        (180, 390, 490, 55)
    )

    select_o = small_font.render(
        "2 - Select Player O",
        True,
        WHITE
    )

    screen.blit(
        select_o,
        select_o.get_rect(
            center=(WIDTH // 2, 417)
        )
    )


    # Start button
    if (
        selected_x_player is not None
        and selected_o_player is not None
        and selected_x_player != selected_o_player
    ):

        pygame.draw.rect(
            screen,
            GREEN,
            (180, 460, 490, 55)
        )

        start_text = small_font.render(
            "ENTER - Start Game",
            True,
            WHITE
        )

        screen.blit(
            start_text,
            start_text.get_rect(
                center=(WIDTH // 2, 487)
            )
        )

    else:

        warning = small_font.render(
            "Select two different players",
            True,
            WHITE
        )

        screen.blit(
            warning,
            warning.get_rect(
                center=(WIDTH // 2, 487)
            )
        )


    controls = history_font.render(
        "N = New Player     C = Clear All Data",
        True,
        WHITE
    )

    screen.blit(
        controls,
        controls.get_rect(
            center=(WIDTH // 2, 550)
        )
    )


# ============================================================
# DRAW PLAYER SELECT SCREEN
# ============================================================

def draw_player_select():

    screen.fill(BACKGROUND)

    title = message_font.render(
        f"SELECT PLAYER {selected_player_slot}",
        True,
        YELLOW
    )

    screen.blit(
        title,
        title.get_rect(
            center=(WIDTH // 2, 60)
        )
    )


    if len(players) == 0:

        empty = history_font.render(
            "No players found. Press N to create one.",
            True,
            WHITE
        )

        screen.blit(
            empty,
            empty.get_rect(
                center=(WIDTH // 2, 180)
            )
        )

    else:

        player_names = list(players.keys())

        y = 130

        for index, name in enumerate(player_names):

            if index >= 7:
                break

            player = players[name]

            pygame.draw.rect(
                screen,
                DARK_GRAY,
                (120, y, 610, 55)
            )

            if name == selected_x_player:
                border_color = RED

            elif name == selected_o_player:
                border_color = BLUE

            else:
                border_color = WHITE

            pygame.draw.rect(
                screen,
                border_color,
                (120, y, 610, 55),
                2
            )

            player_text = history_font.render(
                f"{index + 1}. {name} | "
                f"W: {player['wins']} "
                f"L: {player['losses']} "
                f"D: {player['draws']}",
                True,
                WHITE
            )

            screen.blit(
                player_text,
                (140, y + 15)
            )

            y += 65


    controls = history_font.render(
        "Press number to select | N = New Player | ESC = Back",
        True,
        WHITE
    )

    screen.blit(
        controls,
        controls.get_rect(
            center=(WIDTH // 2, 550)
        )
    )


# ============================================================
# DRAW NEW PLAYER SCREEN
# ============================================================

def draw_new_player():

    screen.fill(BACKGROUND)

    title = message_font.render(
        "NEW PLAYER",
        True,
        YELLOW
    )

    screen.blit(
        title,
        title.get_rect(
            center=(WIDTH // 2, 100)
        )
    )


    subtitle = small_font.render(
        "Enter player name",
        True,
        WHITE
    )

    screen.blit(
        subtitle,
        subtitle.get_rect(
            center=(WIDTH // 2, 170)
        )
    )


    pygame.draw.rect(
        screen,
        WHITE,
        (180, 230, 490, 60),
        2
    )


    name_text = input_font.render(
        new_player_name,
        True,
        WHITE
    )

    screen.blit(
        name_text,
        (195, 245)
    )


    instruction = history_font.render(
        "ENTER = Create Player | BACKSPACE = Delete | ESC = Back",
        True,
        WHITE
    )

    screen.blit(
        instruction,
        instruction.get_rect(
            center=(WIDTH // 2, 380)
        )
    )


# ============================================================
# DRAW FINAL RESULT
# ============================================================

def draw_final_result():

    screen.fill(BACKGROUND)

    title = message_font.render(
        "FINAL RESULT",
        True,
        YELLOW
    )

    screen.blit(
        title,
        title.get_rect(
            center=(WIDTH // 2, 60)
        )
    )


    x_data = players[player_x_name]
    o_data = players[player_o_name]


    x_score = history_font.render(
        f"{player_x_name}: "
        f"{x_data['wins']} W / "
        f"{x_data['losses']} L / "
        f"{x_data['draws']} D",
        True,
        RED
    )

    screen.blit(
        x_score,
        x_score.get_rect(
            center=(WIDTH // 2, 160)
        )
    )


    o_score = history_font.render(
        f"{player_o_name}: "
        f"{o_data['wins']} W / "
        f"{o_data['losses']} L / "
        f"{o_data['draws']} D",
        True,
        BLUE
    )

    screen.blit(
        o_score,
        o_score.get_rect(
            center=(WIDTH // 2, 210)
        )
    )


    # Session winner
    session_x_wins = 0
    session_o_wins = 0
    session_draws = 0


    for game in session_history:

        if game["winner"] == player_x_name:
            session_x_wins += 1

        elif game["winner"] == player_o_name:
            session_o_wins += 1

        else:
            session_draws += 1


    if session_x_wins > session_o_wins:

        final_text = (
            f"SESSION WINNER: {player_x_name}"
        )

        final_color = RED

    elif session_o_wins > session_x_wins:

        final_text = (
            f"SESSION WINNER: {player_o_name}"
        )

        final_color = BLUE

    else:

        final_text = "SESSION RESULT: DRAW"

        final_color = WHITE


    final_message = message_font.render(
        final_text,
        True,
        final_color
    )

    screen.blit(
        final_message,
        final_message.get_rect(
            center=(WIDTH // 2, 300)
        )
    )


    session_score = history_font.render(
        f"{player_x_name}: {session_x_wins} | "
        f"{player_o_name}: {session_o_wins} | "
        f"Draws: {session_draws}",
        True,
        WHITE
    )

    screen.blit(
        session_score,
        session_score.get_rect(
            center=(WIDTH // 2, 360)
        )
    )


    total_games = history_font.render(
        f"Games in session: {len(session_history)}",
        True,
        WHITE
    )

    screen.blit(
        total_games,
        total_games.get_rect(
            center=(WIDTH // 2, 420)
        )
    )


    controls = small_font.render(
        "R = New Game     ESC = Main Menu",
        True,
        WHITE
    )

    screen.blit(
        controls,
        controls.get_rect(
            center=(WIDTH // 2, 500)
        )
    )


# ============================================================
# DRAW GAME
# ============================================================

def draw_game():

    screen.fill(BACKGROUND)


    # ========================================================
    # BOARD
    # ========================================================

    pygame.draw.line(
        screen,
        WHITE,
        (CELL_SIZE, 0),
        (CELL_SIZE, BOARD_SIZE),
        LINE_WIDTH
    )

    pygame.draw.line(
        screen,
        WHITE,
        (CELL_SIZE * 2, 0),
        (CELL_SIZE * 2, BOARD_SIZE),
        LINE_WIDTH
    )

    pygame.draw.line(
        screen,
        WHITE,
        (0, CELL_SIZE),
        (BOARD_SIZE, CELL_SIZE),
        LINE_WIDTH
    )

    pygame.draw.line(
        screen,
        WHITE,
        (0, CELL_SIZE * 2),
        (BOARD_SIZE, CELL_SIZE * 2),
        LINE_WIDTH
    )


    # ========================================================
    # X AND O
    # ========================================================

    for row in range(3):

        for col in range(3):

            if board[row][col] != "":

                if board[row][col] == "X":

                    color = RED

                else:

                    color = BLUE


                text = player_font.render(
                    board[row][col],
                    True,
                    color
                )

                text_rect = text.get_rect(
                    center=get_cell_center(row, col)
                )

                screen.blit(
                    text,
                    text_rect
                )


    # ========================================================
    # WINNING LINE
    # ========================================================

    if (
        winner is not None
        and len(winning_cells) == 3
    ):

        start = get_cell_center(
            winning_cells[0][0],
            winning_cells[0][1]
        )

        end = get_cell_center(
            winning_cells[2][0],
            winning_cells[2][1]
        )

        pygame.draw.line(
            screen,
            YELLOW,
            start,
            end,
            12
        )


    # ========================================================
    # GAME MESSAGE
    # ========================================================

    if winner is not None:

        winner_name = get_player_name(winner)

        message = message_font.render(
            f"{winner_name} WINS!",
            True,
            GREEN
        )

        screen.blit(
            message,
            message.get_rect(
                center=(BOARD_SIZE // 2, 260)
            )
        )

        result = small_font.render(
            f"Moves: {len(current_game_moves)}",
            True,
            WHITE
        )

        screen.blit(
            result,
            result.get_rect(
                center=(BOARD_SIZE // 2, 320)
            )
        )

        restart = small_font.render(
            "R = Next Level",
            True,
            WHITE
        )

        screen.blit(
            restart,
            restart.get_rect(
                center=(BOARD_SIZE // 2, 370)
            )
        )


    elif draw:

        message = message_font.render(
            "DRAW!",
            True,
            WHITE
        )

        screen.blit(
            message,
            message.get_rect(
                center=(BOARD_SIZE // 2, 260)
            )
        )

        result = small_font.render(
            f"Moves: {len(current_game_moves)}",
            True,
            WHITE
        )

        screen.blit(
            result,
            result.get_rect(
                center=(BOARD_SIZE // 2, 320)
            )
        )

        restart = small_font.render(
            "R = Next Level",
            True,
            WHITE
        )

        screen.blit(
            restart,
            restart.get_rect(
                center=(BOARD_SIZE // 2, 370)
            )
        )


    else:

        current_name = get_player_name(
            current_player
        )

        turn = small_font.render(
            f"{current_name} ({current_player})'s Turn",
            True,
            WHITE
        )

        screen.blit(
            turn,
            (10, 10)
        )


    # ========================================================
    # RIGHT PANEL
    # ========================================================

    pygame.draw.rect(
        screen,
        GRAY,
        (620, 0, 230, 600)
    )


    title = history_title_font.render(
        "PLAYERS",
        True,
        WHITE
    )

    screen.blit(
        title,
        (660, 15)
    )


    # Player X
    x_data = players[player_x_name]

    x_info = history_font.render(
        f"X: {player_x_name}",
        True,
        RED
    )

    screen.blit(
        x_info,
        (630, 70)
    )

    x_stats = history_font.render(
        f"W {x_data['wins']} "
        f"L {x_data['losses']} "
        f"D {x_data['draws']}",
        True,
        WHITE
    )

    screen.blit(
        x_stats,
        (630, 100)
    )


    # Player O
    o_data = players[player_o_name]

    o_info = history_font.render(
        f"O: {player_o_name}",
        True,
        BLUE
    )

    screen.blit(
        o_info,
        (630, 145)
    )

    o_stats = history_font.render(
        f"W {o_data['wins']} "
        f"L {o_data['losses']} "
        f"D {o_data['draws']}",
        True,
        WHITE
    )

    screen.blit(
        o_stats,
        (630, 175)
    )


    # ========================================================
    # SESSION HISTORY
    # ========================================================

    history_title = history_font.render(
        "SESSION HISTORY",
        True,
        YELLOW
    )

    screen.blit(
        history_title,
        (630, 220)
    )


    y = 255


    if len(session_history) == 0:

        text = history_font.render(
            "No games yet",
            True,
            WHITE
        )

        screen.blit(
            text,
            (650, y)
        )


    else:

        for game in session_history[-3:]:

            level = history_font.render(
                f"LEVEL {game['level']}",
                True,
                YELLOW
            )

            screen.blit(
                level,
                (630, y)
            )


            result_color = WHITE

            if game["winner"] == player_x_name:
                result_color = RED

            elif game["winner"] == player_o_name:
                result_color = BLUE


            result = history_font.render(
                game["result"],
                True,
                result_color
            )

            screen.blit(
                result,
                (630, y + 25)
            )


            moves = history_font.render(
                f"Moves: {game['moves']}",
                True,
                WHITE
            )

            screen.blit(
                moves,
                (630, y + 50)
            )


            pygame.draw.line(
                screen,
                WHITE,
                (630, y + 75),
                (835, y + 75),
                2
            )


            y += 85


    # ========================================================
    # CONTROLS
    # ========================================================

    controls = history_font.render(
        "R = Restart",
        True,
        WHITE
    )

    screen.blit(
        controls,
        (630, 520)
    )


    finish = history_font.render(
        "F = Finish",
        True,
        YELLOW
    )

    screen.blit(
        finish,
        (745, 520)
    )


# ============================================================
# LOAD DATABASE
# ============================================================

load_data()


# ============================================================
# MAIN LOOP
# ============================================================

running = True

while running:

    # ========================================================
    # EVENTS
    # ========================================================

    for event in pygame.event.get():

        # ----------------------------------------------------
        # CLOSE
        # ----------------------------------------------------

        if event.type == pygame.QUIT:

            save_data()

            running = False


        # ====================================================
        # MAIN MENU
        # ====================================================

        elif menu_screen and menu_mode == "main":

            if event.type == pygame.KEYDOWN:

                # Select X
                if event.key == pygame.K_1:

                    selected_player_slot = "X"

                    menu_mode = "select"


                # Select O
                elif event.key == pygame.K_2:

                    selected_player_slot = "O"

                    menu_mode = "select"


                # New player
                elif event.key == pygame.K_n:

                    new_player_name = ""

                    menu_mode = "new"


                # Start
                elif event.key == pygame.K_RETURN:

                    if (
                        selected_x_player is not None
                        and selected_o_player is not None
                        and selected_x_player != selected_o_player
                    ):

                        player_x_name = selected_x_player
                        player_o_name = selected_o_player

                        reset_game()

                        menu_screen = False


                # Clear everything
                elif event.key == pygame.K_c:

                    players.clear()

                    save_data()

                    selected_x_player = None
                    selected_o_player = None


        # ====================================================
        # PLAYER SELECT
        # ====================================================

        elif menu_screen and menu_mode == "select":

            if event.type == pygame.KEYDOWN:

                # Back
                if event.key == pygame.K_ESCAPE:

                    menu_mode = "main"


                # New player
                elif event.key == pygame.K_n:

                    new_player_name = ""

                    menu_mode = "new"


                # Select player by number
                elif (
                    pygame.K_1
                    <= event.key
                    <= pygame.K_9
                ):

                    index = (
                        event.key
                        - pygame.K_1
                    )

                    player_names = list(
                        players.keys()
                    )

                    if index < len(player_names):

                        selected_name = player_names[index]

                        if selected_player_slot == "X":

                            selected_x_player = selected_name

                        else:

                            selected_o_player = selected_name

                        menu_mode = "main"


        # ====================================================
        # NEW PLAYER
        # ====================================================

        elif menu_screen and menu_mode == "new":

            if event.type == pygame.KEYDOWN:

                # Back
                if event.key == pygame.K_ESCAPE:

                    menu_mode = "main"


                # Create
                elif event.key == pygame.K_RETURN:

                    name = new_player_name.strip()

                    if (
                        name != ""
                        and name not in players
                        and len(name) <= 18
                    ):

                        create_player(name)

                        # Automatically select new player
                        if selected_player_slot == "X":

                            selected_x_player = name

                        else:

                            selected_o_player = name

                        new_player_name = ""

                        menu_mode = "main"


                # Delete
                elif event.key == pygame.K_BACKSPACE:

                    new_player_name = (
                        new_player_name[:-1]
                    )


                # Type
                else:

                    if event.unicode.isprintable():

                        if len(new_player_name) < 18:

                            new_player_name += (
                                event.unicode
                            )


        # ====================================================
        # FINAL RESULT
        # ====================================================

        elif session_finished:

            if event.type == pygame.KEYDOWN:

                # New game
                if event.key == pygame.K_r:

                    reset_game()

                    session_finished = False


                # Main menu
                elif event.key == pygame.K_ESCAPE:

                    session_finished = False

                    session_history.clear()

                    menu_screen = True

                    menu_mode = "main"


        # ====================================================
        # GAME
        # ====================================================

        else:

            # ------------------------------------------------
            # MOUSE
            # ------------------------------------------------

            if event.type == pygame.MOUSEBUTTONDOWN:

                if (
                    winner is None
                    and not draw
                ):

                    mouse_x, mouse_y = event.pos


                    if (
                        mouse_x < BOARD_SIZE
                        and mouse_y < BOARD_SIZE
                    ):

                        row = (
                            mouse_y
                            // CELL_SIZE
                        )

                        col = (
                            mouse_x
                            // CELL_SIZE
                        )


                        if board[row][col] == "":

                            board[row][col] = (
                                current_player
                            )


                            current_game_moves.append({
                                "player": current_player,
                                "row": row,
                                "col": col
                            })


                            # Check winner
                            winner, winning_cells = (
                                check_winner()
                            )


                            # Check draw
                            if winner is None:

                                draw = check_draw()


                            # Save completed game
                            if (
                                winner is not None
                                or draw
                            ):

                                save_completed_game()


                            # Change turn
                            if (
                                winner is None
                                and not draw
                            ):

                                if current_player == "X":

                                    current_player = "O"

                                else:

                                    current_player = "X"


            # ------------------------------------------------
            # KEYBOARD
            # ------------------------------------------------

            if event.type == pygame.KEYDOWN:

                # Restart current level
                if event.key == pygame.K_r:

                    reset_game()


                # Clear all player data
                elif event.key == pygame.K_c:

                    players.clear()

                    save_data()

                    reset_game()


                # Finish session
                elif event.key == pygame.K_f:

                    if len(session_history) > 0:

                        session_finished = True


                # Back to menu
                elif event.key == pygame.K_ESCAPE:

                    session_history.clear()

                    menu_screen = True

                    menu_mode = "main"

                    reset_game()


    # ========================================================
    # DRAW
    # ========================================================

    if menu_screen:

        if menu_mode == "main":

            draw_main_menu()

        elif menu_mode == "select":

            draw_player_select()

        elif menu_mode == "new":

            draw_new_player()


    elif session_finished:

        draw_final_result()


    else:

        draw_game()


    pygame.display.update()


# ============================================================
# SAVE BEFORE EXIT
# ============================================================

save_data()

pygame.quit()