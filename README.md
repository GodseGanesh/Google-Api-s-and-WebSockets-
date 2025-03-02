# Google-Apis-and-WebSockets in Django-
# 🚀 Django Google Drive Integration API

This API allows users to **log in via Google**, **upload files**, **list files**, and **download files** from their Google Drive using **Django and Google OAuth**. 🔥  

---

## 🛠 Setup and Running the API  

### 1⃣ Clone the Repository  
```bash
git clone https://github.com/your-repo/google-drive-django.git
cd google-drive-django
```

### 2⃣ Create a Virtual Environment  
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

### 3⃣ Install Dependencies  
```bash
pip install -r requirements.txt
```

### 4⃣ Configure Environment Variables  
Create a `.env` file in the project root and add your **Google OAuth credentials**:  
```ini
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

### 5⃣ Apply Migrations  
```bash
python manage.py migrate
```

### 6⃣ Create a Superuser (Optional)  
```bash
python manage.py createsuperuser
```

### 7⃣ Run the Server  
```bash
python manage.py runserver
```
🚀 The API is now running at **http://127.0.0.1:8000/** 🎉  

---

## 🔑 **User Guide: How to Use the Application**  

### **Step 1⃣: Login with Google**  
- Open your browser and go to:  
  🔗 **[http://127.0.0.1:8000/login/](http://127.0.0.1:8000/login/)**  
- Click **Sign in with Google** and allow the required permissions.  

### **Step 2⃣: Connect Google Drive**  
- After login, the system automatically fetches your Google details.  
- Connect Google Drive using:  
  🔗 **[http://127.0.0.1:8000/connect-drive/](http://127.0.0.1:8000/connect-drive/)**  

### **Step 3⃣: Upload a File**  
- Open the upload page:  
  🔗 **[http://127.0.0.1:8000/upload/](http://127.0.0.1:8000/upload/)**  
- Select a file and click the **Upload** button.  

### **Step 4⃣: List Files in Google Drive**  
- Retrieve a list of files using:  
  🔗 **[http://127.0.0.1:8000/fetch-files/](http://127.0.0.1:8000/fetch-files/)**  

### **Step 5⃣: Download a File**  
- Use the file ID from Step 4 to download a file.  
- URL format:  
  🔗 **[http://127.0.0.1:8000/download-file/<file_id>/](http://127.0.0.1:8000/download-file/<file_id>/)**  

### **Step 6⃣: Logout**  
- Log out using:  
  🔗 **[http://127.0.0.1:8000/logout/](http://127.0.0.1:8000/logout/)**  

---

## 💼 **Testing the API Endpoints**  

You can test the API using **Postman** or **cURL**.  

### **1⃣ Login & Authentication**  
- **Login:**  
  ```http
  GET /login/
  ```
- **Get User Info:**  
  ```http
  GET /api/google/user/
  ```

### **2⃣ Google Drive Operations**  
- **Connect to Drive:**  
  ```http
  GET /connect-drive/
  ```
- **Upload a File:**  
  ```http
  POST /upload-file/
  Content-Type: multipart/form-data
  Body: file=<your_file>
  ```
- **List Files:**  
  ```http
  GET /fetch-files/
  ```
- **Download a File:**  
  ```http
  GET /download-file/<file_id>/
  ```
- **Logout:**  
  ```http
  POST /logout/
  ```

---

## 🎨 **Frontend Interface**  
- File Upload UI available at:  
  🔗 **[http://127.0.0.1:8000/upload/](http://127.0.0.1:8000/upload/)**  
- Dark-themed UI with orange accents for a better experience. 🔥  

---

## 📃 **Troubleshooting**  

### 🔹 Google OAuth Login Issues  
- Ensure your **Google OAuth Client ID & Secret** are correctly set in `.env`.  
- Make sure your **Google OAuth App** is verified and **Scopes** are set.  

### 🔹 API Authentication Errors  
- If you get `401 Unauthorized`, make sure you are logged in and authorized.  

### 🔹 File Upload Issues  
- Ensure the file is **not empty** and has **read permissions**.  
- Check that your **Google Drive storage is not full**.  

---

## 🔥 **Contributing**  
Feel free to **fork** this repo, submit **issues**, or send **pull requests**!  

---

## 🐝 **License**  
This project is **open-source** and free to use.  

---
Made with ❤️ by Ganesh Godse 🚀  
