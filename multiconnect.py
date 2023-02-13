"""
User fastapi to allow connections from computers on the host's network by
routing it through the IPv6 address.
"""
from fastapi import FastAPI, HTTPException, Response
from win10toast import ToastNotifier
from fastapi.responses import FileResponse
import pyautogui
import uvicorn
import os

api = FastAPI()
notifier = ToastNotifier()


@api.get('/')
async def root():
    return "Hello, world!"


favicon_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'assets/favicon.ico')


@api.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


@api.get('/user')
async def currentuser():
    return f"Current Host User: {os.getlogin()}"


@api.get('/msg')
async def sendmsg(message):
    notifier.show_toast("MultiConnect",
                        msg=message,
                        duration=5,
                        icon_path=favicon_path)


@api.get('/disfile')
async def display(path):
    """
    Display the contents of a file.
    """
    if os.path.isfile(path):
        return FileResponse(path)
        # return FileResponse(path=path)
    return HTTPException(404, "File does not exist.")


@api.get('/dwlfile')
async def download(path):
    """
    Download the contents of a file.
    """
    if os.path.isfile(path):
        return FileResponse(path, media_type='application/octet-stream', filename=os.path.basename(path))
        # return FileResponse(path=path)
    return HTTPException(404, "File does not exist.")


@api.get('/showfiles')
async def show(path):
    """
    Show all files in a path.
    """
    try:
        return {f'files in {path} directory': os.listdir(path)}
    except NotADirectoryError:
        return HTTPException(406, 'directory is invalid.')
    except FileNotFoundError:
        return HTTPException(404, 'directory does not exist.')


@api.get('/getscreen')
async def screen():
    """
    Take a screenshot, save it as tmp.png, send it to the requester, then delete the temp file.
    """
    scrn = pyautogui.screenshot()
    scrn.save('tmp.png')
    with open('tmp.png', 'rb') as f:
        file = f.read()
    os.remove('tmp.png')
    return Response(content=file, media_type='image/png')

if __name__ == '__main__':
    ##HOST = ''
    ##PORT = 1441
    HOST = input('Enter your IPv6 Address. > ')
    PORT = input('Enter desired Port. > ')
    PORT = int(PORT)
    print(f'Starting server on [{HOST}]:{PORT}.')
    print("Disregard errors speaking of NoneType. This is a module issue. Not MultiConnect.")
    uvicorn.run(api, host=HOST, port=PORT)
