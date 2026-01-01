import pygame
import sys
import time
import numpy as np
from sudoko import generate_full_grid, make_puzzle
from sudokuDFS import solve_sudoku as solve_dfs
from CSP import SudokoCSP

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 900
HEIGHT = 700
GRID_SIZE = 540
CELL_SIZE = GRID_SIZE // 9
SIDEBAR_WIDTH = WIDTH - GRID_SIZE
BUTTON_HEIGHT = 50
PADDING = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (240, 240, 240)
DARK_GRAY = (100, 100, 100)
BLUE = (52, 152, 219)
LIGHT_BLUE = (174, 214, 241)
GREEN = (46, 204, 113)
RED = (231, 76, 60)
ORANGE = (230, 126, 34)
PURPLE = (155, 89, 182)
YELLOW = (241, 196, 15)

# Fonts
FONT_LARGE = pygame.font.Font(None, 48)
FONT_MEDIUM = pygame.font.Font(None, 36)
FONT_SMALL = pygame.font.Font(None, 24)
FONT_TINY = pygame.font.Font(None, 20)


class SudokuGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Sudoku Solver - DFS vs CSP Comparison")
        self.clock = pygame.time.Clock()
        
        self.difficulty = "medium"
        self.original_grid = None
        self.current_grid = None
        self.solution_grid = None
        
        self.solving_results = {
            "DFS": {"time": 0, "solved": False},
            "CSP": {"time": 0, "solved": False}
        }
        
        self.show_dashboard = False
        self.game_active = True
        
        self.generate_new_puzzle()
    
    def generate_new_puzzle(self):
        """Generate a new Sudoku puzzle"""
        self.solution_grid = generate_full_grid()
        self.original_grid = make_puzzle(self.solution_grid, difficulty=self.difficulty)
        self.current_grid = [row[:] for row in self.original_grid]
        self.show_dashboard = False
        self.solving_results = {
            "DFS": {"time": 0, "solved": False},
            "CSP": {"time": 0, "solved": False}
        }
    
    def solve_with_dfs(self):
        """Solve using DFS backtracking"""
        grid_copy = [row[:] for row in self.original_grid]
        start_time = time.time()
        solved = solve_dfs(grid_copy)
        end_time = time.time()
        
        self.solving_results["DFS"]["time"] = end_time - start_time
        self.solving_results["DFS"]["solved"] = solved
        
        if solved:
            self.current_grid = grid_copy
        
        return solved
    
    def solve_with_csp(self):
        """Solve using CSP with AC3"""
        grid_copy = [row[:] for row in self.original_grid]
        grid_np = np.array(grid_copy)
        
        start_time = time.time()
        csp_solver = SudokoCSP(grid_np)
        solved = csp_solver.solve()
        end_time = time.time()
        
        self.solving_results["CSP"]["time"] = end_time - start_time
        self.solving_results["CSP"]["solved"] = solved
        
        if solved:
            self.current_grid = csp_solver.grid.tolist()
        
        return solved
    
    def solve_all_methods(self):
        """Solve using both methods and show dashboard"""
        # Solve with DFS
        self.current_grid = [row[:] for row in self.original_grid]
        try:
            self.solve_with_dfs()
        except Exception as e:
            print(f"Error solving with DFS: {e}")
            self.solving_results["DFS"]["solved"] = False
        
        # Solve with CSP
        self.current_grid = [row[:] for row in self.original_grid]
        try:
            self.solve_with_csp()
        except Exception as e:
            print(f"Error solving with CSP: {e}")
            self.solving_results["CSP"]["solved"] = False
        
        self.show_dashboard = True
    
    def draw_grid(self):
        """Draw the Sudoku grid"""
        # Draw cells
        for row in range(9):
            for col in range(9):
                x = col * CELL_SIZE + PADDING
                y = row * CELL_SIZE + PADDING
                
                # Draw cell background
                if self.original_grid[row][col] != 0:
                    pygame.draw.rect(self.screen, LIGHT_GRAY, (x, y, CELL_SIZE, CELL_SIZE))
                else:
                    pygame.draw.rect(self.screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))
                
                # Draw cell border
                pygame.draw.rect(self.screen, GRAY, (x, y, CELL_SIZE, CELL_SIZE), 1)
                
                # Draw number
                if self.current_grid[row][col] != 0:
                    num = str(self.current_grid[row][col])
                    if self.original_grid[row][col] != 0:
                        color = BLACK
                        font = FONT_MEDIUM
                    else:
                        color = BLUE
                        font = FONT_MEDIUM
                    
                    text = font.render(num, True, color)
                    text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                    self.screen.blit(text, text_rect)
        
        # Draw thick lines for 3x3 boxes
        for i in range(4):
            thickness = 3
            # Vertical lines
            pygame.draw.line(self.screen, BLACK, 
                           (i * 3 * CELL_SIZE + PADDING, PADDING), 
                           (i * 3 * CELL_SIZE + PADDING, GRID_SIZE + PADDING), 
                           thickness)
            # Horizontal lines
            pygame.draw.line(self.screen, BLACK, 
                           (PADDING, i * 3 * CELL_SIZE + PADDING), 
                           (GRID_SIZE + PADDING, i * 3 * CELL_SIZE + PADDING), 
                           thickness)
    
    def draw_button(self, text, x, y, width, height, color, text_color=WHITE):
        """Draw a button and return its rect"""
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, color, rect, border_radius=8)
        pygame.draw.rect(self.screen, DARK_GRAY, rect, 2, border_radius=8)
        
        text_surface = FONT_SMALL.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
        
        return rect
    
    def draw_sidebar(self):
        """Draw the sidebar with controls"""
        sidebar_x = GRID_SIZE + PADDING * 2
        y_offset = PADDING
        
        # Title
        title = FONT_MEDIUM.render("Controls", True, BLACK)
        self.screen.blit(title, (sidebar_x, y_offset))
        y_offset += 60
        
        # Difficulty selection
        diff_text = FONT_SMALL.render("Difficulty:", True, BLACK)
        self.screen.blit(diff_text, (sidebar_x, y_offset))
        y_offset += 35
        
        button_width = (SIDEBAR_WIDTH - PADDING * 3) // 3
        difficulties = ["easy", "medium", "hard"]
        self.difficulty_buttons = {}
        
        for i, diff in enumerate(difficulties):
            color = GREEN if self.difficulty == diff else GRAY
            x = sidebar_x + i * (button_width + 10)
            rect = self.draw_button(diff.capitalize(), x, y_offset, button_width - 10, 40, color)
            self.difficulty_buttons[diff] = rect
        
        y_offset += 60
        
        # New game button
        self.new_game_button = self.draw_button("New Game", sidebar_x, y_offset, 
                                                SIDEBAR_WIDTH - PADDING * 2, BUTTON_HEIGHT, BLUE)
        y_offset += BUTTON_HEIGHT + 20
        
        # Solve buttons
        solve_text = FONT_SMALL.render("Solve with:", True, BLACK)
        self.screen.blit(solve_text, (sidebar_x, y_offset))
        y_offset += 35
        
        self.solve_dfs_button = self.draw_button("DFS Backtracking", sidebar_x, y_offset, 
                                                 SIDEBAR_WIDTH - PADDING * 2, BUTTON_HEIGHT, ORANGE)
        y_offset += BUTTON_HEIGHT + 10
        
        self.solve_csp_button = self.draw_button("CSP (AC-3)", sidebar_x, y_offset, 
                                                 SIDEBAR_WIDTH - PADDING * 2, BUTTON_HEIGHT, PURPLE)
        y_offset += BUTTON_HEIGHT + 20
        
        # Compare all button
        self.compare_all_button = self.draw_button("Compare Both Methods", sidebar_x, y_offset, 
                                                   SIDEBAR_WIDTH - PADDING * 2, BUTTON_HEIGHT, GREEN)
    
    def draw_dashboard(self):
        """Draw the comparison dashboard"""
        # Semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(230)
        overlay.fill(WHITE)
        self.screen.blit(overlay, (0, 0))
        
        # Dashboard container
        dash_width = 700
        dash_height = 450
        dash_x = (WIDTH - dash_width) // 2
        dash_y = (HEIGHT - dash_height) // 2
        
        pygame.draw.rect(self.screen, WHITE, (dash_x, dash_y, dash_width, dash_height), border_radius=15)
        pygame.draw.rect(self.screen, BLUE, (dash_x, dash_y, dash_width, dash_height), 3, border_radius=15)
        
        # Title
        title = FONT_LARGE.render("Algorithm Comparison", True, BLUE)
        title_rect = title.get_rect(center=(WIDTH // 2, dash_y + 40))
        self.screen.blit(title, title_rect)
        
        # Results
        y_offset = dash_y + 110
        methods = ["DFS", "CSP"]
        colors = [ORANGE, PURPLE]
        
        # Find fastest method
        fastest_time = float('inf')
        fastest_method = None
        for method in methods:
            if self.solving_results[method]["solved"] and self.solving_results[method]["time"] < fastest_time:
                fastest_time = self.solving_results[method]["time"]
                fastest_method = method
        
        for i, (method, color) in enumerate(zip(methods, colors)):
            result = self.solving_results[method]
            
            # Method name with full description
            if method == "DFS":
                display_name = "DFS Backtracking"
            else:
                display_name = "CSP (AC-3)"
                
            method_text = FONT_MEDIUM.render(display_name, True, color)
            self.screen.blit(method_text, (dash_x + 50, y_offset))
            
            # Status and time
            if result["solved"]:
                status = "✓ Solved"
                status_color = GREEN
                time_text = f"{result['time']:.4f}s"
                
                # Mark fastest
                if method == fastest_method:
                    trophy = FONT_MEDIUM.render("🏆", True, YELLOW)
                    self.screen.blit(trophy, (dash_x + 320, y_offset))
            else:
                status = "✗ Failed"
                status_color = RED
                time_text = "N/A"
            
            status_surface = FONT_SMALL.render(status, True, status_color)
            self.screen.blit(status_surface, (dash_x + 380, y_offset + 5))
            
            time_surface = FONT_SMALL.render(time_text, True, BLACK)
            self.screen.blit(time_surface, (dash_x + 530, y_offset + 5))
            
            # Progress bar (visual representation)
            if result["solved"] and fastest_time > 0:
                bar_width = 300
                bar_height = 25
                bar_x = dash_x + 50
                bar_y = y_offset + 45
                
                # Background
                pygame.draw.rect(self.screen, LIGHT_GRAY, (bar_x, bar_y, bar_width, bar_height), border_radius=5)
                
                # Filled portion
                solved_times = [r["time"] for r in self.solving_results.values() if r["solved"]]
                if solved_times:
                    max_time = max(solved_times)
                    fill_width = int((result["time"] / max_time) * bar_width)
                    pygame.draw.rect(self.screen, color, (bar_x, bar_y, fill_width, bar_height), border_radius=5)
                
                # Border
                pygame.draw.rect(self.screen, DARK_GRAY, (bar_x, bar_y, bar_width, bar_height), 2, border_radius=5)
            
            y_offset += 120
        
        # Close button
        self.close_dashboard_button = self.draw_button("Close & Play Again", 
                                                       WIDTH // 2 - 150, dash_y + dash_height - 70, 
                                                       300, 50, BLUE)
    
    def handle_click(self, pos):
        """Handle mouse clicks"""
        if self.show_dashboard:
            if hasattr(self, 'close_dashboard_button') and self.close_dashboard_button.collidepoint(pos):
                self.show_dashboard = False
                self.generate_new_puzzle()
            return
        
        # Difficulty buttons
        for diff, rect in self.difficulty_buttons.items():
            if rect.collidepoint(pos):
                self.difficulty = diff
                self.generate_new_puzzle()
                return
        
        # New game button
        if self.new_game_button.collidepoint(pos):
            self.generate_new_puzzle()
            return
        
        # Solve buttons
        if self.solve_dfs_button.collidepoint(pos):
            self.solve_with_dfs()
            return
        
        if self.solve_csp_button.collidepoint(pos):
            self.solve_with_csp()
            return
        
        if self.compare_all_button.collidepoint(pos):
            self.solve_all_methods()
            return
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            self.screen.fill(WHITE)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        self.handle_click(event.pos)
            
            if not self.show_dashboard:
                self.draw_grid()
                self.draw_sidebar()
            else:
                self.draw_grid()
                self.draw_dashboard()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = SudokuGame()
    game.run()