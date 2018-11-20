#file: vis_reg_result.py
#date: Nov. 7, 2018
#autor: Heather Kurtz
#Description: This code takes in the results from the regression test that 
#are kept in a txt file and plots them.

import glob
import numpy as np
import os
import argparse
import matplotlib.pyplot as plt
import pandas as pd
 
from bokeh.models import HoverTool
from bokeh.layouts import row
from bokeh.models import ColorBar
from bokeh.models import LogColorMapper
from bokeh.models import LogTicker
from bokeh.models import Plot
from bokeh.palettes import gray
from bokeh.plotting import ColumnDataSource
from bokeh.plotting import figure
from bokeh.plotting import output_file
from bokeh.plotting import save




def parse_args():
	"""Parse command line arguements.

	Parameters:
		Nothing

	Returns:
		arguments: argparse.Namespace object
			An object containing all of the added arguments.

	Outputs:
		Nothing
	"""

	#diff_help = 'Use flag to calculate differences.'
	#ratio_help = 'Use flag to calculate ratios.'
	#cte_help = 'Use flag to subtract flt from flc for same rootname'
	ncores_help = 'Number of cores to use for multiprocessing. Default value is 8.'
	first_help = 'Path to first image(s) to be compared.'
	file_help = 'file type to be compared.'

	ncores = 1

	parser = argparse.ArgumentParser()
	#parser.add_argument('-n', type=int, help=ncores_help, action='store',
	#	required=False, default=ncores)
	parser.add_argument('fp', type=str, metavar='first_path', help=first_help, action='store')
	parser.add_argument('ft', type=str, metavar='file_type', help=file_help, action='store')
	args=parser.parse_args()

	return args



def make_label_names(name_lsit):
    """Make an array of the ratio label names for the hover tool.

    Parameters
    ----------
    ratio_label_names : list
        The list of the strings wanted to create labels for the data.

    Returns
    -------
    hover_label_names : list
        The list of names wanted for the labels on the plot.
    """

    hover_label_names = []
    for x in range(len(name_lsit)):
        temp1 = name_lsit[x]
        hover_label_names.append(temp1)

    return hover_label_names

def make_hover_name(n_list, fname):
	n_list.append(fname)
	return(n_list)




def read_file(file, hdr,sk):
	#file=glob.glob(first_path)
	data=pd.read_csv(file,header=None, skiprows=sk, names=hdr, sep='\s+')
	return data


def make_dict_diff(diction,data,file,f_name):
	exts=data['EXTENSION']
	#f_name=file[-22:-9]
	for i in range(len(exts)):
		ext=str(data['EXTENSION'][i])
		mean=(data['MEAN'][i])
		median=(data['MEDIAN'][i])
		std=(data['STD'][i])
		mins=(data['MIN'][i])
		maxs=(data['MAX'][i])
		name=f_name+ext
		diction[name]=(ext,mean,median,std,mins,maxs)

	return(diction)

def make_dict_stats(diction,data,file,f_name):
	exts=data['EXT']
	#f_name=file[-28:-15]

	
	for i in range(len(exts)):
		ext=str(data['EXT'][i])
		mean=(data['MEAN'][i])
		median=(data['MED'][i])
		std=(data['STD'][i])
		mins=(data['MIN'][i])
		maxs=(data['MAX'][i])
		pe1=(data['1e-'][i])
		pe2=(data['2e-'][i])
		pe5=(data['5e-'][i])
		e10=(data['10e-'][i])
		pe50=(data['50e-'][i])
		name=f_name+ext
		diction[name] = (ext,mean,median,std,mins,maxs,pe1,pe2,pe5)

	return(diction)


def plots(first_path,file_type):
	#first_path='/grp/hst/wfc3v/hkurtz/crds_test/2018_3a/3a_2b_comp/Differences/*stats.txt'
	#file_type='stats'



	dic = {}
	name_list = []
	files_list = glob.glob(first_path)
	for file in files_list:
	
		if file_type == 'diff':
			hdr = ['EXTENSION','MEAN','MEDIAN','STD','MIN','MAX']
			sk = 2
			data = read_file(file, hdr,sk)
			f_name=file[-22:-9]
			dic = make_dict_diff(dic,data,file,f_name)
			name_list = make_hover_name(name_list, f_name)
	
		elif file_type == 'stats':
			hdr = ['EXT','TARG','FILT','MEAN','MED','STD','MIN','MAX','1e-', '2e-', '5e-', '10e-', '50e-']
			sk = 1
			data = read_file(file, hdr,sk)
			f_name=file[-28:-15]
			dic = make_dict_stats(dic,data,file, f_name)
			name_list = make_hover_name(name_list, f_name)

	#for key in dict:
	#	plt.scatter(dict[key][2],dict[key][4])
	#plt.show()

	#xdr = Range1d(start=-20.5, end=20.5)
	#ydr = Range1d(start=-20.5, end=20.5)

	


	plot_title='hope'
	#tools = "pan,wheel_zoom,box_zoom,reset,save,hover"
	#source = ColumnDataSource(data=dict(name=name_list))
	#TOOLTIPS = [
	#			('filename', '@name')
	#			]
	#hover = HoverTool(tooltips=TOOLTIPS)
	p = figure( title=plot_title, #tools=tools,
				plot_width=600, plot_height=500)

	#hover_names = make_label_names(name_list)
	#pd_names = pd.DataFrame(name_list)
	#source4 = ColumnDataSource(
	#	data=dict(
	#		name=hover_names,
	#		)
	#	)

	#source = ColumnDataSource(data=dict(name=name_list))
	#TOOLTIPS = [
	#			('filename', '@name')
	#			]
	#hover = HoverTool(tooltips=TOOLTIPS)
	#p.add_tools(hover)
	#hover = p.select#(dict(type=HoverTool))
	#hover.tooltips = hover_names
	#hover.names = ["name"]
	#hover.mode = 'mouse'
	#print(dic)

	for key in dic:
		p.circle(dic[key][2],dic[key][4])#,source=source)
	#p.show()
	#





	#tools = "pan,wheel_zoom,box_zoom,reset,save,hover"
	#p = figure(x_axis_type="datetime", y_range=(ymin, ymax), title=plot_title, tools=tools,
	#			plot_width=600, plot_height=500)
#
	## Build plots
	#p.circle(converted_date_4, shutter_dict['ratio_ext4'], source=source4, color='blue', legend='Chip 1', name='ext4')
#


#
	# Save Figure
	#fig_all=row(plot_ax)
	savefig_html = '{}.html'.format(file_type)
	#savefig_html = 'testing2.html'
	output_file(savefig_html)
	save(p)
#



if __name__=='__main__':
	"""
	Main Controller
	"""
	options = parse_args()
	plots(options.fp, options.ft)#, options.n)





























