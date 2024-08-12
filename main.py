#!/usr/bin/env python3

import traceback
import tcod
import color
import exceptions
import input_handlers
import setup_game

def main() -> None:
    #setting dimensions
    screen_width = 80
    screen_height = 50


    #grabbing the image with letters
    tileset = tcod.tileset.load_tilesheet(
        "assests/images/letters.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    handler: input_handlers.BaseEventHandler = setup_game.MainMenu()

    #creating the terminal
    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Yet Another Rougelike Tutorial",
        vsync=True,
    ) as context: 
        #generates screen that will be drawn on
        root_console = tcod.console.Console(screen_width, screen_height, order="F")
        try:
            while True:
                #printing @ on screen
                root_console.clear()
                handler.on_render(console=root_console)
                context.present(root_console)

                try:
                    for event in tcod.event.wait():
                        context.convert_event(event)
                        handler = handler.handle_events(event)
                except Exception: #Handle exceptions in game.
                    traceback.print_exc() #Print error to stderr.
                    #Then print error to the message log.
                    if isinstance(handler, input_handlers.EventHandler):
                        handler.engine.message_log.add_message(
                            traceback.format_exc(), color.error
                        )
        except exceptions.QuitWithoutSaving:
            raise
        except SystemExit: #Save and quit.
            #TODO: Add the save function here
            raise
        except BaseException: #Save on any other unexpected exception.
            #TODO: Add the save function here
            raise

if __name__ == "__main__":
    main()