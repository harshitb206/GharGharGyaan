exports.getRightsByCategory = (req, res) => {
  const category = req.params.category;
  const rightsInfo = {
    maternity: "₹6000 under PMMVY, 26 weeks paid leave. Apply via Anganwadi.",
    domestic_violence: "Protection under DV Act. File complaint at police or protection officer.",
    immunization: "Free child vaccines at government centers.",
    pensions: "Widow/Disability pensions available from district office.",
    legal_aid: "Free legal help under NALSA. Visit Legal Services Authority office."
  };
  res.json({ info: rightsInfo[category] || "No information available." });
};