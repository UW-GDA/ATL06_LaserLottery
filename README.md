# **ATL06: Laser Lottery**  

## **Project Team**  
- Jack Hayes ([@Jack-Hayes](https://github.com/jack-hayes))  
- Collaborators (this could be you!)  

## **Project Overview**  
**ATL06: Laser Lottery** is a comparative analysis of ICESat-2's ATL06 land ice elevation algorithm and custom photon-counting approaches. Using a variety of elevation datasets, we aim to assess the impact of different processing strategies on elevation retrievals over diverse terrain and vegetation. Our goal is to determine why certain processing algorithms perform better in specific conditions and how they can contribute to NASA's **Surface Topography and Vegetation (STV) Incubation program**.

## **Background**  
Launched on **September 15, 2018**, **[ICESat-2](https://icesat-2.gsfc.nasa.gov/)** is a NASA satellite that measures global elevation using the **Advanced Topographic Laser Altimeter System (ATLAS)**. ATLAS fires **10,000 laser pulses per second**, each containing **~300 trillion photons**, but only a handful return to the sensor. These photons are then processed by algorithms such as **ATL06**, which estimates land ice surface height by filtering noise and computing along- and across-track slopes.

![ICESat-2 Beams (Smith et al., 2019)](icesat2_beams.jpg)  
*Figure: ICESat-2 beam configuration (Smith et al., 2019).*

ICESat-2 supports multiple applications through various data products, with a few listed below:  
- **ATL03:** Raw photon cloud data  
- **ATL06:** Land ice elevation (our focus)  
- **ATL08:** Canopy height and surface classification  
- **ATL13:** Inland water surface heights  

For more details, see the **[ICESat-2 Data Products](https://icesat-2.gsfc.nasa.gov/science/data-products)**.

## **Problem Statement & Objectives**  
Accurate and high-resolution topographic data are crucial for understanding Earth’s **dynamic surface processes**, including **glacier retreat, vegetation structure, and elevation changes**. The **National Academy of Sciences’ 2017–2027 Decadal Survey for Earth Observation** identified these datasets as priority observables for NASA Earth Science ([National Academies, 2018](https://doi.org/10.17226/24938)). In response, NASA’s **Surface Topography and Vegetation (STV) Incubation Program** aims to develop **next-generation multi-modal elevation datasets** by integrating **satellite and airborne data**.

Unlike past efforts such as **SRTM (Shuttle Radar Topography Mission)**, which provided a near-global topographic dataset over 11 days in 2001, STV seeks to **fuse elevation measurements from lidar, optical stereo, and synthetic aperture radar (SAR)** collected at different times. This integration introduces several challenges:
- **Variability in measurement techniques** (e.g., photon-counting lidar vs. radar)
- **Differences in spatial resolution and sensor geometry**
- **Real surface changes over time** (e.g., vegetation growth, ice melt)

ATL06 is a standard processing algorithm for ICESat-2, but its **performance and biases** in non-glacial environments remain **poorly understood**. Comparing ATL06-derived elevations with alternative photon classification methods is essential to:
- **Identify systematic biases** in ICESat-2’s elevation products
- **Understand why ATL06-derived elevations disagree with other altimetry sources** (e.g., airborne LiDAR, stereo photogrammetry, radar DEMs)
- **Improve the accuracy of fused elevation datasets for STV**

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
### *Because counting photons is more complicated than it sounds*  🚀❄️
