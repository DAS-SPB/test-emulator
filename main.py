from fastapi import FastAPI

from temu.api.endpoints import payment, order_update

PREFIX = "/test-emulator"

temu = FastAPI()
temu.include_router(payment.router, prefix=PREFIX)
temu.include_router(update_order.router, prefix=PREFIX)


@temu.get("/")
def read_root():
    return {"message": "Welcome to test emulator"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(temu, host="127.0.0.1", port=8000)
