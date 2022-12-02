import pandas as pd
from views.dashboard import Dashboard
from views.dataset_manager import DatasetManager
import models.manage as model_manager
import webbrowser
from threading import Thread, Timer
from termcolor import cprint
import colorama

def new_dashboard(database=None, port=8000, domain="http://127.0.0.1"):

    dataset = model_manager.db_load(database)
    model_manager.extract_words(dataset)

    # localhost:PORT
    def open_browser():
        webbrowser.open(f"{domain}:{port}", new=0, autoraise=True)
        cprint("Dash server is now running... open {domain}:{port} \n \t to access your dashboard.", "red")

    Timer(1.0, open_browser).start()
    # model_manager.testme()

    _ = Dashboard(graph_words_title = "Words Statistics:")
    _thread = Thread(target=_.run, args=[True, ]) # debug = false
    _thread.run()


if __name__ == '__main__':

    # for initializing colored printing (cprint) in python
    colorama.init()

    main = DatasetManager(new_dashboard)
    main_thread = Thread(target=main.show)
    main_thread.run()
