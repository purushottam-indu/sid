import React from 'react';
import styles from './query.module.css';

const Query= () => {
  return (
    <div className={styles.boxesContainerquerySuggestion}>
      <div className={styles.boxquerySuggestion}>
        “Explain [medical condition] in simple language for a newly diagnosed patient. Give me 3 examples.”
      </div>
      <div className={styles.boxquerySuggestion}>
        “How to upload a document and query it?”
      </div>
      <div className={styles.boxquerySuggestion}>
        “Explore the applications of genetic testing in pharmacogenomics, focusing on how genetic information can inform medication selection and dosing (within 120 words), while addressing the ethical implications of genetic data privacy.”
      </div>
      <div className={styles.boxquerySuggestion}>
        “Explore the possibility of predicting individual health outcomes based on various factors (genetics, lifestyle, medical history). Develop a predictive model that tailors recommendations for personalized healthcare interventions.”
      </div>
      <div className={styles.boxquerySuggestion}>
        “Outline a case conference format for discussing complex cases of [medical condition] with professionals from different disciplines. Compose 3 outlines, each no more than 250 words.”
      </div>
      <div className={styles.boxquerySuggestion}>
        “Create an outline for a community-based awareness program focusing on [medical condition]. Provide 3 examples, each within 200 words.”
      </div>
    </div>
  );
}

export default Query;
