from controller.mainViewController import init_main_controller, lunch
from view.mainView import MainView


if __name__ == "__main__":
    main_v = MainView()
    init_main_controller(main_v)
    lunch()
    main_v.show()
