exports.generateDocument = (req, res) => {
  const { name, scheme } = req.body;
  const doc = `To whom it may concern,

This is to certify that ${name} is applying for the ${scheme} scheme under the applicable laws and requests assistance as per entitlement.

Sincerely,
GharGharGyaan Team`;

  res.json({ document: doc });
};