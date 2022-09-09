from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.cruds import tipo_documento_crud, evento_crud,makers_crud
from app.modules import registro_maker,asistencia,login,maker_qr

app = FastAPI()

'''
SECCION DONDE SE LLAMAN A LAS APIS DESARROLLADAS
'''
# CRUDS
app.include_router(tipo_documento_crud.router)
app.include_router(evento_crud.router)
app.include_router(makers_crud.router)
#app.include_router(ciudad_crud.router)

#MODULES
app.include_router(registro_maker.router)
app.include_router(asistencia.router)
app.include_router(login.router)
app.include_router(maker_qr.router)


'''
SECCION DONDE SE AGREGAN LOS CORS
'''
origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://congresohacedores.org",
    "https://prueba.congresohacedores.org",
    "https://registro.congresohacedores.org",
    "https://asistencia.congresohacedores.org"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


'''
SECCION DONDE SE INICIALIZA LA APLICACION
'''
@app.get("/")
async def root():
    return {"message": "WELCOME TO APP CONGRESO-HACEDORES"}

