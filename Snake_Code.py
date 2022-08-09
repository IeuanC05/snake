from pickle import NONE
import sys, pygame, random, os, operator

# Pygame start
pygame.init()

# Screensize variables
dis_width = 920
dis_height = 560

# Colours saved to variables
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
gold = (255, 215, 0)
grey = (50, 50, 50)
score_list = []
SCORE = 0
high_score = 0
keypress = False
settings = False
edges = False
game_started = False
snake_speed = 10
e_on_off = "OFF"
   
# Setting snake game screen size
dis = pygame.display.set_mode((dis_width, dis_height))

# Set game caption to 'Snake'
pygame.display.set_caption('Snake')

# set clock variable for snake speed limiting fps
clock = pygame.time.Clock()

# Set snake size
snake_block = 20

# Set game over font for game over screen
gameover_font = pygame.font.SysFont("timesnewroman", 75)
gameover_font2 = pygame.font.SysFont("timesnewroman", 25)

# Set score font
score_font = pygame.font.SysFont("calibri", 30)
score_font2 = pygame.font.SysFont("calibri", 15)
score_font3 = pygame.font.SysFont("calibri", 40)
start_font = pygame.font.SysFont("calibri", 100)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.environ.get("_MEIPASS2",os.path.abspath("."))

    return os.path.join(base_path, relative_path)

def score_save(score):
    f = open(resource_path("high_score.txt", "w"))
    f.write(score)
    f.close()

def highscore_find():
    f = open(resource_path("high_score.txt"))
    global high_score
    for line in f:
        if int(line) > high_score:
            high_score = int(line)
    return high_score
    f.close()

# Score function when called displays score on screen
def Score():
    value = score_font.render("YOUR SCORE: " + str(SCORE), True, white)
    dis.blit(value, [5, 5])
    #if high_score > 0:
    highscore_find()
    value2 = score_font.render("HIGH SCORE: " + str(high_score), True, white)
    dis.blit(value2, [(dis_width / 3) + 5, 5])

# snake function when called calls all snake attributes which builds players snake
def snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, green, [x[0], x[1], snake_block, snake_block])

# message function when called displays game over screen
def game_over_screen():
    mesg = gameover_font.render("YOU DIED", True, red)
    dis.blit(mesg, [275, 20])
    mesg2 = gameover_font2.render("PRESS ANY BUTTON TO CONTINUE!", True, red)
    dis.blit(mesg2, [250, 100])
    mesg1 = score_font3.render("Edges:  " + str(e_on_off), True, green)
    dis.blit(mesg1, [(dis_width / 2) - 85, 250])
    mesg2 = score_font3.render("Snake Speed:  " + str(snake_speed - 3), True, green)
    dis.blit(mesg2, [(dis_width / 2) - 130, 290])
    pygame.draw.rect(dis, gold, [20, 450, 200, 90]) 
    mesg3 = score_font.render("Settings(s)", True, black)
    dis.blit(mesg3, [55, 480])
    pygame.draw.rect(dis, gold, [700, 450, 200, 90]) 
    mesg3 = score_font.render("Play(p)", True, black)
    dis.blit(mesg3, [740, 480])
    f = open(resource_path("high_score.txt"))
    highscore_find()
    if os.stat(resource_path("high_score.txt")).st_size == 0:
        mesg3 = score_font.render("NEW HIGH SCORE  " + str(SCORE), True, white)
        dis.blit(mesg3, [310, 140])
        score_save(str(SCORE))
    else:
        if SCORE <= high_score:
            mesg3 = score_font.render("HIGH SCORE  " + str(high_score), True, white)
            dis.blit(mesg3, [335, 140])
            mesg4 = score_font.render("SCORE  " + str(SCORE), True, white)
            dis.blit(mesg4, [380, 175])
        elif SCORE > high_score:
            mesg3 = score_font.render("NEW HIGH SCORE  " + str(SCORE), True, white)
            dis.blit(mesg3, [310, 135])
            score_save(str(SCORE))
            
def gold_score(score):
    gold_value = score_font.render("GOLD APPLE POINTS:  " + str(score), True, gold)
    dis.blit(gold_value, [((dis_width / 3) * 2) + 5, 5])

