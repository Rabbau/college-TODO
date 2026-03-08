"""Текущий урок 3.8"""


from fastapi import FastAPI
from handlers import routers 


app = FastAPI()

for router in routers:
    app.include_router(router=router)

'''
    При проблемах с завершением сервера uvicorn:

netstat -ano | findstr :8000 
taskkill /PID {pid} /F

'''