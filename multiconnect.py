from fastapi import FastAPI, HTTPException
from win10toast import ToastNotifier
from fastapi.responses import FileResponse
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
                        duration = 5,
                        icon_path=favicon_path)

@api.get('/disfile')
async def display(file_path):
    """
    Display the contents of a file.
    """
    if os.path.isfile(file_path):
        return FileResponse(file_path)
        # return FileResponse(path=file_path)
    return HTTPException(404, "File does not exist.")

@api.get('/dwlfile')
async def download(file_path):
    """
    Download the contents of a file.
    """
    if os.path.isfile(file_path):
        return FileResponse(file_path, media_type='application/octet-stream', filename=os.path.basename(file_path))
        # return FileResponse(path=file_path)
    return HTTPException(404, "File does not exist.")

if __name__ == '__main__':
    ##HOST = ''
    ##PORT = 1441
    HOST = input('Enter your IPv6 Address. > ')
    PORT = input('Enter desired Port. > ')
    PORT = int(PORT)
    print(f'Starting server on [{HOST}]:{PORT}.')
    print("Disregard errors speaking of NoneType. This is a module issue. Not MultiConnect.")
    uvicorn.run(api, host=HOST, port=PORT)