def settings_menu():
    global e_on_off
    global snake_speed
    global SCORE
    global game_started
    global edges
    while True:
        if edges == True:
            e_on_off = "ON"
        elif edges == False:
            e_on_off = "OFF"
        dis.fill(black)
        pygame.draw.rect(dis, gold, [360, 175, 200, 90])
        mesg = score_font.render("Edges(e):  " + e_on_off, True, black)
        dis.blit(mesg, [375, 210])
        pygame.draw.rect(dis, gold, [700, 450, 200, 90])
        mesg1 = score_font.render("Play(p)", True, black)
        dis.blit(mesg1, [760, 485])
        pygame.draw.polygon(dis, gold, ((630, 285), (630, 385), (730, 335)))
        pygame.draw.polygon(dis, gold, ((290, 285), (290, 385), (190, 335)))
        pygame.draw.rect(dis, gold, [310, 285, 300, 100])
        mesg2 = score_font.render("Snake Speed(1-9):  " + str(snake_speed - 3), True, black)
        dis.blit(mesg2, [330, 320])
        pygame.display.update()
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    edges = not edges
                    game_started = True
                elif event.key == pygame.K_p:
                    game_started = True
                    clock.tick(snake_speed)
                    score_list.append(SCORE)
                    SCORE = 0
                    main()
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a and snake_speed > 4:
                    snake_speed -= 1
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d and snake_speed < 12:
                    snake_speed += 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mouse[0] >= 360 and mouse[1] >= 175 and mouse[0] <= 560 and mouse[1] <= 265:
                    edges = not edges
                    game_started = True
                elif mouse[0] >= 700 and mouse[1] >= 450 and mouse[0] <= 900 and mouse[1] <= 540:
                    game_started = True
                    clock.tick(snake_speed)
                    score_list.append(SCORE)
                    SCORE = 0
                    main()

def Start_Menu():
    global e_on_off
    global keypress
    global settings
    while keypress == False:
        clock.tick(60) 
        dis.fill(black)        
        mesg = start_font.render("SNAKE", True, green)
        dis.blit(mesg, [(dis_width / 2) - 140, 20])
        mesg1 = score_font3.render("Edges:  " + str(e_on_off), True, green)
        dis.blit(mesg1, [(dis_width / 2) - 85, 120])
        mesg2 = score_font3.render("Snake Speed:  " + str(snake_speed - 3), True, green)
        dis.blit(mesg2, [(dis_width / 2) - 130, 170])
        pygame.draw.rect(dis, gold, [20, 450, 200, 90]) 
        mesg3 = score_font.render("Settings(s)", True, black)
        dis.blit(mesg3, [55, 480])
        pygame.draw.rect(dis, gold, [700, 450, 200, 90]) 
        mesg4 = score_font.render("Play(p)", True, black)
        dis.blit(mesg4, [760, 480])
        pygame.display.update()
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos() 
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mouse[0] >= 20 and mouse[1] >= 450 and mouse[0] <= 220 and mouse[1] <= 540:
                    return settings_menu()
                elif mouse[0] >= 700 and mouse <= 900 and mouse[1] >= 450 and mouse[1] <= 540:
                    keypress = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    return settings_menu()
                elif event.key == pygame.K_p:
                    keypress = True

