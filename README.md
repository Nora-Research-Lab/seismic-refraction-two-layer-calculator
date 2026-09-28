![NORA logo](https://i.ibb.co/0VJCC9Gf/IMG-20260114-WA0008.jpg)
 
# Seismic Refraction Two-Layer Calculator
 
*For geophysicists and exploration geologists: enter first-arrival times and distances from a refraction survey to instantly compute P-wave velocities and depth to the refractor using the intercept-time method.*
 
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
 

## Overview
 
**Industry:** Geophysics
 
The tool implements the intercept-time method for a two-layer horizontal seismic refraction model.

Inputs:
- Distance array (m): a comma-separated list of source-to-receiver distances (positive, increasing).
- First arrival time array (ms): comma-separated list of corresponding first-arrival travel times (≥0).
- Both must be same length, at least 6 points.

Core calculation steps:
1. Sort (distance, time) pairs by distance.
2. Initial split: first round(0.25 × N) points as direct arrivals, remainder as refracted.
3. Perform linear regression (distance vs time) on each subset to get slopes and intercepts.
4. Compute crossover distance Xc = (b2 - b1) / (m1 - m2) where m1=1/V1, b1=intercept for direct; m2=1/V2, b2=intercept for refracted.
5. Reassign: points with distance ≤ Xc are direct, > Xc are refracted; recompute regressions.
6. Compute V1 = 1 / (slope of direct regression), V2 = 1 / (slope of refracted regression).
7. Compute intercept time ti = intercept of refracted regression line (ms).
8. Compute depth to interface: h = (ti * V1 * V2) / (2 * sqrt(V2² - V1²)).
9. Output both velocities in km/s, depth in meters, crossover distance in meters.
10. Show a travel-time plot with data points and both best-fit lines (direct dashed, refracted solid).
11. Provide a classification: if V1 < 1.5 km/s -> 'Unconsolidated soil'; 1.5–2.5 km/s -> 'Weathered rock'; else 'Competent rock'.
12. Output a downloadable CSV with distance, time, fitted direct time, fitted refracted time.

UI (Gradio):
- Left column: two textboxes for distance and time arrays; 'Compute' button.
- Right column: matplotlib plot (travel-time graph) and a text box showing V1, V2, depth, crossover distance, classification.
- Below: 'Download CSV' button.

No AI/ML component; pure deterministic calculation with iterative regression.
 
## Run it
 
```bash
docker build -t seismic-refraction-two-layer-calculator .
docker run -p 7860:7860 seismic-refraction-two-layer-calculator
```
 
Then open http://localhost:7860 in your browser.
 
## About
 
This tool was generated and published automatically by the **NORA Earth Intelligence**
tool factory, an autonomous pipeline maintained by **NORA Research Lab** that turns
one idea per run into a small, working geoscience tool — end to end, with an
LLM writing and Docker-testing the code, and another model generating the
banner above.
 
- Platform: [https://noraearth.xyz](https://noraearth.xyz)
- Parent lab: [https://noraresearchlab.site](https://noraresearchlab.site)
 
Built 2026-09-28.
 
---
 
### Maintainer
 
**NORA Research Lab**
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
