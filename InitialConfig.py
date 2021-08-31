from PyQt5.QtCore import QSettings, QSize, QPoint


def initiation(app):
    settings_init()

    initial_configure_size(app, 0.9, 0.6, 0.2, 0.5)

    settings = QSettings("MySoft", "DropdownMenu")
    settings.setValue("Initial/is_initiated", True)


def settings_init():

    settings = QSettings("MySoft", "DropdownMenu")  # TODO org name
    print("Settings in ", settings.fileName())

    settings.setValue("Initial/is_initiated", False)

    # settings.beginGroup("Screen")
    # settings.value("main_frame_geometry")
    # settings.value("main_pos")
    # settings.value("sett_frame_geometry")
    # settings.value("sett_pos")
    # settings.endGroup()
    # settings.value("Hotkey/open_hotkey")

    return settings


def initial_configure_size(app, w_mul, h_mul, settings_w_mul, settings_h_mul):
    screen = app.primaryScreen()

    size = screen.size()

    main_window_w = size.width() * w_mul
    main_window_h = size.height() * h_mul

    main_window_off_w = (size.width() - main_window_w) // 2

    settings_window_w = size.width() * settings_w_mul
    settings_window_h = size.height() * settings_h_mul

    settings = QSettings("MySoft", "DropdownMenu")
    settings.beginGroup("Screen")
    settings.setValue("main_frame_geometry", QSize(main_window_w, main_window_h))
    settings.setValue("main_pos", QPoint(main_window_off_w, 0))
    settings.setValue("sett_frame_geometry", QSize(settings_window_w, settings_window_h))
    settings.setValue("sett_pos", "Center")
    settings.endGroup()

    for key in settings.allKeys():
        print(f"{key} == {settings.value(key)}")

    # size = {"main_window_w": main_window_w,
    #         "main_window_h": main_window_h,
    #         "main_window_off_w": main_window_off_w,
    #         "settings_window_w": settings_window_w,
    #         "settings_window_h": settings_window_h}
    #
    # return size