# main function happens when application runs
def main():
    # game_over variable set to False. When True game stops running
    game_over = False
    
    # game_close variable set to False. When True game over screen displayed
    game_close = False

    # Set snake speed
    global snake_speed

    # Sets initial player location
    player_x = snake_block * 24
    player_y = (snake_block * 12) + 40

    # Sets player movement distance
    x_change = 0
    y_change = 0

    # keeps track of snake length
    snake_List = []
    Length_of_snake = 1
    COUNTER = 0
    global SCORE
    global edges
    DIRECTION = NONE
    player_x_temp = player_x
    player_y_temp = player_y
    co_ords = 42
    g_points = 21

    # Sets apple location
    apple_x = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
    apple_y = round(random.randrange(40, dis_height - (40 + snake_block)) / 20.0) * 20.0
    gold_apple_x = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
    gold_apple_y = round(random.randrange(40, dis_height - (40 + snake_block)) / 20.0) * 20.0
    
    if game_started != True:
        Start_Menu()

    # main game loop
    while not game_over:

        # when player dies
        while game_close == True:
            
            # game over screen
            dis.fill(black)
            game_over_screen()
            pygame.display.update()
            clock.tick(60)

            # determines if player wants to quit or play again
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                    if event.type == pygame.QUIT:
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_s:
                            settings_menu()
                        elif event.key == pygame.K_p:
                            clock.tick(snake_speed)
                            score_list.append(SCORE)
                            SCORE = 0
                            main()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if mouse[0] >= 20 and mouse[0] <= 220 and mouse[1] >= 450 and mouse[1] <= 540:
                        settings_menu()
                    if mouse[0] >= 700 and mouse[0] <= 900 and mouse[1] >= 450 and mouse[1] <= 540:
                        clock.tick(snake_speed)
                        score_list.append(SCORE)
                        SCORE = 0
                        main()

        # If player quits during game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # Determines player direction based on button press
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if x_change != snake_block or Length_of_snake < 2:
                        x_change = -snake_block
                        y_change = 0
                        DIRECTION = 'left'
                        break
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if x_change != -snake_block or Length_of_snake < 2:
                        x_change = snake_block
                        y_change = 0
                        DIRECTION = 'right'
                        break
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    if y_change != snake_block or Length_of_snake < 2:
                        y_change = -snake_block
                        x_change = 0

                        DIRECTION = 'up'
                        break
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if y_change != -snake_block or Length_of_snake < 2:
                        y_change = snake_block
                        x_change = 0
                        DIRECTION = 'down'
                        break

        # If player hits edge of screen sends them to other side of display area
        if edges == False:
            if player_x > dis_width - (snake_block * 2) and DIRECTION == 'right':
                player_x = -snake_block
            elif player_x < snake_block and DIRECTION == 'left':
                player_x = dis_width
            elif player_y > dis_height - (snake_block * 2) and DIRECTION == 'down':
                player_y = snake_block
            elif player_y <= (snake_block * 2) + 5 and DIRECTION == 'up':
                player_y = dis_height
        elif edges == True:
            if player_x >= dis_width - (snake_block * 2) and DIRECTION == 'right':
                game_close = True
            elif player_y >= dis_height - (snake_block * 2) and DIRECTION == 'down':
                game_close = True
            elif player_x <= 0 + snake_block and DIRECTION == 'left':
                game_close = True
            elif player_y <= 0 + (snake_block * 3) and DIRECTION == 'up':
                game_close = True 

        # moves player based on previous input
        player_x += x_change
        player_y += y_change
        dis.fill(black)
        pygame.draw.rect(dis, red, [apple_x, apple_y, snake_block, snake_block])

        if COUNTER % 5 == 0 and COUNTER != 0 and co_ords < 43 and co_ords > 0 and g_points > 0:
            pygame.draw.rect(dis, gold, [gold_apple_x, gold_apple_y, snake_block, snake_block])
            if player_x_temp != player_x or player_y_temp != player_y:
                co_ords += 1
        elif g_points > 0 and g_points < 21:
            pygame.draw.rect(dis, gold, [gold_apple_x, gold_apple_y, snake_block, snake_block])
            if player_x_temp != player_x or player_y_temp != player_y:
                co_ords += 1
        else:
            gold_apple_x = -20
            gold_apple_y = -20
            co_ords = 0

        if co_ords < 43 and co_ords > 0 and co_ords % 2 == 0 and g_points > 0:
            g_points -= 1
            if g_points != 0:
                gold_score(g_points)
        elif g_points > 0 and g_points < 21:
            gold_score(g_points)

        if g_points == 0:
            pygame.draw.rect(dis, black, [gold_apple_x, gold_apple_y, snake_block, snake_block])
            
        player_x_temp = player_x
        player_y_temp = player_y

        snake_Head = []
        snake_Head.append(player_x)
        snake_Head.append(player_y)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        snake(snake_block, snake_List)
        Score()
        pygame.draw.line(dis, grey, (0, 40), (dis_width, 40), 1)
        pygame.draw.line(dis, grey, (dis_width / 3, 0), (dis_width / 3, 40), 1)
        pygame.draw.line(dis, grey, ((dis_width / 3) * 2, 0), ((dis_width / 3) * 2, 40), 1)
        if g_points >= 21 or g_points <= 0:
            gold_value = score_font.render("GOLD APPLE POINTS:  ", True, gold)
            dis.blit(gold_value, [((dis_width / 3) * 2) + 5, 5])        

        pygame.display.update()

        # if player co-ords are same as apple co-ords player gains point
        if player_x == apple_x and player_y == apple_y:
            apple_x = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
            apple_y = round(random.randrange(40, dis_height - (40 + snake_block)) / 20.0) * 20.0
            for x in snake_List:
                if x[0] == apple_x and x[1] == apple_y or apple_x == gold_apple_x and apple_y == gold_apple_y:
                    apple_x = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
                    apple_y = round(random.randrange(40, dis_height - (40 + snake_block)) / 20.0) * 20.0
                    continue
            Length_of_snake += 1
            SCORE += snake_speed - 3
            COUNTER += 1
            if COUNTER % 5 == 0:
                gold_apple_x = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
                gold_apple_y = round(random.randrange(40, dis_height - (40 + snake_block)) / 20.0) * 20.0
                for x in snake_List:
                    if x[0] == gold_apple_x and x[1] == gold_apple_y:
                        gold_apple_x = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
                        gold_apple_y = round(random.randrange(40, dis_height - (40 + snake_block)) / 20.0) * 20.0
                    continue
                co_ords += 1
                g_points = 21

        if player_x == gold_apple_x and player_y == gold_apple_y:
            gold_apple_x = -20
            gold_apple_y = -20
            Length_of_snake += 1
            SCORE += g_points
            g_points = 0
            co_ords = 0

        clock.tick(snake_speed)
            
    sys.exit()

main()