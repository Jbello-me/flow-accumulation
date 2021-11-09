'''
Author: Jubril Bello 
Modified and adapted from Dr. John B. Lindsay (https://www.whiteboxgeo.com/manual/wbt_book/preface.html)
This python script interfaces with WhiteboxTools to create flow accumulation rasters using:
    D8 algorithm
    D-infinity algorithm
    Qin et al. (2007) flow algorithm 
'''
from WBT.whitebox_tools import WhiteboxTools

wbt = WhiteboxTools()  # Setup Whitebox

# Set the working directory, which contains the lab data.
# Modify the string (in red) below to suit your data location.
wbt.set_working_dir = (r"C:\put\your\directory\here")

# First breach the depressions in the DEM.
wbt.breach_depressions_least_cost(
    dem="DEM.tif",
     output="DEM_breached.tif", 
     dist=1000, 
     fill=False)

# There are likely still depression in the DEM and so we'll also fill.
wbt.fill_depressions_wang_and_liu(
    dem="DEM_breached.tif", 
    output="DEM_filled.tif", 
    fix_flats=True)

# Perform a D8 flow accumulation operation.
wbt.d8_flow_accumulation(
    i="DEM_filled.tif", 
    output="d8.tif", 
    out_type="sca", 
    log=True)

# Perform a D-infinity flow accumulation operation.
wbt.d_inf_flow_accumulation(
    i="DEM_filled.tif", 
    output="dinf.tif", 
    out_type="sca", 
    threshold=10000, 
    log=True)

# Perfom a Qin flow accumulation operation.
wbt.qin_flow_accumulation(
    dem="DEM_filled.tif",
    output="Qin.tif",
    out_type="specific contributing area",
    exponent=10.0,
    max_slope=45.0,
    threshold=10000,
    log=True,
    clip=False,
)

# For-loop to test lower and higher threshold values
for t in range(0, 10001, 1000):  # The for-loop checks theshold values in the range: 0-10,000
    print(f"threshold:{t}")      # An interval value of 1,000 is used to step through the range
    wbt.d_inf_flow_accumulation(
        i="DEM_filled.tif",
        output=f"dinf_threshold{t}.tif",
        out_type="sa",
        threshold=t,
        log=True
    )

#Create a hillshade to overlay when we visualize the flow accumulation rasters.
wbt.multidirectional_hillshade(
    dem="DEM_filled.tif", 
    output="multi_hillshade", 
    altitude=45.0, zfactor=None, 
    full_mode=True
)
