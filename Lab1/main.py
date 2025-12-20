from fastapi import FastAPI
from src.controller.product import router
import uvicorn
app = FastAPI(
    title='API',
    description='Zarządzanie produktami - Laboratorium 1'
)

app.include_router(router)



if __name__ == '__main__':

    uvicorn.run(app, host='0.0.0.0', port=8005)