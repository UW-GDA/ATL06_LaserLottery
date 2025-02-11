# **ATL06: Laser Lottery**  

## **Project Team**  
- Jack Hayes ([@Jack-Hayes](https://github.com/jack-hayes))  
- Collaborators (this could be you!)  

## **Project Overview**  
**ATL06: Laser Lottery** is a comparative analysis of ICESat-2's ATL06 land ice elevation algorithm and custom photon-counting approaches. Using a variety of elevation datasets, we aim to assess the impact of different processing strategies on elevation retrievals over diverse terrain and vegetation. Our goal is to determine why certain processing algorithms perform better in specific conditions and how they can contribute to NASA's **Surface Topography and Vegetation (STV) Incubation program**.

## **Background**  
Launched on **September 15, 2018**, **[ICESat-2](https://icesat-2.gsfc.nasa.gov/)** is a NASA satellite that measures global elevation using the **Advanced Topographic Laser Altimeter System (ATLAS)**. ATLAS fires **10,000 laser pulses per second**, each containing **~300 trillion photons**, but only a handful return to the sensor. These photons are then processed by algorithms such as **ATL06**, which estimates land ice surface height by filtering noise and computing along- and across-track slopes.

ICESat-2 supports multiple applications through various data products, with a few listed below:  
- **ATL03:** Raw photon cloud data  
- **ATL06:** Land ice elevation (our focus)  
- **ATL08:** Canopy height and surface classification  
- **ATL13:** Inland water surface heights  

For more details, see the **[ICESat-2 Data Products](https://icesat-2.gsfc.nasa.gov/science/data-products)**.

## **Problem Statement & Objectives**  
While ATL06 is widely used for land ice elevation, alternative processing techniques may provide improved accuracy in complex terrain and vegetation. We aim to:  
- Compare **ATL06's standard processing** to **custom photon-counting algorithms**.  
- Assess performance over **varying vegetation and terrain** types.
- Understand **why** some algorithms perform better than others.  
- Investigate implications for **multi-modal elevation fusion** for NASA's **STV Incubation program**.

## **Datasets**  
We will analyze ICESat-2 elevation data alongside:  
- **[USGS 3DEP Aerial LiDAR](https://www.usgs.gov/3d-elevation-program)** – High-resolution airborne LiDAR.  
- **[Maxar VHR In-Track Stereo DSMs](https://stereopipeline.readthedocs.io/en/latest/introduction.html)** – Derived from satellite stereo imagery using NASA's [Ames Stereo Pipeline](https://stereopipeline.readthedocs.io/en/latest/introduction.html).  
- **[Copernicus 30m DEM (COP-DEM)](https://spacedata.copernicus.eu/web/cscda/dataset-details?articleId=394198)** – Global medium-resolution DEM.  

## **Tools & Software**  
We will leverage multiple tools to process and analyze the data:  
- **[SlideRule](https://slideruleearth.io/)** – NASA’s cloud-based ICESat-2 processing framework, supporting both standard and **custom algorithms**.  
- **[Coincident](https://coincident.readthedocs.io/en/latest/)** – Includes a wrapper for SlideRule allowing for ease of spatiotemporal filtering over differing geometries and land cover and terrain  
- **[GeoPandas](https://geopandas.org/)** – Spatial data analysis.  
- **[Xarray](https://docs.xarray.dev/en/stable/)** – Handling multi-dimensional elevation datasets.  

## **Methodology**  
1. **Preprocess Differing ELevation Measurement Sources** – Retrieve elevation profiles over the study area for the different datasets.  
2. **Apply Custom Photon-Counting Algorithms** – Implement alternative processing methods in SlideRule via gridsearch.  
3. **Compare with Reference Datasets** – Validate against aerial LiDAR, stereo DSMs, and radar DEMs.  
4. **Analyze Performance Metrics** – Evaluate accuracy based on terrain, land cover, and algorithmic differences.  
5. **Integrate Findings into NASA’s STV Framework** – Assess how these techniques fit into broader Earth observation objectives.

## **Expected Outcomes**  
- Identification of conditions where **custom photon-counting algorithms** outperform ATL06.  
- Insights into **terrain- and vegetation-dependent biases** in ICESat-2 elevation retrievals.  
- Contributions to NASA’s **STV Incubation program** for **multi-modal elevation fusion**.  

## **Related Work**  
- **[ICESAT-2 HackWeek: Surfit](https://github.com/ICESAT-2HackWeek/surfit)** – Prior work on surface fitting algorithms for ICESat-2.  
- **[ICESat-2 Data Portal](https://icesat-2.gsfc.nasa.gov/)** – Official mission website.  
- **[ICESat-2 Land Ice Elevation Paper](https://www.sciencedirect.com/science/article/pii/S0034425719303712)** – Foundational ICESat-2 paper.  

## **References**  
- **National Academies of Sciences, Engineering, and Medicine (2018).** *Thriving on Our Changing Planet: A Decadal Strategy for Earth Observation from Space.* [DOI: 10.17226/24938](https://doi.org/10.17226/24938).  
- **Donnellan, A. (2021).** *Observing Earth's Surface Topography and Vegetation Structure in the Next Decade.* [AGU U32A-01](https://agu.confex.com/agu/fm21/meetingapp.cgi/Paper/940395).  
- **Farr, T. (2007).** *Shuttle Radar Topography Mission (SRTM) Data Processing and Applications.*  

---  
### *"Because counting photons is more complicated than it sounds."*  🚀❄️
