from collections import defaultdict

from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from motor import motor_asyncio

from config import BaseConfig
from routers import cars_router, users_router

settings = BaseConfig()

# define origins
origins = ["*"]


async def lifespan(app: FastAPI):
    app.client = motor_asyncio.AsyncIOMotorClient(settings.DB_URL)
    app.db = app.client[settings.DB_NAME]

    try:
        app.client.admin.command("ping")
        print("Pinged your deployment. You have successfully connected to MongoDB!")
        print("Mongo address:", settings.DB_URL)
    except Exception as e:
        print(e)
    yield
    app.client.close()


app = FastAPI(lifespan=lifespan)


# add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def custom_form_validation_error(request, exc):
    reformatted_message = defaultdict(list)
    for pydantic_error in exc.errors():
        loc, msg = pydantic_error["loc"], pydantic_error["msg"]
        filtered_loc = loc[1:] if loc[0] in ("body", "query", "path") else loc
        # nested fields with dot-notation
        field_string = ".".join(filtered_loc)
        reformatted_message[field_string].append(msg)

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            {"detail": "Invalid request", "errors": reformatted_message}
        ),
    )


app.include_router(cars_router, prefix="/cars", tags=["cars"])
app.include_router(users_router, prefix="/users", tags=["users"])


@app.get("/")
async def get_root():
    return {"Message": "Root working"}
