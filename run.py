from app.main import app
import firebase_admin

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", reload=True)
