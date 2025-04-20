const express = require('express');
const router = express.Router();
const { getStories } = require('../controllers/storiesController');

router.get('/', getStories);

module.exports = router;