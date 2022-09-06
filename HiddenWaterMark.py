import PySimpleGUI as sg

# Main Function
def WaterMarkGen(img, watermark):
    pass
'''
The best way to go about this will be to create an Input Element as your target. 
Mark the Input Element as invisible so that it's not actually shown in the window. 
Also enable events for the Input Element. 
This will cause an event to be generated when someone chooses files. 
When you get this input element's key as the event, then parse the value of that field and fill in the listbox with the values.
'''
# UI
sg.theme('LightBlue2')

file_list = []

layout = [  [sg.Input(key = '_IN_'), sg.FilesBrowse(file_types = (('Image Files', '.jpg .png .bmp'), ), key='_FILES_')],
            [sg.Button('Add'), sg.Button('Delete')],
            [sg.Text('List of Image Files')],
            [sg.Listbox(file_list, s=(120, 5), key='_LISTBOX_')],
            [sg.Text('Watermark Text'), sg.Input(s=15), sg.Text('Rename'), sg.Input(s=30), \
                sg.Text('Choose Mode'), sg.Radio('Encode', 'mode', default=True), sg.Radio('Decode', 'mode')],
            [sg.Button('Start'), sg.Button('Close')]    ]


window = sg.Window('Hidden Watermark Generator', layout)

while True:
    event, values = window.read()

    # if user closes window or clicks cancel
    if event == sg.WIN_CLOSED or event == 'Close': 
        break

    elif event == '_LISTBOX_':
        selected = values
        print(selected)

    # Add and Delete Image Files
    if event == 'Add':
        file_list += values['_IN_'].split(';')
        window['_LISTBOX_'].update(file_list)
        # 중복 파일 제외하는 거 추가해야함



    if event == 'Delete':
        file_list.remove(selected)
        window['_LISTBOX_'].update(file_list)
        

    # Preview


    # Save Path 


    # Options (watermark text:input, rename:input)


    # Progress bar


    # Start and Close
    if event == 'Start':
        pass


'''
Next version's feature would be 'pattern generator'
It randomly generates a watermark algorithm and save it as a file. 
'''