# HealthBook-AI: The Gut Hypercycle & Phenomic Health OS

**Status:** ☑️ Clinically Informed | ☑️ Ready for Multimodal AI Integration
**Target Audience:** Hoifung Poon (MSR), Alexander Ersoy (Azure Healthcare), Gates Foundation
**Core Maintainer:** Thread ② – HealthBook Agent
**Dependency:** `M3-Core-Engine` (for metabolic pathway definitions)

---

## 🩺 The Problem with Current AI
LLMs and Multimodal Foundation Models (BioGPT, PubMedBERT) excel at finding correlations in unstructured text and images. However, they treat the human body as a black box. They lack a **Causal Model of Metabolism**.

**HealthBook-AI provides the missing Mechanistic Layer.**

---

## 🧠 Why We Are Needed: The Metabolic Hypercycle in the Gut

Taking the ecological hypercycle proven in soil by **MBT55**, we model the gut as a 24-hour bioreactor.

| Ecological Layer | MBT55 Soil Hypercycle | **HealthBook Gut Hypercycle** |
| :--- | :--- | :--- |
| **Substrate** | Cellulose, Lignin | Dietary Fiber, Polyphenols |
| **Primary Currency** | Lactate | **Butyrate (Butyrate)** |
| **Specialized Signals** | Fulvic Acid | **Urolithin A (Mitophagy), Equol (Hormonal)** |
| **Stability Key** | H₂ Partial Pressure → 0 | **Redox Balance & Treg Induction** |

### The Core Metabolic Code (The 15 Pathways)
Unlike general "microbiome analysis," HealthBook maps patient data onto a **15-dimension metabolic pathway vector** covering Energy, Inflammation, Oxidative Stress, Hormonal Balance, and Detoxification.

This allows us to:
1.  **Predict Disease Risk** in a **137-Disease Matrix**.
2.  **Design Interventions** using MBT Probiotics (Lactate → Butyrate converters) or Herbal metabolites.

---

## ☁️ Integration with Azure Biomedical AI (Poon & Ersoy)

- **For Hoifung Poon (RWE/Causal Learning):** HealthBook provides the **Structural Causal Model (SCM)**. Instead of "correlation X causes Y," we provide the enzyme pathway `Polyphenol → Urolithin A → Mitophagy`.
- **For Alexander Ersoy (Multimodal):** We add the **5th Modality (Metabolome)** to Azure’s current Text/Image/Genomics model. We provide the real-time dynamic ODEs of the gut.

---

## 📦 Repository Structure

| Directory | Content |
| :--- | :--- |
| `src/` | Python models for 15-pathway vector and gut hypercycle simulation. |
| `models/` | MBT Probiotics library and Herbal Metabolism library definitions. |
| `dashboard/` | Streamlit app for patient journey simulation (Phenomics). |
| `questionnaire/` | The 200-item health screening matrix schema. |

> **Validation:** "We are not just diagnosing. We are mathematically proving the path from Soil (M3-Core-Engine) to Metabolism (HealthBook) to Finance (PBPE)."
