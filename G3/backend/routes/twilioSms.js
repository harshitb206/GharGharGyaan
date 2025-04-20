
const express = require('express');
const router = express.Router();
const smsCtrl = require('../controllers/twilioSmsController');

router.post('/', smsCtrl.handleSms);

module.exports = router;
