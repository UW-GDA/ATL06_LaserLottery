# **ATL06: Laser Lottery** ![what da dog doin](https://github.com/tlberglund/animated-gifs/blob/3cd940af8cd795393388f117f4e8c091cde72d0c/corgi-diving.gif)

## **Project Team**  
- Jack Hayes ([@Jack-Hayes](https://github.com/jack-hayes))  
- Collaborators (this could be you!)  

## **Project Overview**  
**ATL06: Laser Lottery** is a comparative analysis of ICESat-2's ATL06 land ice elevation algorithm and custom photon-counting approaches. Using a variety of elevation datasets, we aim to assess the impact of different processing strategies on elevation retrievals over diverse terrain and vegetation. Our goal is to determine why certain processing algorithms perform better in specific conditions and how they can contribute to NASA's **Surface Topography and Vegetation (STV) Incubation program** efforts.

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

Given the limited scope of our final project, we're mainly concerned with the question **what biases are introduced by different ATL06 processing parameters, how do these biases change over varying terrain and land cover characteristics, and why?**

ATL06 is a standard processing algorithm for ICESat-2, but its **performance and biases** in non-glacial environments remain **poorly understood**. Comparing customized ATL06 photon processing methods, using the "standard" ATL06 processing as reference, is essential to:
- **Identify systematic biases** in ICESat-2’s elevation products
- **Understand why ATL06-derived elevations disagree with other altimetry sources** 
- **Improve the accuracy of fused elevation datasets for STV**

In the context of our project, we will hone in on understanding why ATL06-derived elevations disagree with "ground truth" altimetry derived from aerial LiDAR DSMs. Additionally, we will focus on a small subset of the [CO West Central 2019](https://portal.opentopography.org/usgsDataset?dsid=CO_WestCentral_2019) 3DEP mission dlown over western Colorado in August and September of 2019 which was selected as a site for STV's [Precursor Coincident Dataset](https://science.nasa.gov/earth-science/decadal-surveys/decadal-stv/coincident-datasets/) efforts. The site was selected due to the fortuitous collection of coincident, near-contemporaneous elevation datasets (VHR in-track stereo, GEDI, ICESat-2, aerial LIDAR) over the area and we utilize this site because the aerial LiDAR DSM has already been processed with custom parameters, and we want to avoid using vendor-generated products. We will just be focusing on the ICESat-2 and aerial LiDAR observations, though. The site exhibits high elevation (2500-4300m) and relief with various types of vegetation, containing bare ground for control points as well.

## **Datasets**  
We will analyze ICESat-2 elevation data alongside:  
- **[USGS 3DEP Aerial LiDAR DSMs](https://www.usgs.gov/3d-elevation-program)** – High-resolution airborne LiDAR DSMs derived via custom [PDAL](https://pdal.io/en/2.8.4/) processing pipelines. Treated as "ground truth" elevation.
- **[ESA WorldCover LULC](https://esa-worldcover.org/en)** – THIS IS TO-BE UPDATED WITH CUSTOM "ECOZONES" AS SEEN FROM [Malambo et al. 2021](https://www.sciencedirect.com/science/article/pii/S0034425721004314) AND MORE DISTINCT LULC IN GENERAL

## **Tools & Software**  
We will leverage multiple tools to process and analyze the data:  
- **[SlideRule](https://slideruleearth.io/)** – NASA’s cloud-based ICESat-2 processing framework, supporting both standard and **custom algorithms**.   
- **[GeoPandas](https://geopandas.org/)** – Spatial data analysis for our ICESat-2 points and other relevant vector geometries.  
- **[Xarray](https://docs.xarray.dev/en/stable/)** – Handling multi-dimensional elevation datasets and other relevant rasters and nDarrays.  

## **Methodology**  
1. **Preprocess Differing Elevation Measurement Sources** – Retrieve elevation profiles over the study area for the different datasets.  
2. **Apply Custom Photon-Counting Algorithms** – Implement alternative processing methods in SlideRule via gridsearch.  
3. **Compare with Reference Datasets** – Validate against aerial LiDAR based on terrain, land cover, and algorithmic differences.
4. **Tie Findings into NASA’s STV Framework** – Assess how these techniques fit into broader Earth observation objectives.

## **Expected Outcomes**  
- Identification of conditions where **custom photon-counting algorithms** outperform standard ATL06 processing.  
- Insights into **terrain- and vegetation-dependent biases** in ICESat-2 elevation retrievals.  
- Contributions to NASA’s **STV Incubation program** for **multi-modal elevation fusion**.  

## **Related Work**  
- **[ICESAT-2 HackWeek: Surfit](https://github.com/ICESAT-2HackWeek/surfit)** – Prior work on surface fitting algorithms for ICESat-2.  
- **[ICESat-2 Data Portal](https://icesat-2.gsfc.nasa.gov/)** – Official mission website.  
- **[ICESat-2 Land Ice Elevation Paper](https://www.sciencedirect.com/science/article/pii/S0034425719303712)** – Foundational ICESat-2 paper.
- **[ICESat-2 Canopy Height Evaluation Paper](https://www.sciencedirect.com/science/article/pii/S0034425721004314)** – Similar work comparing ATL08 algorithms for canopy height.

## **References**  
- **National Academies of Sciences, Engineering, and Medicine (2018).** *Thriving on Our Changing Planet: A Decadal Strategy for Earth Observation from Space.* [DOI: 10.17226/24938](https://doi.org/10.17226/24938).  
- **Donnellan, A. (2021).** *Observing Earth's Surface Topography and Vegetation Structure in the Next Decade.* [AGU U32A-01](https://agu.confex.com/agu/fm21/meetingapp.cgi/Paper/940395).  
- **Farr, T. (2007).** *Shuttle Radar Topography Mission (SRTM) Data Processing and Applications.*  

---  
### *Because counting photons is more complicated than it sounds*  🚀❄️
