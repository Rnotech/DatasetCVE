# CVE Dataset (1999-2024) for LLM Fine-Tuning

---

## Overview

This dataset comprises **Common Vulnerabilities and Exposures (CVE)** records spanning from **1999 to 2024**. Each entry provides essential information on software vulnerabilities, their descriptions, affected products and versions, CVSS scores, and relevant references. The data is formatted in a **JSON Lines (.jsonl)** structure, making it suitable for fine-tuning **Large Language Models (LLMs)** for tasks such as cybersecurity analysis, vulnerability detection, and automated threat intelligence.

The dataset is prepared for use in scenarios where an LLM needs to comprehend, describe, and respond to questions about cybersecurity vulnerabilities. It leverages data from official CVE repositories, transforming it into a structured question-answer format.

---

## Dataset Structure

Each line in the `.jsonl` file corresponds to a JSON object with the following fields:

- **`instruction`**: The task or command for the model.
- **`input`**: The specific question or query.
- **`output`**: The response or information the model is expected to generate.

### Example Entry

```json
{
    "instruction": "Describe CVE-2021-1234.",
    "input": "What is CVE-2021-1234?",
    "output": "An out-of-bounds write vulnerability exists in XYZ software version 1.2.3, allowing remote attackers to execute arbitrary code."
}
```

---

## Fields Breakdown

### `instruction`

The `instruction` field specifies the task or context for the model. It can include requests such as:

- **Describing the vulnerability**:  
  `"instruction": "Describe CVE-2020-5678."`

- **Identifying affected products**:  
  `"instruction": "Identify the affected product in CVE-2019-9876."`

- **Stating CVSS scores**:  
  `"instruction": "State the CVSS score for CVE-2022-3456."`

- **Providing references**:  
  `"instruction": "Provide references for CVE-2023-7890."`

- **Stating publication dates**:  
  `"instruction": "State the publication date of CVE-2018-6543."`

### `input`

The `input` field contains a specific question or query related to the instruction. Examples include:

- **For descriptions**:  
  `"input": "What is CVE-2020-5678?"`

- **For affected products**:  
  `"input": "Which product is affected by CVE-2019-9876?"`

- **For CVSS scores**:  
  `"input": "What is the CVSS score of CVE-2022-3456?"`

- **For references**:  
  `"input": "Where can I find more information about CVE-2023-7890?"`

- **For publication dates**:  
  `"input": "When was CVE-2018-6543 published?"`

### `output`

The `output` field provides the detailed answer to the input query. Examples include:

- **Description**:  
  `"output": "A buffer overflow vulnerability exists in ABC software version 2.0, which allows remote code execution."`

- **Affected product and version**:  
  `"output": "The affected product is DEF software, version 1.5.2 and 1.6.0."`

- **CVSS score and severity**:  
  `"output": "The CVSS score and severity for CVE-2022-3456 is 7.8 (High)."`

- **References**:  
  `"output": "References are available at: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-7890."`

- **Publication date**:  
  `"output": "CVE-2018-6543 was published on 2018-03-15."`

---

## Preparation for Fine-Tuning

This dataset is preprocessed and ready for fine-tuning any LLM architecture that supports instruction-based learning, such as:

- **Llama 2/3**  
- **GPT models**  
- **Mistral**  
- **Falcon**  

The `.jsonl` format allows for straightforward integration into popular fine-tuning framework like: **Hugging Face's Transformers**
  
---

## Dataset Size and Scope

- **Years Covered**: 1999 to 2024
- **Dataset Size**: Approximately 288 MB
- **Sources**: Data derived from official CVE repositories: https://github.com/CVEProject/cvelistV5  

---

## Conclusion

This dataset provides a rich, structured source of CVE data tailored for training AI models in cybersecurity tasks. By leveraging detailed instructions, inputs, and outputs, you can enhance your model’s ability to understand and analyze vulnerability data, contributing to more effective cyber threat detection and response.

---
