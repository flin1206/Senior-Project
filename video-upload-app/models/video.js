const mongoose = require('mongoose');

const videoSchema = new mongoose.Schema({
  originalname: String,
  filename: String,
  result:String,
  createdAt: {
    type: Date,
    default: Date.now,
  },
});

module.exports = mongoose.model('Video', videoSchema);
