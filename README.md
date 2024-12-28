# streaming-project-using-TCP
# Video Streaming System

## **Overview**
This project implements a lightweight video streaming system designed for efficient file transfer, seamless video playback, and scalability within a local area network (LAN). The system utilizes a Flask-based backend, a multi-threaded TCP server, and a user-friendly frontend interface to provide an optimized streaming experience.

---

## **Features**

### Flask Backend:
- Handles user authentication, video listing, and playback requests.
- Routes:
  - `/watch/<filename>`: Streams videos in real-time for immediate playback.
  - `/download/<filename>`: Enables video downloads in chunks for optimized performance.

### TCP Server:
- Transfers video files in manageable chunks (8192 bytes) to minimize memory usage.
- Supports multiple simultaneous client connections using a thread pool architecture.

### Chunk-Based Streaming:
- Ensures smooth playback without requiring the entire video file to be downloaded.
- Efficiently handles large files and concurrent users.

### User Interface:
- Intuitive frontend with features like:
  - Browsing available videos.
  - An embedded video player with playback controls (fast forward, rewind, etc.).
  - Download options for videos.

### Database Integration:
- SQLite database for secure user authentication and personalized content.
- Stores user credentials and manages access control.

---

## **Project Architecture**
1. **Flask Backend**: Serves as the web application’s core, interfacing with the TCP server and managing client requests.
2. **TCP Server**: Handles video file transfers efficiently in chunks, ensuring minimal resource consumption.
3. **Frontend**: Provides an easy-to-use interface for video browsing, playback, and downloads.
4. **Database**: Maintains user data securely and ensures proper access control.

---

## **Setup Instructions**

### Prerequisites:
- Python 3.8+
- Flask
- SQLite

### Steps:
1. Clone this repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Initialize the SQLite database:
   ```bash
   python init_db.py
   ```

4. Start the TCP server:
   ```bash
   python tcp_server.py
   ```

5. Start the Flask application:
   ```bash
   flask run
   ```

6. Access the application in your browser at:
   ```
   http://localhost:5000
   ```

---

## **How to Use**

### User Authentication:
- Register a new account or log in using existing credentials.

### Browsing Videos:
- Navigate through the list of available videos on the homepage.

### Watching Videos:
- Click on a video to stream it in real-time using the embedded player.
- Use the player controls to fast forward, rewind, or pause.

### Downloading Videos:
- Select the download option to save the video to your local device.

---

## **Folder Structure**
```
.
├── static/
│   ├── css/          # Stylesheets
│   ├── js/           # JavaScript files
│   └── videos/       # Video storage
├── templates/        # HTML templates
├── app.py            # Main Flask application
├── tcp_server.py     # TCP server for video transfer
├── init_db.py        # Database initialization script
├── requirements.txt  # Python dependencies
└── README.md         # Project documentation
```

---

## **Future Enhancements**
- Implement user-specific video recommendations.
- Add support for subtitles and multiple video formats.
- Extend the system for cloud-based deployment.

---

## **Contributors**
This project was developed by a team of 4 members. (Add names here.)

---

## **License**
This project is licensed under the MIT License. See the LICENSE file for details.

