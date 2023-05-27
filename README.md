# Problem Statement

- Medical data is sensitive and contains personally identifiable information (PII) that needs to be protected.
- Researchers need access to medical data to gain valuable insights and learnings.
- How can we provide access to deidentified medical data to researchers while protecting patient privacy?

# Solution Idea

- Use generative AI techniques to remove PII identifiers from medical data and deidentify it.
- Use natural language processing (NLP) and text vector embeddings to perform anonymisation tasks.
- Use machine learning to train the model on large datasets of medical data and PII identifiers.
- Input data can be either textual reports data like pathology tests, EMR or pictographic test reports like X-Rays, MRI, etc.
- Build a secure platform where researchers can access the deidentified medical data for research purposes.

# Planned Features

- Text analysis: The model should be able to analyse the text data and identify the presence of any sensitive or PII data like names, addresses, phone numbers, and email addresses.
- Anonymisation techniques: The model should be able to anonymise the identified sensitive data using techniques like masking, obfuscation, and tokenisation.
- Contextual analysis: The model should be able to analyse the context of the text data and use the context to identify and deidentify the sensitive data accurately.
- Machine learning algorithms: The model should use machine learning algorithms and techniques like Natural Language Processing, Named Entity Recognition, and Sequence Labelling to identify and deidentify sensitive data.

# Technical Architecture

- Data ingestion layer: This layer should be responsible for ingesting the text data from various sources and preparing it for analysis.
- Data processing layer: This layer should be responsible for analysing the text data and identifying any sensitive or PII data.
- Data deidentification layer: This layer should be responsible for deidentifying the sensitive data using the anonymisation techniques mentioned above.
- Machine learning layer: This layer should be responsible for using machine learning algorithms to improve the accuracy and efficiency of the model.
- API layer: This layer should provide an API that can be used to integrate the model with other applications and workflows.
- Model training and management layer: This layer should be responsible for training and managing the model, including updating the model with new data and retraining as needed.

# What’s out of scope

- Data Ingestion layer pipelines will not be built as part of the basic prototype. Prototype will be API-driven.
- Model will not be trained on a very large set of data.
- Pictographic test reports as input will be supported later.
