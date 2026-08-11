---
title: Machine Learning vs Deep Learning
type: concept
domain: [ai-ml]
status: stable
tags: [ai, ml, deep-learning, fundamentals]
sources: [raw-sources/archive/ML-vs-DL.md]
created: 2026-08-11
updated: 2026-08-11
---

# Machine Learning vs Deep Learning

## Summary
ML and DL are both subsets of AI: AI → ML → DL. ML learns patterns from data using classical algorithms; DL is the subset of ML that uses multi-layer neural networks and handles unstructured data (images, audio, text) directly.

## Details

### Machine Learning
- Requires structured data
- Needs manual feature engineering
- Works well with smaller datasets
- Examples: spam detection, fraud detection, recommendation systems

### Deep Learning
- Works with unstructured data (images, text, audio)
- Extracts features automatically
- Requires large datasets and heavy compute
- Examples: LLMs (ChatGPT-class models), image recognition, voice assistants

### Key differences

| Feature | Machine Learning | Deep Learning |
|---|---|---|
| Data requirement | Low to medium | High |
| Feature engineering | Manual | Automatic |
| Complexity | Lower | High |
| Training time | Faster | Slower |
| Accuracy | Moderate | High |
| Hardware | CPU | GPU/TPU |

### When to use which
- **Use ML** when data is small/structured, the problem is simple, and you need faster results.
- **Use DL** when data is large/unstructured, patterns are complex, and you need high accuracy.

### DevOps mapping
- **ML**: log anomaly detection, alert classification
- **DL**: NLP for log understanding, AI copilots, root-cause analysis

## Open questions
- Specific algorithms (XGBoost, Random Forest) and DL architectures (CNN, RNN, Transformers) were flagged as future expansion but never detailed.

## Related
- [[artificial-intelligence]]
- [[aiops]]
