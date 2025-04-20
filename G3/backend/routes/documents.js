const express = require('express');
const router = express.Router();
const { generateDocument } = require('../controllers/documentController');

router.post('/', generateDocument);

module.exports = router;