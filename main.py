"""Текущий урок 3.8"""


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from handlers import routers 


# made by леша start
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# made by леша end

app.mount("/static", StaticFiles(directory="static"), name="static")

for router in routers:
    app.include_router(router=router)

'''
    При проблемах с завершением сервера uvicorn:

netstat -ano | findstr :8000 
taskkill /PID {pid} /F

'''
