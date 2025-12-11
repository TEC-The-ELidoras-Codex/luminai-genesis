const express = require('express');
const router = express.Router();

module.exports = (db) => {
  // static example harm reduction resources - in real deployment, these are dynamic/curated
  const resources = [
    { id: 1, title: 'Fentanyl Test Strip Locator', href: 'https://harmreduction.org', type: 'harm_reduction' },
    { id: 2, title: 'Find naloxone (Narcan)', href: 'https://www.narcan.com', type: 'overdose' },
    { id: 3, title: 'Local Harm Reduction Coalition', href: 'https://harmreduction.org', type: 'org' }
  ];

  router.get('/resources', (req, res) => {
    res.json({ resources });
  });

  return router;
};
