# -*- coding: utf-8 -*-

# Copyright (C) 2010 - 2012, A. Murat Eren
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

import os
import sys
import copy
import numpy as np
import matplotlib.pyplot as plt
import cPickle

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
from utils.random_colors import random_colors
from utils.utils import HTMLColorToRGB
from utils.utils import get_oligos_sorted_by_abundance


def oligotype_distribution_across_datasets(datasets_dict, colors_dict, output_file = None, legend = False, project_title = None, display = True, oligos = None):
    datasets = datasets_dict.keys()
    datasets.sort()
   
    if oligos == None:
        oligos = get_oligos_sorted_by_abundance(datasets_dict, oligos)
    else:
        oligos.reverse()
 
    if colors_dict == None:
        colors_dict = random_colors(copy.deepcopy(oligos))


    oligo_percents = {}
    max_normalized_across_datasets_vectors = {}
    sum_normalized_across_datasets_vectors = {}

    for oligo in oligos:
        percents = []
        for dataset in datasets:
            if datasets_dict[dataset].has_key(oligo):
                percents.append(datasets_dict[dataset][oligo] * 100.0 / sum(datasets_dict[dataset].values()))
            else:
                percents.append(0.0)

        oligo_percents[oligo] = percents

    for oligo in oligos:
        max_normalized_across_datasets_vectors[oligo] = [p * 100.0 / max(oligo_percents[oligo]) for p in oligo_percents[oligo]]
        sum_normalized_across_datasets_vectors[oligo] = [p * 100.0 / sum(oligo_percents[oligo]) for p in oligo_percents[oligo]]


    # figure.. 
    fig = plt.figure(figsize=(20, 10))
    
    if legend:
        plt.subplots_adjust(left=0.03, bottom = 0.15, top = 0.97, right = 0.80)
    else:
        plt.subplots_adjust(left=0.03, bottom = 0.15, top = 0.97, right = 0.99)

    plt.rcParams.update({'axes.linewidth' : 0.1})
    plt.rc('grid', color='0.70', linestyle='-', linewidth=0.1)
    plt.grid(True) 
    plt.subplot(2, 1, 1)
    plt.grid(True) 

    N = len(datasets)
    ind = np.arange(N)
    width = 0.75
    
    lines = []
    
    for i in range(0, len(oligos)):
        oligo = oligos[i]
        try:
            color = HTMLColorToRGB(colors_dict[oligos[i]])
        except:
            color = 'black'

        if len(oligos) < 50:
            plt.plot(max_normalized_across_datasets_vectors[oligo], color=color, linewidth = 3, alpha = 0.3, zorder = i)
            plt.plot(max_normalized_across_datasets_vectors[oligo], color=color, linewidth = 5, alpha = 0.2, zorder = i)
        p = plt.plot(max_normalized_across_datasets_vectors[oligo], color=color, linewidth = 1, alpha = 0.9, zorder = i)
        lines.append(p)
    
    plt.ylabel('MAX Normalized', size='large')
    plt.title('Normalized Oligotype Distributions Across Datasets %s' \
                 % (('for "%s"' % project_title) if project_title else ''))

    plt.xticks(ind, ['' for d in datasets], rotation=90, size='small')
    plt.yticks([])
    plt.ylim(ymax = 100)
    plt.xlim(xmin = -(width) / 2, xmax = len(datasets) - 0.5)
    
    if legend:
        plt.legend([b[0] for b in lines][::-1], oligos[::-1], bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0.0, shadow=True, fancybox=True)
        
        leg = plt.gca().get_legend()
        ltext  = leg.get_texts()
        llines = leg.get_lines()
        frame  = leg.get_frame()
        
        frame.set_facecolor('0.80')
        plt.setp(ltext, fontsize='small', fontname='arial', family='monospace')
        plt.setp(llines, linewidth=1.5)


    plt.subplot(2, 1, 2)
    if legend:
        plt.subplots_adjust(left=0.03, bottom = 0.15, top = 0.97, right = 0.80)
    else:
        plt.subplots_adjust(left=0.03, bottom = 0.15, top = 0.97, right = 0.99)

    plt.rcParams.update({'axes.linewidth' : 0.1})
    plt.rc('grid', color='0.70', linestyle='-', linewidth=0.1)
    plt.grid(True) 
    
    for i in range(0, len(oligos)):
        oligo = oligos[i]
        try:
            color = HTMLColorToRGB(colors_dict[oligos[i]])
        except:
            color = 'black'

        if len(oligos) < 50:
            plt.plot(sum_normalized_across_datasets_vectors[oligo], color=color, linewidth = 3, alpha = 0.3, zorder = i)
            plt.plot(sum_normalized_across_datasets_vectors[oligo], color=color, linewidth = 5, alpha = 0.2, zorder = i)
        p = plt.plot(sum_normalized_across_datasets_vectors[oligo], color=color, linewidth = 1, alpha = 0.9, zorder = i)
    
    plt.ylabel('SUM Normalized', size='large')

    plt.xticks(ind, datasets, rotation=90, size='small')
    plt.yticks([])
    plt.ylim(ymax = 100)
    plt.xlim(xmin = -(width) / 2, xmax = len(datasets) - 0.5)
 
    if output_file:
        plt.savefig(output_file)
    if display:
        try:
            plt.show()
        except:
            pass

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Max Normalized Oligotype Distribution Across Datasets')
    parser.add_argument('environment_file', metavar = 'ENVIRONMENT_FILE',\
                        help = 'Oligotype distribution in datasets')
    parser.add_argument('--colors-file', metavar = 'COLORS_FILE', default = None,\
                        help = 'File that contains random colors for oligotypes')
    parser.add_argument('--output-file', default = None, metavar = 'OUTPUT_FILE',\
                        help = 'File name for the figure to be stored. File name\
                                must end with "png", "jpg", or "tiff".')
    parser.add_argument('--legend', action = 'store_true', default = False,
                        help = 'Turn on legend')
    parser.add_argument('--project-title', default = None, metavar = 'PROJECT_TITLE',\
                        help = 'Project name for the datasets.')


    args = parser.parse_args()

    datasets_dict = {}
    for oligotype, dataset, count in [line.strip().split('\t') for line in open(args.environment_file).readlines()]:
        if datasets_dict.has_key(dataset):
            if datasets_dict[dataset].has_key(oligotype):
                datasets_dict[dataset][oligotype] += int(count)
            else:
                datasets_dict[dataset][oligotype] = int(count)
        else:
            datasets_dict[dataset] = {}
            datasets_dict[dataset][oligotype] = int(count)


    if args.colors_file:
        colors_dict = {}
        for oligotype, color in [line.strip().split('\t') for line in open(args.colors_file).readlines()]:
            colors_dict[oligotype] = color
    else:
        colors_dict = None

    oligotype_distribution_across_datasets(datasets_dict, colors_dict, output_file = args.output_file, legend = args.legend, project_title = args.project_title)










