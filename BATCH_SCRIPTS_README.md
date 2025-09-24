# AI Health Assistant - Batch Scripts

This directory contains batch scripts to easily start, stop, and set up the AI Health Assistant project on Windows.

## 📋 **Available Scripts**

### **🚀 start.bat**
**Basic startup script for the AI Health Assistant**

**What it does:**
- Checks for Python and Node.js installation
- Creates and activates Python virtual environment
- Installs Python dependencies
- Installs Node.js dependencies
- Starts both backend and frontend servers in separate windows

**Usage:**
```bash
start.bat
```

**Features:**
- Automatic dependency installation
- Virtual environment setup
- Dual server startup
- Error handling and validation

---

### **🚀 start_advanced.bat**
**Advanced startup script with enhanced features**

**What it does:**
- All features of start.bat
- Enhanced error checking and validation
- NLTK data verification and download
- File existence validation
- Colored output and progress indicators
- Detailed troubleshooting information

**Usage:**
```bash
start_advanced.bat
```

**Features:**
- Step-by-step progress display
- Comprehensive error checking
- NLTK data management
- File validation
- Enhanced user feedback
- Troubleshooting tips

---

### **🛑 stop.bat**
**Script to stop all running servers**

**What it does:**
- Stops all Python processes (backend server)
- Stops all Node.js processes (frontend server)
- Cleans up server windows
- Provides confirmation of shutdown

**Usage:**
```bash
stop.bat
```

**Features:**
- Graceful server shutdown
- Process cleanup
- Window cleanup
- Confirmation messages

---

### **⚙️ setup.bat**
**First-time setup script**

**What it does:**
- Checks system requirements (Python, Node.js)
- Creates Python virtual environment
- Installs all dependencies
- Downloads NLTK data
- Validates project structure
- Provides setup completion confirmation

**Usage:**
```bash
setup.bat
```

**Features:**
- Complete environment setup
- Dependency installation
- NLTK data download
- Project validation
- Setup guidance

---

## 🎯 **Quick Start Guide**

### **First Time Setup:**
1. **Run setup.bat** to install all dependencies
2. **Run start.bat** to start the servers
3. **Open http://localhost:8080** in your browser

### **Daily Usage:**
1. **Run start.bat** to start the servers
2. **Use the application** at http://localhost:8080
3. **Run stop.bat** when finished

### **Troubleshooting:**
1. **Run setup.bat** to reinstall dependencies
2. **Check the server windows** for error messages
3. **Verify ports 5000 and 8080** are available

---

## 🔧 **System Requirements**

### **Required Software:**
- **Python 3.8+** - Download from [python.org](https://www.python.org/downloads/)
- **Node.js** - Download from [nodejs.org](https://nodejs.org/)
- **Windows 10/11** - Batch scripts are Windows-specific

### **Required Ports:**
- **Port 5000** - Backend API server
- **Port 8080** - Frontend development server

### **Disk Space:**
- **~500MB** - For Python dependencies and models
- **~200MB** - For Node.js dependencies

---

## 📁 **Project Structure**

```
hariproject/
├── start.bat              # Basic startup script
├── start_advanced.bat     # Advanced startup script
├── stop.bat               # Stop servers script
├── setup.bat              # First-time setup script
├── BATCH_SCRIPTS_README.md # This documentation
├── ai/                    # Backend directory
│   ├── venv/              # Python virtual environment
│   ├── requirements.txt   # Python dependencies
│   ├── disease_prediction_api.py
│   └── ...
└── frontend/              # Frontend directory
    ├── node_modules/      # Node.js dependencies
    ├── package.json       # Node.js dependencies
    └── ...
```

---

## 🚨 **Troubleshooting**

### **Common Issues:**

#### **"Python is not installed"**
- Install Python 3.8+ from [python.org](https://www.python.org/downloads/)
- Make sure to check "Add Python to PATH" during installation

#### **"Node.js is not installed"**
- Install Node.js from [nodejs.org](https://nodejs.org/)
- Download the LTS (Long Term Support) version

#### **"Port already in use"**
- Close other applications using ports 5000 or 8080
- Run `stop.bat` to stop any existing servers
- Restart your computer if needed

#### **"Failed to install dependencies"**
- Check your internet connection
- Run `setup.bat` to reinstall dependencies
- Try running the installation commands manually

#### **"Virtual environment failed"**
- Delete the `ai/venv` folder and run `setup.bat` again
- Make sure Python is properly installed

#### **"NLTK data download failed"**
- Check your internet connection
- Run the NLTK download command manually:
  ```bash
  cd ai
  venv\Scripts\activate
  python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
  ```

---

## 📞 **Support**

### **Getting Help:**
1. **Check the server windows** for detailed error messages
2. **Run setup.bat** to reinstall dependencies
3. **Verify system requirements** are met
4. **Check project documentation** in `ai/docs/` directory

### **Manual Commands:**
If batch scripts fail, you can run commands manually:

**Backend:**
```bash
cd ai
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python disease_prediction_api.py
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

---

## 🎉 **Success Indicators**

### **Setup Complete:**
- ✅ Python virtual environment created
- ✅ Python dependencies installed
- ✅ Node.js dependencies installed
- ✅ NLTK data downloaded

### **Servers Running:**
- ✅ Backend server at http://localhost:5000
- ✅ Frontend server at http://localhost:8080
- ✅ Both servers in separate windows
- ✅ No error messages in server windows

### **Application Working:**
- ✅ Frontend loads in browser
- ✅ Chat interface appears
- ✅ Can send messages
- ✅ Backend responds to requests

---

*Last Updated: September 2025*
*Script Version: 1.0*
