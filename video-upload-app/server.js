const express = require('express');
const mongoose = require('mongoose');
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const Video = require('./models/video'); // 创建一个Video模型来表示视频元数据
const { spawn } = require('child_process');
const http = require('http');
const socketIo = require('socket.io');
const app = express();
const PORT = process.env.PORT || 3000;

const server = http.createServer(app);
const { Server } = require('socket.io');
const io = new Server(server);



function runPythonScript(filename, socket) {
  const pythonProcess = spawn('python', ['Trans_to_keypoints.py', filename]);

  pythonProcess.stdout.on('data', (data) => {
    const predictionData = data.toString(); // 将 stdout 数据转换为字符串
    console.log(`Python stdout: ${predictionData}`);

    // 实时更新数据到前端
    const htmlContent = `<div>${predictionData}</div>`; // 包裹在 div 中
    socket.emit('predictionData', htmlContent);
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
  res.sendFile(path.join(__dirname, 'index.html'));
});

io.on('connection', (socket) => {
  console.log('A user connected');

  socket.on('disconnect', () => {
    console.log('User disconnected');
  });
});


app.use(express.static(path.join(__dirname, '/public')));

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
    const { result } = 'curry'
    const { originalname, filename } = req.file;
    const video = new Video({
      originalname,
      filename,
      result,
    });

    await video.save();

    // 运行Python脚本，并将 socket 传递给函数
    runPythonScript(filename, io);

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

// 在你的 Express 应用程序中添加以下代码
app.get('/latest', async (req, res) => {
  try {
    const videos = await Video.find().sort({ createdAt: -1 }).limit(5); // 获取最新的 5 个视频
    res.render('test', { videos });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: '无法获取视频信息' });
  }
});

server.listen(PORT, () => console.log(`Server listening on port: ${PORT}`));

app.get('/', (req, res) => {
  // 在这里可以返回一个欢迎页面或其他内容
  res.send('欢迎访问视频上传应用');
});

