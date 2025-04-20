
const twilio = require('twilio');
const VoiceResponse = twilio.twiml.VoiceResponse;

exports.handleCall = (req, res) => {
  const twiml = new VoiceResponse();
  const gather = twiml.gather({
    numDigits: 1,
    action: '/api/voice/handle-input',
    method: 'POST'
  });
  gather.say('Welcome to Ghar Ghar Gyaan. Press 1 for maternity benefits. Press 2 for legal aid.');
  res.type('text/xml');
  res.send(twiml.toString());
};

exports.handleInput = (req, res) => {
  const twiml = new VoiceResponse();
  const digit = req.body.Digits;
  if (digit === '1') {
    twiml.say('You are eligible for 26 weeks paid leave and six thousand rupees under PMMVY.');
  } else if (digit === '2') {
    twiml.say('Free legal aid is available through NALSA. Visit your local legal services authority.');
  } else {
    twiml.say('Invalid input. Goodbye.');
  }
  res.type('text/xml');
  res.send(twiml.toString());
};
