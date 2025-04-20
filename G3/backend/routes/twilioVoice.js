
const express = require('express');
const router = express.Router();
const voiceCtrl = require('../controllers/twilioVoiceController');

router.post('/', voiceCtrl.handleCall);
router.post('/handle-input', voiceCtrl.handleInput);

module.exports = router;
