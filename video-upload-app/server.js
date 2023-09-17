const express = require('express');
const mongoose = require('mongoose');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const Video = require('./models/video'); // 创建一个Video模型来表示视频元数据

const app = express();
const PORT = process.env.PORT || 3000;
const { spawn } = require('child_process');

function runPythonScript(filename, res) {
  const pythonProcess = spawn('python', ['Trans_to_keypoints.py', filename]);

  pythonProcess.stdout.on('data', (data) => {
    const predictionData = data.toString(); // 将 stdout 数据转换为字符串
    console.log(`Python stdout: ${predictionData}`);

  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Python stderr: ${data}`);
  });

  pythonProcess.on('close', (code) => {
    console.log(`Python process exited with code ${code}`);
  });
}


mongoose.connect('mongodb://127.0.0.1:27017/video_upload_app', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

const db = mongoose.connection;
db.on('error', console.error.bind(console, 'MongoDB 连接错误：'));
db.once('open', () => {
  console.log('已连接到 MongoDB 数据库');
});

// Serve the test.html file at the root ("/") path
app.get('/', (req, res) => {
  // Read and send the test.html file
  res.sendFile(path.join(__dirname, 'test.html'));
});

app.use(express.static(path.join(__dirname, 'public')));

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/');
  },
  filename: (req, file, cb) => {
    const ext = path.extname(file.originalname);
    cb(null, `${Date.now()}${ext}`);
  },
});

const upload = multer({ storage });

app.post('/upload', upload.single('video'), async (req, res) => {
  try {
    const { originalname, filename } = req.file;
    const video = new Video({
      originalname,
      filename,
    });

    await video.save();

    // 运行Python脚本
    runPythonScript(filename, res);

    res.status(200).json({ message: '视频上传成功' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: '视频上传失败' });
  }
});

// 新增用于提供视频文件的路由
app.get('/videos/:filename', (req, res) => {
  const { filename } = req.params;
  res.sendFile(path.join(__dirname, 'uploads', filename));
});

app.listen(PORT, () => {
  console.log(`服务器运行在端口 ${PORT}`);
});

app.get('/', (req, res) => {
  // 在这里可以返回一个欢迎页面或其他内容
  res.send('欢迎访问视频上传应用');
});

