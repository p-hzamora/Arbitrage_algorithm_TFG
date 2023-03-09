from pynput.keyboard import Key, Listener, Controller

def on_press(key):  # The function that's called when a key is pressed
    global add
    if key == Key.space:
        print(' ', end= "")
    elif key == Key.esc:
        # Stop listener
        return False
    elif key == Key.enter:
        print('')
    else:
        add.append(key)
        print(str(key), end="")

    # if 'char' ina dir(key):     #check if char method exists,
    #     if key.char == 'q':
    #         print("quit")
add = []	
with Listener(on_press=lambda event: on_press(event)) as listener:
    #your code
    listener.join()