from symbol import pass_stmt
import pygame
import sys
from const import *
from game import Game
from square import Square
from move import Move

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game()

    def mainloop(self):

        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger

        while True:
            #show methods
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():
                
                # click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece

                        # valid piece
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)

                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                # motion
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE
                    game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        # show methods
                        game.show_bg(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)
                # free
                elif event.type == pygame.MOUSEBUTTONUP:

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        relased_row = dragger.mouseY // SQSIZE
                        relased_col = dragger.mouseX // SQSIZE

                        # create possible move
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(relased_row, relased_col)
                        move = Move(initial, final)

                        if board.valid_move(dragger.piece, move):
                            captured = board.squares[relased_row][relased_col].has_piece()

                            board.move(dragger.piece, move)
                            # sound
                            game.play_sound(captured)

                            #show methods
                            game.show_bg(screen)  
                            game.show_last_move(screen)
                            game.show_pieces(screen)      

                            # next turn
                            game.next_turn()                  

                    dragger.undrag_piece()

                # key press
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        # change theme
                        game.change_theme()

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

main = Main()
main.mainloop()