const stories = require('../data/stories.json');

exports.getStories = (req, res) => {
  res.json(stories);
};