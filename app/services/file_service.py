import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app
from PIL import Image


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def generate_unique_filename(filename):
    """Generate unique filename to prevent collisions"""
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    return unique_name


def save_uploaded_file(file, subfolder=''):
    """Save a single uploaded file"""
    if file and file.filename and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = generate_unique_filename(filename)
        
        # Create subfolder if it doesn't exist
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
        os.makedirs(upload_path, exist_ok=True)
        
        file_path = os.path.join(upload_path, unique_filename)
        file.save(file_path)
        
        # Create thumbnail for images
        if subfolder == 'images':
            try:
                create_thumbnail(file_path, subfolder)
            except Exception as e:
                print(f"Error creating thumbnail: {e}")
        
        # Return relative path for storage in database
        return os.path.join(subfolder, unique_filename).replace('\\', '/')
    
    return None


def save_uploaded_files(files, subfolder=''):
    """Save multiple uploaded files"""
    saved_files = []
    
    for file in files:
        if file and file.filename:
            filepath = save_uploaded_file(file, subfolder)
            if filepath:
                saved_files.append(filepath)
    
    return saved_files


def create_thumbnail(image_path, subfolder=''):
    """Create thumbnail for image"""
    try:
        img = Image.open(image_path)
        img.thumbnail((300, 300), Image.Resampling.LANCZOS)
        
        # Save thumbnail
        filename = os.path.basename(image_path)
        thumb_name = f"thumb_{filename}"
        thumb_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder, 'thumbnails')
        os.makedirs(thumb_folder, exist_ok=True)
        
        thumb_path = os.path.join(thumb_folder, thumb_name)
        img.save(thumb_path)
        
        return os.path.join(subfolder, 'thumbnails', thumb_name).replace('\\', '/')
    except Exception as e:
        print(f"Error creating thumbnail: {e}")
        return None


def delete_file(filepath):
    """Delete a file from upload folder"""
    if filepath:
        try:
            full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filepath)
            if os.path.exists(full_path):
                os.remove(full_path)
                
                # Also delete thumbnail if it exists
                if 'images' in filepath:
                    thumb_path = filepath.replace('images/', 'images/thumbnails/thumb_')
                    thumb_full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], thumb_path)
                    if os.path.exists(thumb_full_path):
                        os.remove(thumb_full_path)
                
                return True
        except Exception as e:
            print(f"Error deleting file {filepath}: {e}")
    
    return False


def delete_files(file_list):
    """Delete multiple files"""
    for filepath in file_list:
        delete_file(filepath)
