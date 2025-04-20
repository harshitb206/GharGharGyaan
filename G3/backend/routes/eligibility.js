const express = require('express');
const router = express.Router();
const { checkEligibility } = require('../controllers/eligibilityController');

router.post('/', checkEligibility);

module.exports = router;