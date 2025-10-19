import os
import time
from models import Base, User, User_Photo, Output_Photo, Logs
from flask import Flask, request, jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select, func
from dotenv import load_dotenv
from datetime import datetime
from data import Get_Image_Data

load_dotenv()
app = Flask(__name__)
engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

UPLOAD_FOLDER = 'User_Data/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def current_milli_time():
    return round(time.time() * 1000)

@app.route("/")
def hello():
   return "Api Works"

@app.route("/signup", methods=["POST"])
def Signup():
    data = request.get_json()

    try:
        data = request.get_json()
        username = data.get("UserName")
        email = data.get("Email")
        password = data.get("Password")

        if not username or not email or not password:
            return jsonify({"error": "Missing username, email, or password"}), 400

        existing_user = session.query(User).filter(
            (User.UserName == username) | (User.Email == email)
        ).first()

        if existing_user:
            return jsonify({"error": "User with that username or email already exists"}), 409

        new_user = User(
            User_ID=current_milli_time(),
            Email=email,
            Password=password,
            UserName=username,
            Created_at=datetime.utcnow()
        )

        session.add(new_user)
        session.commit()

        return jsonify({
            "message": "Signup successful",
            "user": {
                "User_ID": new_user.User_ID,
                "UserName": new_user.UserName,
                "Email": new_user.Email,
                "Created_at": new_user.Created_at.isoformat()
            }
        }), 201

    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500

    finally:
        session.close()

@app.route("/login", methods=["POST"])
def Login():
    data = request.get_json()  

    if not data:
        return jsonify({"error": "Missing JSON body"}), 400
    
    UserName = data.get("UserName")
    Password = data.get("Password")

    if not UserName or not Password:
        return jsonify({"error": "Missing username or password"}), 400
    
    user = session.query(User).filter_by(UserName=UserName).first()
    if user and user.Password == Password:
        return jsonify({
            "message": "Login successful",
            "user": {
                "User_ID": user.User_ID,
                "Email": user.Email,
                "UserName": user.UserName,
                "Created_at": user.Created_at.isoformat()
            }
        }), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401
      
@app.route("/logs")
def Get_All_Logs(): 
    try:  
        logs = session.query(Logs).all()
        log_list = [
            {
                "Log_ID": log.Log_ID,
                "User_ID": log.User_ID,
                "User_Photo_ID": log.User_Photo_ID,
                "Output_Photo_ID": log.Output_Photo_ID,
                "Tags": log.Tags,
                "Description": log.Description,
                "Calibration": log.Calibration,
                "Created_at": log.Created_at.isoformat()
            }
            for log in logs
        ]
        return jsonify(log_list), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500

    finally:
        session.close()

@app.route("/logs/<int:user_id>", methods=["GET"])
def get_logs_by_user(user_id):
    try:
        logs = session.query(Logs).filter_by(User_ID=user_id).all()

        if not logs:
            return jsonify({"message": f"No logs found for user {user_id}"}), 404

        log_list = [
            {
                "Log_ID": log.Log_ID,
                "User_ID": log.User_ID,
                "User_Photo_ID": log.User_Photo_ID,
                "Output_Photo_ID": log.Output_Photo_ID,
                "Tags": log.Tags,
                "Description": log.Description,
                "Calibration": log.Calibration,
                "Created_at": log.Created_at.isoformat()
            }
            for log in logs
        ]
        return jsonify(log_list), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500

    finally:
        session.close()

@app.route("/Handle_Logging", methods=["POST"])
def Handle_Logging():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file = request.files['file']
    user_id = request.form.get("User_ID") 
    Title = request.form.get("Title")
    caption = request.form.get("Caption", "")
    location = request.form.get("Location", "")

    if not file or file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if not user_id:
        return jsonify({"error": "Missing User_ID"}), 400

    if file and allowed_file(file.filename):
        # Secure the filename
        filename = file.filename
        # Save to disk
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], user_id, filename)
        file.save(file_path)

        Data, img_path = Get_Image_Data(file_path)
        Photo_ID = current_milli_time()

        time.sleep(1)

        Output_Photo_ID = current_milli_time()
        new_photo = User_Photo(
            Photo_ID=Photo_ID,
            User_ID=user_id,
            Image_Url=file_path,
            Caption=caption,
            Location=location,
            Created_At=datetime.now()
        )

        New_Output_Photo = Output_Photo(
            Photo_ID = Output_Photo_ID,
            Image_Url = img_path,
            Created_At = datetime.now()
        )

        New_Log = Logs(
            Log_ID = current_milli_time(),
            User_ID = user_id,
            User_Photo_ID = Photo_ID,
            Output_Photo_ID = Output_Photo_ID,
            Title = Title,
            Tags = Data["tags"],
            Created_at = datetime.now(),
            Calibration =  Data["type"],
            Description = caption
        )

        # Store the path in the database
        
        session.add(new_photo)
        session.add(New_Log)
        session.add(New_Output_Photo)
        session.commit()

        return jsonify({
            "message": "File uploaded successfully",
            "file_path": file_path,
            "Photo_ID": new_photo.Photo_ID
        }), 201
    else:
        return jsonify({"error": "Invalid file type"}), 400



if __name__ == "__main__":
    app.run(debug=True)
