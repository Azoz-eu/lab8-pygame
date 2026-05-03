# Architecture Documentation

## Scope
This document captures the concrete architecture of the current project implementation in main.py.
The file main(old).py is present as legacy code and is not imported or executed by the current entry path.

## Source Inventory
- Runtime entry point: main.py
- Primary classes: Game, Square
- Runtime library: pygame
- Supporting libraries: random, math, typing
- Legacy snapshot: main(old).py

## Dependency Graph
```mermaid
graph TD
    Main["main.py"]
    Legacy["main(old).py"]
    Pygame["pygame"]
    Random["random"]
    Math["math"]
    Typing["typing.List"]

    Main --> Pygame
    Main --> Random
    Main --> Math
    Main --> Typing
    Legacy --> Pygame
    Legacy --> Random
    Legacy --> Math
    Legacy --> Typing
```

Notes:
- main.py is the active module used by the program entry guard.
- main(old).py is currently disconnected from runtime execution.

## High-Level Runtime Flow
```mermaid
flowchart TD
    Start["Process Start"] --> Guard["if __name__ == '__main__'"]
    Guard --> GameInit["Game.__init__()"]
    GameInit --> InitPygame["pygame.init()"]
    InitPygame --> Window["Create Display and Clock"]
    Window --> CreateSquares["Create List[Square]"]
    CreateSquares --> Run["Game.run()"]

    Run --> LoopCheck{"running is True"}
    LoopCheck -->|"Yes"| HandleEvents["Game.handle_events()"]
    HandleEvents --> Update["Game.update()"]
    Update --> Draw["Game.draw()"]
    Draw --> Tick["clock.tick(FPS)"]
    Tick --> LoopCheck

    LoopCheck -->|"No"| Quit["pygame.quit()"]
    Quit --> End["Process End"]
```

## Function-Level Call Graph
```mermaid
graph TD
    Entry["__main__ block"] --> NewGame["Game()"]
    Entry --> RunCall["Game.run()"]

    NewGame --> PyInit["pygame.init()"]
    NewGame --> SetMode["pygame.display.set_mode()"]
    NewGame --> SetCaption["pygame.display.set_caption()"]
    NewGame --> NewClock["pygame.time.Clock()"]
    NewGame --> NewFont["pygame.font.SysFont()"]
    NewGame --> BuildSquares["[Square(...) for _ in range(NUM_SQUARES)]"]

    BuildSquares --> SquareInit["Square.__init__()"]
    SquareInit --> RandSize["random.randint()"]
    SquareInit --> RandPos["random.randint()"]
    SquareInit --> RandVel["random.choice() + random.uniform()"]
    SquareInit --> RandColor["random.randint()"]

    RunCall --> HandleEvents["Game.handle_events()"]
    RunCall --> Update["Game.update()"]
    RunCall --> Draw["Game.draw()"]
    RunCall --> Tick["clock.tick(FPS)"]
    RunCall --> Quit["pygame.quit()"]

    HandleEvents --> EventGet["pygame.event.get()"]

    Update --> SquareUpdate["Square.update(all_squares)"]
    SquareUpdate --> Jitter["random.uniform()"]
    SquareUpdate --> Dist["math.sqrt()"]
    SquareUpdate --> Speed["math.hypot()"]
    SquareUpdate --> Target["Square.target_speed()"]

    Draw --> Fill["screen.fill()"]
    Draw --> SquareDraw["Square.draw(surface)"]
    Draw --> FpsRender["font.render()"]
    Draw --> Blit["screen.blit()"]
    Draw --> Flip["pygame.display.flip()"]
    SquareDraw --> DrawRect["pygame.draw.rect()"]
```

## Primary Execution Sequence
```mermaid
sequenceDiagram
    participant U as "User"
    participant OS as "OS Window System"
    participant M as "main.py"
    participant G as "Game"
    participant S as "Square[*]"
    participant P as "pygame"

    U->>M: "Run python main.py"
    M->>G: "Create Game()"
    G->>P: "init()"
    G->>P: "display.set_mode()"
    G->>P: "display.set_caption()"
    G->>P: "time.Clock()"
    G->>P: "font.SysFont()"
    loop "Create NUM_SQUARES"
        G->>S: "Square.__init__(screen_width, screen_height)"
    end

    M->>G: "run()"
    loop "While running"
        G->>P: "event.get()"
        alt "QUIT or ESC pressed"
            OS-->>G: "Quit event or Escape key"
            G->>G: "running = False"
        else "No exit event"
            G->>G: "running stays True"
        end

        loop "For each square"
            G->>S: "update(all_squares)"
            S->>S: "apply jitter"
            S->>S: "compute flee from larger nearby squares"
            S->>S: "normalize to target speed"
            alt "Hit horizontal wall"
                S->>S: "invert vx"
            else "No horizontal collision"
                S->>S: "keep vx"
            end
            alt "Hit vertical wall"
                S->>S: "invert vy"
            else "No vertical collision"
                S->>S: "keep vy"
            end
        end

        G->>P: "screen.fill(black)"
        loop "For each square"
            G->>S: "draw(surface)"
            S->>P: "draw.rect(...)"
        end
        G->>P: "font.render(FPS text)"
        G->>P: "screen.blit(...)"
        G->>P: "display.flip()"
        G->>P: "clock.tick(FPS)"
    end

    G->>P: "quit()"
```

## Assumptions and Boundaries
- The architecture reflects the code currently in main.py.
- main(old).py is documented for dependency visibility but excluded from runtime flow because there is no import or call path from main.py to main(old).py.
- No external service, database, or network boundary is present in this project.
