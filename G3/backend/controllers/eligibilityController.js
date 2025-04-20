const schemes = require('../data/schemes.json');

exports.checkEligibility = (req, res) => {
  const answers = req.body;
  const eligibleSchemes = schemes.filter(scheme =>
    scheme.criteria.every(criterion => answers[criterion] === true)
  );
  res.json({ eligibleSchemes });
};