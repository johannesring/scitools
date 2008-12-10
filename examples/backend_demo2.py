#!/usr/bin/env python
"""
Grab matplolib backend to prepare and tweak easyviz plots

 - Shows how to prepare matplotlib backend using rcParams before plotting 
 - Grab matplotlib backend to create thicker frames, tickmarks and fonts
 - Use both major and minor tick marks
 - Use backend to place text at an arbitrary position as a postprocess
"""

__author__ = 'Rolv Erlend Bredesen <rolv@simula.no>'

from scitools.all import *

def _pylab_thick_frame(lines=10,  width=5, size=8, labelsize=20):
    """Prepare matplotlib backend with parameters for a nice thick frame
    @param lines: width of plot lines
    @param width: width of frame line (and tick marks)
    @param size: length of tick marks
    @param labelsize: size of ticklables

    Developers notice:
     We use the markeredgewidth to set the width of the tick marks.
     lines.markeredgewidth will also change size of markers used in plots.
     It appears that this is the only way to set the width of tickmarks.
     The markeredgewidth applies to the black line surrounding a marker,
     making it appear circular and black if it's set to high. """
    plt._g.rcParams.update({
        'lines.linewidth': lines ,         # Plotline width
        'ytick.labelsize': labelsize,
        'ytick.major.pad': size,
        'ytick.minor.pad': size,
        'ytick.major.size': size*1.8,      # Tickmark length
        'ytick.minor.size': size,
        'xtick.labelsize': labelsize,
        'xtick.major.pad': size,
        'xtick.minor.pad': size,
        'xtick.major.size': size*1.8,        
        'xtick.minor.size': size,
        'lines.markeredgewidth': size/3,   # Tickmark border width 
        'axes.linewidth': width,           # Frame width
        })
    
def _pylab_major_minor(axis='y',
                       major_tick_interval=1, minor_tick_interval=.2):
    """Use both major and minor ticks on given axis.
    Must be applied as a postprocess after the easyviz plot"""
    if backend != 'matplotlib':
        return
    pylab = get_backend()
    # Use both major and minor ticks
    from matplotlib.ticker import MultipleLocator, FormatStrFormatter
    majorLocator = MultipleLocator(major_tick_interval)
    majorFormatter = FormatStrFormatter("%d")
    minorLocator = MultipleLocator(minor_tick_interval)
    if axis == 'x':
        axis = pylab.gca().xaxis
    elif axis == 'y':
        axis = pylab.gca().yaxis
    axis.set_minor_locator(minorLocator)
    axis.set_major_locator(majorLocator)
    axis.set_major_formatter(majorFormatter)
    # update backend
    pylab.draw()

def main():
    x = linspace(0, 5, 101)
    y = sin(2*pi*x)
    plot(y, '-o', x=x, log='x', xmin=.04, xmax=1, ymin=-1.1, ymax=1.1)
    
if __name__ == '__main__':
    main()
    hardcopy('normal_frame.png')

    if backend == 'matplotlib':

        # Setup parameters for thicker frame and tickmarks 
        _pylab_thick_frame()

        # Normal easyviz plotting
        main()

        # Major and minor ticks for the y axis
        _pylab_major_minor(axis='y')

        # Title using latex and specific fontsize 
        plt._g.title(r'y=sin(2\pi x)', fontsize=20) 

        # Place text at given location in plot (position by data coordinates)
        plt._g.text(.05, -.8, 'Check out the nice thick frame',
                    {'size':20}, horizontalalignment='left',)
        
        # Use backend hardcopy since normal hardcopy would reset text and title
        plt._g.savefig('thick_frame.png')  

        # Load a font set from matplotlib (check matplotlib's fonts_demo)
        from matplotlib.font_manager import fontManager, FontProperties
        plt._g.text(1, 1, 'Added some text using x-small font',
                    fontproperties=FontProperties(size='x-small'),
                    horizontalalignment='right',
                    transform=pylab.gca().transAxes)  # figure coordinates
            
    raw_input('press enter')
    