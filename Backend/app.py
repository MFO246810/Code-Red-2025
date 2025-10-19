import os
import time
from models import Base, User, User_Photo, Output_Photo, Logs
from flask import Flask, request, jsonify, send_from_directory
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select, func
from dotenv import load_dotenv
from datetime import datetime
from data import Get_Image_Data
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)
engine = create_engine(os.getenv("DATABASE_URL"), echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
CORS(app)

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
        log_list = []
        for log in logs:
            user_photo = session.query(User_Photo).filter_by(Photo_ID=log.User_Photo_ID).first()
            output_photo = session.query(Output_Photo).filter_by(Photo_ID=log.Output_Photo_ID).first()

            log_list.append({
                "Log_ID": log.Log_ID,
                "User_ID": log.User_ID,
                "User_Photo": user_photo.Image_Url if user_photo else None,
                "Output_Photo": output_photo.Image_Url if output_photo else None,
                "Tags": log.Tags,
                "Description": log.Description,
                "Calibration": log.Calibration,
                "Created_at": log.Created_at.isoformat(),
                "Location": user_photo.Location if user_photo and hasattr(user_photo, "Location") else None
            })

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

        log_list = []
        for log in logs:
            user_photo = session.query(User_Photo).filter_by(Photo_ID=log.User_Photo_ID).first()
            output_photo = session.query(Output_Photo).filter_by(Photo_ID=log.Output_Photo_ID).first()

            log_list.append({
                "Log_ID": log.Log_ID,
                "User_ID": log.User_ID,
                "User_Photo": user_photo.Image_Url if user_photo else None,
                "Output_Photo": output_photo.Image_Url if output_photo else None,
                "Tags": log.Tags,
                "Description": log.Description,
                "Calibration": log.Calibration,
                "Created_at": log.Created_at.isoformat(),
                "Location": user_photo.Location if user_photo and hasattr(user_photo, "Location") else None
            })

        return jsonify(log_list), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500

    finally:
        session.close()

@app.route("/Current_logs/<int:log_id>", methods=["GET"])
def get_logs_by_id(log_id):
    print(log_id)
    try:
        # Find the log in the database
        log = session.query(Logs).filter_by(Log_ID=log_id).first()
        if not log:
            return jsonify({"error": "Log not found"}), 404

        # Fetch related images from User_Photo and Output_Photo
        user_photo = session.query(User_Photo).filter_by(Photo_ID=log.User_Photo_ID).first()
        output_photo = session.query(Output_Photo).filter_by(Photo_ID=log.Output_Photo_ID).first()

        # Build the response
        log_data = {
            "Log_ID": log.Log_ID,
            "User_ID": log.User_ID,
            "Title": log.Title,
            "Tags": log.Tags,
            "Calibration": log.Calibration,
            "Description": log.Description,
            "Created_at": log.Created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "User_Photo": user_photo.Image_Url if user_photo else None,
            "Output_Photo": output_photo.Image_Url if output_photo else None,
            "Location": user_photo.Location if user_photo and hasattr(user_photo, "Location") else None
        }

        return jsonify(log_data), 200

    except Exception as e:
        print(f"Error fetching log: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

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
        user_upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], user_id)
        os.makedirs(user_upload_dir, exist_ok=True)
        file_path = file_path = os.path.join(user_upload_dir, filename)
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
            Tags = ", ".join(Data["tags"]),
            Created_at = datetime.now(),
            Calibration =  Data["calibration"],
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
            "Photo_ID": New_Log.Log_ID
        }), 201
    else:
        return jsonify({"error": "Invalid file type"}), 400

@app.route('/uploads/<path:filename>')
def serve_uploaded_file(filename):
    return send_from_directory("./", filename)

if __name__ == "__main__":
    app.run(debug=True)
