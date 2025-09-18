from app import create_app
import os
from dotenv import load_dotenv
from flask_cors import CORS




load_dotenv()

app=create_app()
CORS(app) #ALL ORIGINS
if __name__=='__main__':
    
    app.run(debug=True)