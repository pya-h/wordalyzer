import pandas as pd
from views.dashboard import Dashboard
import models.manage as model_manager
import webbrowser
from threading import Thread, Timer
from termcolor import cprint
import colorama


if __name__ == '__main__':

    # for initializing colored printing (cprint) in python
    colorama.init()


    dataset = model_manager.db_load()
    model_manager.extract_words(dataset)

    # localhost:8050
    def open_browser():
        webbrowser.open("http://127.0.0.1:8050", new=0, autoraise=True)
        cprint("Dash server is now running... open http://127.0.0.1:8050 \n \t or http://localhost:8050 to access your dashboard.", "red")

    Timer(1.0, open_browser).start()
    # model_manager.testme()

    _ = Dashboard(graph_words_title = "Words Statistics:")
    _thread = Thread(target=_.run, args=[False, ]) # debug = false
    _thread.run()
