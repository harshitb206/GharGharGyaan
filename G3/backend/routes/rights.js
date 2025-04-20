const express = require('express');
const router = express.Router();
const { getRightsByCategory } = require('../controllers/rightsController');

router.get('/:category', getRightsByCategory);

module.exports = router;