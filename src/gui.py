import PySimpleGUI as sg
import device
import cv2
import imutils

device_list = device.getDeviceList()


recording, ret = False, False
cap = False

def make_window():

    
    sg.theme("DarkTeal9")
    layout_1 = [
         [sg.Text('Choose Camera'), sg.Combo(device_list, s=(15,22), enable_events=True, readonly=True, k='-COMBO-')],
         [sg.Text("Source Image"), sg.Button('Record', size=(10, 1))],
         [sg.Image(filename='', key='image')]
    ]

    layout = [[sg.Menu([['File', ['Exit']], ['Edit', ['Edit Me', ]]],  k='-CUST MENUBAR-',p=0)],
              [sg.Col(layout_1)]]

    window = sg.Window('The PySimpleGUI Element List', layout, finalize=False, right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_EXIT, keep_on_top=True)

    return window


# window = make_window()


sg.theme("DarkTeal9")
layout_1 = [
        [sg.Text('Choose Camera'), sg.Combo(device_list, s=(15,22), enable_events=True, readonly=True, k='-COMBO-')],
        [sg.Text("Source Image"), sg.Button('Record', size=(10, 1))],
        [sg.Image(filename='', key='image')]
]

layout = [[sg.Menu([['File', ['Exit']], ['Edit', ['Edit Me', ]]],  k='-CUST MENUBAR-',p=0)],
            [sg.Col(layout_1)]]

window = sg.Window('The PySimpleGUI Element List', layout, finalize=True, right_click_menu=sg.MENU_RIGHT_CLICK_EDITME_VER_EXIT, keep_on_top=True)



while True:
    event, values = window.read(timeout=10)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'Record':
        recording = True
    elif event == "-COMBO-":
        try:
            cap.release()
        except:
            pass
        index = device_list.index(values["-COMBO-"])
        cap = cv2.VideoCapture(int(index))

    try:
        ret, frame = cap.read()
        frame = imutils.resize(frame, width=300)
        imgbytes = cv2.imencode('.png', frame)[1].tobytes()
        window['image'].update(data=imgbytes)
    except:
        pass


window.close()