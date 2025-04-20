
exports.handleSms = (req, res) => {
  const incoming = req.body.Body.trim().toLowerCase();
  let reply = 'Sorry, I did not understand that. Try "maternity", "legal", or "help".';

  if (incoming.includes('maternity')) {
    reply = 'You may get ₹6000 under PMMVY. Visit your Anganwadi with Aadhaar & form.';
  } else if (incoming.includes('legal')) {
    reply = 'Free legal help is available under NALSA. Visit your District Legal Services Authority.';
  }

  const MessagingResponse = require('twilio').twiml.MessagingResponse;
  const twiml = new MessagingResponse();
  twiml.message(reply);

  res.type('text/xml');
  res.send(twiml.toString());
};
