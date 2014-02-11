
""" 
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.
    
""" 

import os

import numpy as np
import matplotlib.pyplot as plt

from clawpack.visclaw import colormaps, geoplot
import clawpack.clawutil.clawdata as clawdata

import clawpack.geoclaw.surge as surge
import clawpack.geoclaw.multilayer as multilayer

def meters_to_km(x,y):
    return x/1e3,y/1e3
    
#--------------------------
def setplot(plotdata):
#--------------------------
    
    """ 
    Specify what is to be plotted at each frame.
    Input:  plotdata, an instance of pyclaw.plotters.data.ClawPlotData.
    Output: a modified version of plotdata.
    
    """ 

    # Load data from output
    amrdata = clawdata.AmrclawInputData(2)
    amrdata.read(os.path.join(plotdata.outdir,'amrclaw.data'))
    physics = clawdata.GeoclawInputData(2)
    physics.read(os.path.join(plotdata.outdir,'geoclaw.data'))
    surge_data = surge.data.SurgeData()
    surge_data.read(os.path.join(plotdata.outdir,'surge.data'))
    friction_data = surge.data.FrictionData()
    friction_data.read(os.path.join(plotdata.outdir,'friction.data'))
    multilayer_data = multilayer.data.MultilayerData()
    multilayer_data.read(os.path.join(plotdata.outdir,'multilayer.data'))
    
    # Slicing helper functions
    def transform_c2p(x,y,x0,y0,theta):
        return ((x+x0)*np.cos(theta) - (y+y0)*np.sin(theta),
                (x+x0)*np.sin(theta) + (y+y0)*np.cos(theta))

    def transform_p2c(x,y,x0,y0,theta):
        return ( x*np.cos(theta) + y*np.sin(theta) - x0,
                -x*np.sin(theta) + y*np.cos(theta) - y0)
        
    # if multilayer_data.bathy_type == 1:
    #     x = [0.0,0.0]
    #     y = [0.0,1.0]
    #     x1,y1 = transform_c2p(x[0],y[0],multilayer_data.bathy_location,
    #                                 0.0,multilayer_data.bathy_angle)
    #     x2,y2 = transform_c2p(x[1],y[1],multilayer_data.bathy_location,
    #                                 0.0,multilayer_data.bathy_angle)
        
    #     m = (y1 - y2) / (x1 - x2)
    #     x[0] = (amrdata.ylower - y1) / m + x1
    #     y[0] = amrdata.ylower
    #     x[1] = (amrdata.yupper - y1) / m + x1
    #     y[1] = amrdata.yupper
    #     ref_lines = [((x[0],y[0]),(x[1],y[1]))]
    # else:
    #     ref_lines = []
    # print ref_lines
    

    # plotdata.clearfigures()
    # plotdata.clear_frames = False
    # plotdata.clear_figs = True
    
    # plotdata.save_frames = False
    

    # ========================================================================
    # Axis limits
    #xlimits = [amrdata.xlower,amrdata.xupper]
    xlimits = [-0.5,0.5]
    xlimits_zoomed = xlimits
    #ylimits = [amrdata.ylower,amrdata.yupper]
    ylimits = [-0.5,0.5]
    eta = [multilayer_data.eta_init[0],multilayer_data.eta_init[1]]
    top_surface_limits = [eta[0]-0.03,eta[0]+0.03]
    internal_surface_limits = [eta[1]-0.015,eta[1]+0.015]
    top_speed_limits = [0.0,0.1]
    internal_speed_limits = [0.0,0.03]
    
    top_surf_zoomed = [eta[0] - 0.03,eta[0]+0.03]
    bottom_surf_zoomed = [-0.7,-0.5]
    # bottom_surf_zoomed = [eta[1] - 0.5,eta[1] + 0.5]
    velocities_zoomed = [-0.005,0.005]
    
    # Single layer test limits
    # top_surface_limits = [eta[0]-2.5,eta[0]+2.5]
    # top_speed_limits = [0.0,6.0]
    
    # ========================================================================
    #  Surface Elevations
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='Surface', figno=0)
    plotfigure.show = True
    plotfigure.kwargs = {'figsize':(14,4)}
    
    # Top surface
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Top Surface'
    plotaxes.axescmd = 'subplot(1,2,1)'
    plotaxes.scaled = True
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits
    # plotaxes.afteraxes = pcolor_afteraxes
    multilayer.plot.add_surface_elevation(plotaxes,1,bounds=top_surface_limits)
    # add_surface_elevation(plotaxes,1,bounds=[-0.06,0.06])
    # add_surface_elevation(plotaxes,1)
    multilayer.plot.add_land(plotaxes)
    
    # Bottom surface
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Internal Surface'
    plotaxes.axescmd = 'subplot(1,2,2)'
    plotaxes.scaled = True
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits
    # plotaxes.afteraxes = pcolor_afteraxes
    # add_surface_elevation(plotaxes,2,bounds=[-300-0.5,-300+0.5])
    multilayer.plot.add_surface_elevation(plotaxes,2,bounds=internal_surface_limits)
    # add_surface_elevation(plotaxes,2)
    multilayer.plot.add_land(plotaxes)
    
    # ========================================================================
    #  Depths
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='Depths', figno=42)
    plotfigure.show = True
    plotfigure.kwargs = {'figsize':(14,4)}
    
    # Top surface
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Top Layer Depth'
    plotaxes.axescmd = 'subplot(1,2,1)'
    plotaxes.scaled = True
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits
    # plotaxes.afteraxes = pcolor_afteraxes
    multilayer.plot.add_layer_depth(plotaxes,1)
    multilayer.plot.add_land(plotaxes)
    
    # Bottom surface
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Bottom Layer Depth'
    plotaxes.axescmd = 'subplot(1,2,2)'
    plotaxes.scaled = True
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits
    # plotaxes.afteraxes = pcolor_afteraxes
    multilayer.plot.add_layer_depth(plotaxes,2)
    multilayer.plot.add_land(plotaxes)
    
    # ========================================================================
    #  Water Speed
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='speed', figno=1)
    plotfigure.show = True
    plotfigure.kwargs = {'figsize':(14,4)}

    # Top layer speed
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Currents - Top Layer'
    plotaxes.scaled = True
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits
    plotaxes.axescmd = 'subplot(1,2,1)'
    # plotaxes.afteraxes = pcolor_afteraxes
    # add_speed(plotaxes,1,bounds=[0.00,0.2])
    multilayer.plot.add_speed(plotaxes,1,bounds=top_speed_limits)
    # add_speed(plotaxes,1)
    multilayer.plot.add_land(plotaxes)
    
    # Bottom layer speed
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = 'Currents - Bottom Layer'
    plotaxes.scaled = True
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits
    plotaxes.axescmd = 'subplot(1,2,2)'
    # plotaxes.afteraxes = pcolor_afteraxes
    # add_speed(plotaxes,2,bounds=[0.0,1e-10])
    multilayer.plot.add_speed(plotaxes,2,bounds=internal_speed_limits)
    # add_speed(plotaxes,2)
    multilayer.plot.add_land(plotaxes)
    
    # Individual components
    plotfigure = plotdata.new_plotfigure(name='speed_components',figno=401)
    plotfigure.show = False
    plotfigure.kwargs = {'figsize':(14,14)}
    
    # Top layer
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = "X-Velocity - Top Layer"
    plotaxes.scaled = True
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits
    plotaxes.axescmd = 'subplot(2,2,1)'
    # plotaxes.afteraxes = pcolor_afteraxes
    # add_x_velocity(plotaxes,1,bounds=[-1e-10,1e-10])
    multilayer.plot.add_x_velocity(plotaxes,1)
    multilayer.plot.add_land(plotaxes)
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = "Y-Velocity - Top Layer"
    plotaxes.scaled = True
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits
    plotaxes.axescmd = 'subplot(2,2,2)'
    # plotaxes.afteraxes = pcolor_afteraxes
    # add_y_velocity(plotaxes,1,bounds=[-0.000125,0.000125])
    multilayer.plot.add_y_velocity(plotaxes,1)
    multilayer.plot.add_land(plotaxes)
    
    # Bottom layer
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = "X-Velocity - Bottom Layer"
    plotaxes.scaled = True
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits
    plotaxes.axescmd = 'subplot(2,2,3)'
    # plotaxes.afteraxes = pcolor_afteraxes
    # add_x_velocity(plotaxes,2,bounds=[-1e-10,1e-10])
    multilayer.plot.add_x_velocity(plotaxes,2)
    multilayer.plot.add_land(plotaxes)
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.title = "Y-Velocity - Bottom Layer"
    plotaxes.scaled = True
    plotaxes.xlimits = xlimits
    plotaxes.ylimits = ylimits
    plotaxes.axescmd = 'subplot(2,2,4)'
    # plotaxes.afteraxes = pcolor_afteraxes
    # add_y_velocity(plotaxes,2,bounds=[-0.8e-6,.8e-6])
    multilayer.plot.add_y_velocity(plotaxes,2)
    multilayer.plot.add_land(plotaxes)

    # ========================================================================
    #  Profile Plots
    # ========================================================================
    # plotfigure = plotdata.new_plotfigure(name='profile', figno=4)
    # plotfigure.show = False
    
    # # Top surface
    # plotaxes = plotfigure.new_plotaxes()
    # plotaxes.xlimits = xlimits
    # plotaxes.ylimits = [-2000,20]
    # plotaxes.title = "Profile of depth"
    # plotaxes.afteraxes = profile_afteraxes
    
    # slice_index = 30
    
    # # Internal surface

    
    # # Bathy
    # plotitem = plotaxes.new_plotitem(plot_type='1d_from_2d_data')
    # plotitem.map_2d_to_1d = bathy_profile
    # plotitem.plot_var = 0
    # plotitem.amr_plotstyle = ['-','+','x']
    # plotitem.color = 'k'
    # plotitem.show = True
    
    # # Internal Interface
    # plotitem = plotaxes.new_plotitem(plot_type='1d_from_2d_data')
    # plotitem.map_2d_to_1d = lower_surface
    # plotitem.plot_var = 7
    # plotitem.amr_plotstyle = ['-','+','x']
    # plotitem.color = 'b'
    # plotitem.show = True
    
    # # Upper Interface
    # plotitem = plotaxes.new_plotitem(plot_type='1d_from_2d_data')
    # plotitem.map_2d_to_1d = upper_surface
    # plotitem.plot_var = 6
    # plotitem.amr_plotstyle = ['-','+','x']
    # plotitem.color = (0.2,0.8,1.0)
    # plotitem.show = True
    
    # ========================================================================
    #  Combined Profile Plot
    # ========================================================================
    # add_combined_profile_plot(plotdata,0.25,direction='y',figno=120)
    # add_combined_profile_plot(plotdata,0.8,direction='y',figno=121)
    # 
    # add_velocities_profile_plot(plotdata,0.25,direction='y',figno=130)
    # add_velocities_profile_plot(plotdata,0.8,direction='y',figno=131)
    
        
    # ========================================================================
    #  Bathy Profile
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='bathy_profile',figno=20)
    plotfigure.show = False
    
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = xlimits
    plotaxes.title = "Bathymetry Profile"
    plotaxes.scaled = 'equal'
    
    plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    plotitem.plot_var = multilayer.plot.bathy_profile
    plotitem.imshow_cmin = -4000
    plotitem.imshow_cmax = 10
    plotitem.add_colorbar = True
    # plotitem.amr_imshow_show = [1,1,1]
    plotitem.amr_celledges_show = [0,0,0]
    plotitem.amr_patchedges_show = [1,1,1]
    plotitem.show = True
    
    
    # ========================================================================
    # Figure for grids alone
    # ========================================================================
    plotfigure = plotdata.new_plotfigure(name='grids', figno=11)
    plotfigure.show = False
    
    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = xlimits
    plotaxes.xlimits = ylimits
    plotaxes.title = 'grids'
    # plotaxes.afteraxes = pcolor_afteraxes
    plotaxes.scaled = True
    
    # Set up for item on these axes:
    plotitem = plotaxes.new_plotitem(plot_type='2d_grid')
    # plotitem.amr_grid_bgcolor = ['#ffeeee', '#eeeeff', '#eeffee']
    plotitem.amr_patch_bgcolor = ['blue','red','green','cyan','yellow']
    plotitem.amr_celledges_show = [1,1,0,0,0,0]   
    plotitem.amr_patchedges_show = 1
    
    # ========================================================================
    # Figures for momentum
    # ========================================================================
    # plotfigure = plotdata.new_plotfigure(name='x-momentum', figno=13)
    # plotfigure.show = False

    # # Set up for axes in this figure:
    # plotaxes = plotfigure.new_plotaxes()
    # plotaxes.title = 'X-Velocity'
    # plotaxes.scaled = True
    # plotaxes.xlimits = xlimits
    # plotaxes.ylimits = ylimits
    # plotaxes.afteraxes = pcolor_afteraxes
    
    # # Water
    # # plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    # # # plotitem.plot_var = geoplot.surface
    # # plotitem.plot_var = water_u
    # # plotitem.pcolor_cmap = colormaps.make_colormap({1.0:'r',0.5:'w',0.0:'b'})
    # # # plotitem.pcolor_cmin = -1.e-10
    # # # plotitem.pcolor_cmax = 1.e-10
    # # # plotitem.pcolor_cmin = -2.5 # -3.0
    # # # plotitem.pcolor_cmax = 2.5 # 3.0
    # # plotitem.add_colorbar = True
    # # plotitem.amr_gridlines_show = [0,0,0]
    # # plotitem.amr_gridedges_show = [1,1,1]

    # # Land
    # plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    # plotitem.show = True
    # plotitem.plot_var = geoplot.land
    # plotitem.pcolor_cmap = geoplot.land_colors
    # plotitem.pcolor_cmin = 0.0
    # plotitem.pcolor_cmax = 80.0
    # plotitem.add_colorbar = False
    # plotitem.amr_gridlines_show = [0,0,0]
    # plotitem.amr_gridedges_show = [1,1,1]
    
    # plotfigure = plotdata.new_plotfigure(name='y-momentum', figno=14)
    # plotfigure.show = False

    # # Set up for axes in this figure:
    # plotaxes = plotfigure.new_plotaxes()
    # plotaxes.title = 'Y-Velocity'
    # plotaxes.scaled = True
    # plotaxes.xlimits = xlimits
    # plotaxes.ylimits = ylimits
    # plotaxes.afteraxes = pcolor_afteraxes
    
    # # Water
    # # plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    # # # plotitem.plot_var = geoplot.surface
    # # plotitem.plot_var = water_v
    # # plotitem.pcolor_cmap = colormaps.make_colormap({1.0:'r',0.5:'w',0.0:'b'})
    # # # plotitem.pcolor_cmin = -1.e-10
    # # # plotitem.pcolor_cmax = 1.e-10
    # # # plotitem.pcolor_cmin = -2.5 # -3.0
    # # # plotitem.pcolor_cmax = 2.5 # 3.0
    # # plotitem.add_colorbar = True
    # # plotitem.amr_gridlines_show = [0,0,0]
    # # plotitem.amr_gridedges_show = [1,1,1]

    # # Land
    # add_land(plotaxes)
    
    # ========================================================================
    #  Contour plot for surface
    # ========================================================================
    # plotfigure = plotdata.new_plotfigure(name='contour_surface',figno=15)
    # plotfigure.show = False
    # plotfigure.kwargs = {'figsize':(14,4)}
    
    # # Set up for axes in this figure:
    
    # # Top Surface
    # plotaxes = plotfigure.new_plotaxes()
    # plotaxes.title = 'Top Surface'
    # plotaxes.axescmd = 'subplot(1,2,1)'
    # plotaxes.scaled = True
    # plotaxes.xlimits = xlimits
    # plotaxes.ylimits = ylimits
    # plotaxes.afteraxes = contour_afteraxes
    # add_surface_elevation(plotaxes,plot_type='contour',surface=1,bounds=[-2.5,-1.5,-0.5,0.5,1.5,2.5])
    # add_land(plotaxes,plot_type='contour')
    
    # # Internal Surface
    # plotaxes = plotfigure.new_plotaxes()
    # plotaxes.title = 'Internal Surface'
    # plotaxes.axescmd = 'subplot(1,2,2)'
    # plotaxes.scaled = True
    # plotaxes.xlimits = xlimits
    # plotaxes.ylimits = ylimits
    # plotaxes.afteraxes = contour_afteraxes
    # add_surface_elevation(plotaxes,plot_type='contour',surface=2,bounds=[-2.5,-1.5,-0.5,0.5,1.5,2.5])
    # add_land(plotaxes,plot_type='contour')
    
    # # ========================================================================
    # #  Contour plot for speed
    # # ========================================================================
    # plotfigure = plotdata.new_plotfigure(name='contour_speed',figno=16)
    # plotfigure.show = False
    # plotfigure.kwargs = {'figsize':(14,4)}
    
    # # Set up for axes in this figure:
    # plotaxes = plotfigure.new_plotaxes()
    # plotaxes.title = 'Current'
    # plotaxes.scaled = True
    # plotaxes.xlimits = xlimits
    # plotaxes.ylimits = ylimits
    # plotaxes.afteraxes = contour_afteraxes
    
    # # Surface
    # plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    # plotitem.plot_var = water_speed_depth_ave
    # plotitem.kwargs = {'linewidths':1}
    # # plotitem.contour_levels = [1.0,2.0,3.0,4.0,5.0,6.0]
    # plotitem.contour_levels = [0.5,1.5,3,4.5,6.0]
    # plotitem.amr_contour_show = [1,1,1]
    # plotitem.amr_gridlines_show = [0,0,0]
    # plotitem.amr_gridedges_show = [1,1,1]
    # plotitem.amr_contour_colors = 'k'
    # # plotitem.amr_contour_colors = ['r','k','b']  # color on each level
    # # plotitem.amr_grid_bgcolor = ['#ffeeee', '#eeeeff', '#eeffee']
    # plotitem.show = True 
    
    # # Land
    # plotitem = plotaxes.new_plotitem(plot_type='2d_contour')
    # plotitem.plot_var = geoplot.land
    # plotitem.contour_nlevels = 40
    # plotitem.contour_min = 0.0
    # plotitem.contour_max = 100.0
    # plotitem.amr_contour_colors = ['g']  # color on each level
    # plotitem.amr_grid_bgcolor = ['#ffeeee', '#eeeeff', '#eeffee']
    # plotitem.gridlines_show = 0
    # plotitem.gridedges_show = 0
    # plotitem.show = True
    
    # ========================================================================
    #  Vorticity Plot
    # ========================================================================
    # plotfigure = plotdata.new_plotfigure(name='vorticity',figno=17)
    # plotfigure.show = False
    # plotaxes = plotfigure.new_plotaxes()
    # plotaxes.title = "Vorticity"
    # plotaxes.scaled = True
    # plotaxes.xlimits = xlimits
    # plotaxes.ylimits = ylimits
    # plotaxes.afteraxes = pcolor_afteraxes
    # 
    # # Vorticity
    # plotitem = plotaxes.new_plotitem(plot_type='2d_imshow')
    # plotitem.plot_var = 9
    # plotitem.imshow_cmap = plt.get_cmap('PRGn')
    # # plotitem.pcolor_cmap = plt.get_cmap('PuBu')
    # # plotitem.pcolor_cmin = 0.0
    # # plotitem.pcolor_cmax = 6.0
    # plotitem.imshow_cmin = -1.e-2
    # plotitem.imshow_cmax = 1.e-2
    # plotitem.add_colorbar = True
    # plotitem.amr_gridlines_show = [0,0,0]
    # plotitem.amr_gridedges_show = [1]
    # 
    # # Land
    # plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    # plotitem.plot_var = geoplot.land
    # plotitem.pcolor_cmap = geoplot.land_colors
    # plotitem.pcolor_cmin = 0.0
    # plotitem.pcolor_cmax = 80.0
    # plotitem.add_colorbar = False
    # plotitem.amr_gridlines_show = [0,0,0]
    
    # ========================================================================
    #  Figures for gauges
    # ========================================================================
    # plotfigure = plotdata.new_plotfigure(name='Surface & topo', figno=300, \
    #                 type='each_gauge')
    # plotfigure.show = True
    # plotfigure.clf_each_gauge = True

    # # Set up for axes in this figure:
    # plotaxes = plotfigure.new_plotaxes()
    # plotaxes.xlimits = [0.0,40.0*3600.0]
    # plotaxes.ylimits = top_surface_limits
    # plotaxes.title = 'Top Surface'

    # # Plot surface as blue curve:
    # plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    # plotitem.plot_var = 6
    # plotitem.plotstyle = 'b-'

    # Plot topo as green curve:
    # plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    # plotitem.plot_var = geoplot.gaugetopo
    # plotitem.plotstyle = 'g+'
    
    #-----------------------------------------
    
    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via pyclaw.plotters.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    plotdata.print_framenos = 'all'          # list of frames to print
    plotdata.print_fignos = 'all'            # list of figures to print
    plotdata.html = True                    # create html files of plots?
    plotdata.latex = False                   # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?

    return plotdata

    
