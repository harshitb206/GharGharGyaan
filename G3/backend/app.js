const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');

const eligibilityRoutes = require('./routes/eligibility');
const rightsRoutes = require('./routes/rights');
const storiesRoutes = require('./routes/stories');
const documentRoutes = require('./routes/documents');

const app = express();
const twilioVoice = require('./routes/twilioVoice');
const twilioSms = require('./routes/twilioSms');
app.use(cors());
app.use(bodyParser.json());

app.use('/api/eligibility', eligibilityRoutes);
app.use('/api/rights', rightsRoutes);
app.use('/api/stories', storiesRoutes);
app.use('/api/documents', documentRoutes);

const PORT = 5001;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));