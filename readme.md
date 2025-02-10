# Setup Python Environment and Run the Web Application

## Step 1: Create a Python Virtual Environment
To ensure a clean and isolated workspace, create a virtual environment.

```sh
python3 -m venv venv
```

Activate the virtual environment:

- **On macOS/Linux:**
  ```sh
  source venv/bin/activate
  ```
- **On Windows (CMD):**
  ```sh
  venv\Scripts\activate
  ```

---

## Step 2: Install Dependencies from `requirements.txt`
After activating the virtual environment, install required dependencies:

```sh
pip install -r requirements.txt
```

This will install all the necessary libraries required for the application.

---

## ▶️ Step 3: Run the Program
Once dependencies are installed, start the Python application:

```sh
python3 main.py
```

This will start the web server.

---

## 🌍 Step 4: Access the Web Application
After running the application, open your browser and go to:

```
http://localhost
```

Use the following credentials to log in:
- **Username:** `admin`
- **Password:** `admin`

---

## 🛠️ Step 5: Check SQLite Database (Optional)
To inspect the database, install the **SQLite extension** in VS Code:

### Install SQLite Extension:
1. Open **VS Code**.
2. Go to the **Extensions Marketplace** (`Ctrl+Shift+X` or `Cmd+Shift+X` on macOS).
3. Search for `SQLite` and install the **SQLite Viewer** extension.

### Open and Explore SQLite Database:
1. Open VS Code.
2. Locate the `usersDB.db` file in the project directory.
3. Right-click on the file and select **"Open Database"** using the SQLite extension.
4. Run SQL queries to view data.
