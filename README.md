# Fixed Vector Shorthand Model (FVSM) - Voynich Manuscript Research Framework

A production-grade computer vision, paleographic mapping, and automated validation pipeline designed to analyze 14th-century Latin shorthand scripts within historical manuscript folios.

## Key Architectural Components

* **Folio Matrix Preprocessor (`folio_matrix_processor.py`)**: Utilizes OpenCV bilateral filtering, adaptive Gaussian thresholding, and morphological closing to remove parchment noise while preserving fine tittle and macron stroke vectors. Includes spatial clustering for chronological left-to-right, row-by-row reading order sorting.
* **Token-to-Sigla Bridge (`token_to_sigla.py`)**: Maps isolated paleographic tokens to historical expansion matrices, evaluating baseline compliance scores and Monte Carlo isolation margins.
* **Automated Visual Dashboard (`update_dashboard.py`)**: Compiles real-time evaluation metrics into a responsive HTML compliance matrix dashboard (`fvsm_matrix_dashboard.html`).
* **Workspace Deployment Anchor (`deploy_engine.py`)**: Audits critical local assets, records stability states, and generates structural build manifests (`deployment_manifest.json`) prior to version tracking.
* **Master Orchestration Pipeline (`main_pipeline.py`)**: Unifies image preprocessing, token mapping, and live dashboard compilation into a single execution thread.

## 🛡️ Resilience & Fault-Tolerance (`VoynichIntegrityGuard`)

The FVSM pipeline includes a built-in defensive architecture designed to ensure zero unhandled runtime crashes during complex document processing:
* **File-System Ingestion Assertions**: Automatically validates that target folio scan assets exist and contain non-zero byte payloads before memory allocation.
* **Structural JSON Schema Validation**: Verifies that processed token dictionaries and Monte Carlo isolation margins strictly match matrix structural requirements.
* **Self-Healing Synthetic Fallback**: If a target scan (such as `sample_folio_f1r.png`) is missing from the active path, the execution harness dynamically generates a clean, synthetic 300 DPI parchment matrix via OpenCV to guarantee out-of-the-box pipeline validation.

## Repository Sync & Verification
All modules are structured for automated execution and remote synchronization on GitHub (`DarmaniHirani/Voynich_Project`).
