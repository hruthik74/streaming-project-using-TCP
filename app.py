from flask import Flask, render_template, redirect, url_for, request, session, Response
import sqlite3
import os
import socket

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuration
TCP_SERVER_HOST = '127.0.0.1'
TCP_SERVER_PORT = 5000
VIDEO_FOLDER = 'static/videos/'
THUMBNAIL_FOLDER = 'static/thumbnails/'

# Initialize database
def init_db():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Helper function to interact with TCP server
def request_file_from_tcp_server(filename):
    def stream():
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((TCP_SERVER_HOST, TCP_SERVER_PORT))

            # Send the filename
            client.sendall(filename.encode('utf-8'))

            # Check for server response
            response = client.recv(1024).decode('utf-8')
            if response.startswith("ERROR"):
                yield f"Error: {response}".encode('utf-8')
                return

            # Get file size and send ACK
            file_size = int(response)
            client.sendall(b"ACK")

            # Stream the file in chunks
            received_size = 0
            while received_size < file_size:
                chunk = client.recv(8192)
                if not chunk:
                    break
                received_size += len(chunk)
                yield chunk

        except Exception as e:
            yield f"Error during streaming: {str(e)}".encode('utf-8')
        finally:
            client.close()

    return stream, None


@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    videos = []
    for video_file in os.listdir(VIDEO_FOLDER):
        if video_file.endswith(('.mp4', '.mkv', '.avi')):
            video_name = os.path.splitext(video_file)[0]
            thumbnail_file = f"{video_name}.jpg"
            thumbnail_path = os.path.join(THUMBNAIL_FOLDER, thumbnail_file)
            if os.path.exists(thumbnail_path):
                videos.append((video_file, thumbnail_file))
            else:
                videos.append((video_file, 'default-thumbnail.jpg'))

    return render_template('index.html', videos=videos)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]
            return redirect(url_for('index'))
        else:
            return 'Invalid credentials', 400

    return render_template('login.html')

# New Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()
        try:
            c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return 'Username already exists', 400

        conn.close()
        return redirect(url_for('login'))

    return render_template('register.html')

# New Logout Route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/watch/<filename>')
def watch(filename):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    stream, error = request_file_from_tcp_server(filename)
    if error:
        return error, 500

    return Response(stream(), mimetype='video/mp4', headers={"Content-Disposition": f"inline; filename={filename}"})

@app.route('/download/<filename>')  
def download(filename):
    stream, error = request_file_from_tcp_server(filename)
    if error:
        return {"status": "error", "message": error}, 500

    return Response(stream(), mimetype='application/octet-stream', headers={"Content-Disposition": f"attachment; filename={filename}"})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, threaded=True)