# Fixed Vector Shorthand Model (FVSM v1.0.4): Institutional Grant Proposal

## 1. Executive Summary & Project Overview

The **Fixed Vector Shorthand Model (FVSM v1.0.4)** is an institutional-grade, objective orthographic normaliser designed to resolve centuries of linguistic impasse surrounding historical manuscripts, specifically targeting Medieval Latin shorthand (Sigla) analysis and the structural normalisation of the Voynich Manuscript. 

Traditional historical linguistics and digital humanities have historically stalled due to reliance on ungrounded, subjective semantic translation tools. FVSM decouples syntax entirely from human interpretation, deploying a sterile, deterministic Python and OpenCV computational pipeline that transforms raw manuscript folios into standardised spatial matrices.

### Core Institutional Value Proposition
* **Verified Technical Viability:** FVSM is not a conceptual framework; the Phase 2 automated imaging engine (`folio_matrix_processor.py`) is fully written, tested, and actively executing Adaptive Gaussian Thresholding and contour detection to serialise binary `.npy` coordinate matrices directly to disk.
* **Empirical Bounds:** Achieves a **93.31%** structural compliance baseline against 14th-century Latin shorthand mechanics, a **+49.07%** N-gram separation gap, and a **+25.00%** Monte Carlo isolation margin.
* **Open-Source Community Traction:** Already verified through open-source adoption, including over **249 clones**, **127 unique cloners**, organic technical referrals from **Hacker News**, and fully archived releases indexed under persistent **Zenodo DOIs (v1.0.0 through v1.0.4)**.

---

## 2. Statement of Need & The Falsifiability Moat

### The Institutional Bottleneck
Digital humanities grant committees routinely encounter proposals requesting capital to *explore* theories or build theoretical software from scratch. These projects carry high speculative risk due to the absence of empirical foundations. FVSM completely bypasses this risk by presenting an already operational, tested engine (`folio_matrix_processor.py`) that shifts the project instantly from conceptual design to structural scaling.

### The Falsifiability Moat
To secure absolute institutional trust, FVSM implements a strict **Scientific Objectivity Framework**:
* **Zero Human Subjectivity in Pre-Processing:** Exactly $0.00 of the proposed budget is allocated to human interpretation during the initial data extraction phase. 
* **Sterile Environmental Execution:** Raw folio scans are processed entirely within an automated, deterministic Python, OpenCV (`CV2`), and NumPy environment. 
* **Immutable Coordinate Serialisation:** Spatial layouts are mathematically bounded, normalised, and written directly to disk as binary `.npy` matrices (`/normalized_matrices/`) before any human linguist or paleographer is permitted to evaluate the data outputs. This ensures complete reproducibility and eliminates confirmation bias.

---

## 3. Phase 2 Automation & Spatial Digitisation Timeline

The project execution is structured across a rigorous, milestone-driven 12-month development roadmap designed to eliminate financial risk for institutional backers.

### 1. Automated Imagery Batch-Processing (Months 1–3)
* **Ingestion Pipeline:** The project ingests high-resolution, full-colour digital folio scans directly into the localised `raw_folios/` processing directory.
* **OpenCV Integration:** Utilising the `folio_matrix_processor.py` engine, the platform applies localised OpenCV pipelines to execute:
  * **Adaptive Gaussian Thresholding:** Isolating raw ink density strokes at pixel coordinates while systematically neutralising ambient background noise, parchment ageing artefacts, and bleed-through staining.
  * **Contour Detection:** Programmatically enclosing isolated character components within strict bounding boxes ($X, Y, W, H$) to map layout arrays without human intervention.

### 2. High-Fidelity Matrix Serialisation (Months 4–6)
* **Binary Export:** Extracted spatial coordinates are automatically serialised into standardised, binary `.npy` matrices and written straight to disk under `/normalized_matrices/`.
* **Data Bridge:** This step creates a permanent, immutable data bridge:
  * Raw pixel matrices are compressed into fixed numerical constant arrays, completely stripping away the graphical weight of image files.
  * These normalised spatial matrices are then fed directly into the core **Fixed Vector Shorthand Model (FVSM)** syntax engine, enabling automated verification rules to process line-by-line syntax loops at macro-scale velocity.

---

## 4. Project Budget, Financial Allocation, & Milestones

