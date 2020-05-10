try:
    from src.app import app
    
except ModuleNotFoundError:
    from app import app

if __name__ == "__main__":
    app.run()
