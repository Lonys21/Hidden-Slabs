import pygame
from menu import Menu
pygame.init()

# générer la fenêtre
pygame.display.set_caption("Hidden-Slabs")
icone = pygame.image.load('assets/Slab.png')
pygame.display.set_icon(icone)
screen = pygame.display.set_mode((1000, 1000))

clock = pygame.time.Clock()
FPS = 60

menu = Menu(screen, FPS)
running = True

while running:
    # Update Screenmanager
    if menu.init_finish:
        menu.update()

    # Reactualize the screen
    pygame.display.flip()

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        # Key Press
        elif event.type == pygame.KEYDOWN:
            # Player deplacements
            if menu.actual_screen == "game":
                if not menu.actual_game.player_dead:
                    if event.key == pygame.K_RIGHT:
                        menu.actual_game.player.move_right()
                    if event.key == pygame.K_LEFT:
                        menu.actual_game.player.move_left()
                    if event.key == pygame.K_UP:
                        menu.actual_game.player.move_up()
                    if event.key == pygame.K_DOWN:
                        menu.actual_game.player.move_down()

        # Mouse deplacements
        elif event.type == pygame.MOUSEMOTION:
            if menu.actual_screen == 'welcome':
                for button in menu.welcome_buttons:
                    if button.rect.collidepoint(event.pos):
                        button.image = button.image_mouse_on
                    else:
                        button.image = button.image_idle
            elif menu.actual_screen == 'tuto':
                if menu.tuto.next_button.rect.collidepoint(event.pos):
                    menu.tuto.next_button.image = menu.tuto.next_button.image_mouse_on
                else:
                    menu.tuto.next_button.image = menu.tuto.next_button.image_idle

            elif menu.actual_screen == "menu":
                for button in menu.menu_buttons:
                    if button.rect.collidepoint(event.pos):
                        button.image = button.image_mouse_on
                    else:
                        button.image = button.image_idle
            elif menu.actual_screen == 'win' or 'loose':
                if menu.menu_button.rect.collidepoint(event.pos):
                    menu.menu_button.image = menu.menu_button.image_mouse_on
                else:
                    menu.menu_button.image = menu.menu_button.image_idle

        # Mouseclick
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if menu.actual_screen == 'welcome':
                for button in menu.welcome_buttons:
                    if button.rect.collidepoint(event.pos):
                        button.image = button.image_press
            elif menu.actual_screen == 'tuto':
                if menu.tuto.next_button.rect.collidepoint(event.pos):
                    menu.tuto.next_button.image = menu.tuto.next_button.image_press
            elif menu.actual_screen == "menu":
                for button in menu.menu_buttons:
                    if button.rect.collidepoint(event.pos):
                        button.image = button.image_press
            elif menu.actual_screen == "win" or 'loose':
                if menu.menu_button.rect.collidepoint(event.pos):
                    menu.menu_button.image = menu.menu_button.image_press

        # Mouseclick up
        elif event.type == pygame.MOUSEBUTTONUP:
            # welcome_button
            if menu.actual_screen == 'welcome':
                for button in menu.welcome_buttons:
                    if button.rect.collidepoint(event.pos):
                        if button == menu.welcome_button_menu:
                            menu.actual_screen = 'menu'
                        elif button == menu.welcome_button_tutoriel:
                            menu.actual_screen = 'tuto'
            elif menu.actual_screen == 'tuto':
                if menu.tuto.next_button.rect.collidepoint(event.pos):
                    menu.tuto.next()
            # menu_buttons
            elif menu.actual_screen == 'menu':
                for button in menu.menu_buttons:
                    if button.rect.collidepoint(event.pos):
                        if button == menu.easy_button:
                            menu.launch('simple', 5, 5)
                        elif button == menu.medium_button:
                            menu.launch('simple', 10, 5)
                        elif button == menu.hard_button:
                            menu.launch('simple', 10, 10, )
                        elif button == menu.timer_button:
                            menu.launch('timer', 5, 5)
            # button to menu
            elif menu.actual_screen == 'win' or 'loose':
                if menu.menu_button.rect.collidepoint(event.pos):
                    menu.actual_screen = 'menu'

    clock.tick(FPS)