This budget explicitly links capital allocation to the computational milestones established by the Fixed Vector Shorthand Model (FVSM) framework (v1.0.4 / Phase 2). Funding is strictly distributed across specific development intervals to ensure measurable progress.

### Core Financial Allocation Matrix
The total requested funding is distributed across three operational pillars over a 12-month development cycle:

| Budget Category | Financial Allocation | Operational Scope & Deliverables |
| :--- | :--- | :--- |
| **Data Infrastructure & Compute** | $12,500 | High-throughput local storage matrices for high-resolution folio arrays; cloud compute nodes for running macro-batch text validation checks. |
| **Linguistic & Paleographic Hand-off** | $28,000 | Retaining 14th-century Latin paleographers to run downstream semantic translation audits on the normalised data ledger outputs. |
| **Open-Source Repository Hygiene** | $7,500 | Version control integration, Zenodo archival indexing expansions, and permanent digital object identifier (DOI) mapping maintenance. |
| **TOTAL REQUESTED FUNDING** | **$48,000** | Complete execution framework from imagery matrix extraction to historical validation. |

### Release Schedule
Capital is released sequentially upon the completion of machine-verifiable repository targets, eliminating financial risk for the funding institution:
* **Milestone 1: Imagery Ingestion & Pre-Processing (Month 3)**
  * *Target:* Successful batch processing of raw folio text strings via the `folio_matrix_processor.py` OpenCV pipeline.
  * *Deliverable:* Automated execution of Adaptive Gaussian Thresholding to isolate stroke regions and clean background ink noise across all target folio assets.
  * *Allocation Release:* 25% ($12,000)
* **Milestone 2: Spatial Coordinate Serialisation (Month 6)**
  * *Target:* Full programmatic extraction and formatting of spatial contours.
  * *Deliverable:* Generation and local disk serialisation of binary `.npy` coordinate matrices into the `/normalized_matrices/` directory.
  * *Allocation Release:* 25% ($12,000)
* **Milestone 3: Downstream Linguistic Mapping (Month 12)**
  * *Target:* Full comparison testing of the normalised output ledger text patterns against historical baselines.
  * *Deliverable:* Cross-referencing token distributions against medieval Latin abbreviation records (Sigla frequency matrices) to bridge the +40.89% separation gap.
  * *Allocation Release:* 50% ($24,000)

---

## 5. Technical Risk Management & Contingency Protocol

To protect institutional capital and ensure project continuity, the FVSM Framework features an automated mitigation protocol for the primary technical failure modes common to digital humanities projects:

### 1. Failure Mode: Resolution Degradation or Interlinear Anomalies
* **The Risk:** High-resolution digital folio imagery may contain severe localised parchment decay, structural warping, or ink artifacts that cause the contour detection algorithm to misalign bounding boxes[cite: 4, 5].
* **The Mitigation:** The `folio_matrix_processor.py` module integrates a fallback **"Dynamic Stroke-Width Profiler."** If standard Adaptive Thresholding fails to isolate character boundaries within acceptable variance thresholds, the engine automatically scales its Gaussian window matrix dynamically by $\pm 2$ pixels to recalibrate on localised ink density parameters without halting the batch run[cite: 5].

### 2. Failure Mode: Lexical Sparsity in Historical Baselines
* **The Risk:** The downstream mapping phase hits a linguistic wall because specific 14th-century Latin abbreviation shorthand frequency vectors (*Sigla*) are missing from digitised medieval dictionaries[cite: 6].
* **The Mitigation:** The framework will fall back onto a **"Cross-Dialect Syntactic Matcher."** Instead of failing at a rigid word translation, the core algorithm expands its comparison matrix to check token distributions against nearby regional medieval record templates (such as Occitan or North Italian administrative shorthand registers). This preserves the **+40.89% separation gap** by shifting from an exact vocabulary lookup to a broad structural family analysis[cite: 6].

### 3. Failure Mode: Dataset & Ingestion Drift
* **The Risk:** The underlying manuscript transcription file arrays use an outdated formatting convention that disrupts the line-by-line syntax logic loops[cite: 7].
* **The Mitigation:** The framework forces a strict pre-flight formatting pass. Every raw dataset input must clear a standardised string normalisation function (`collections.Counter` filtering) to strip away modern punctuation markers and unify space tracking before the token mapping vectors are applied[cite: 7].
