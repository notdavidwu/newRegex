import numpy as np
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

from numba import cuda
import tensorflow as tf

if tf.test.is_gpu_available():
    import cupy as cp
    def colormapping(img,colormap):
        #img_rgb=cp.zeros((img.shape+(3,)),dtype='int')
        img_rgb=colormap[img]
        return img_rgb.astype('uint8')

    def gray():
        color=cp.array([
            [0,0,0],
            [1,1,1],
            [2,2,2],
            [3,3,3],
            [4,4,4],
            [5,5,5],
            [6,6,6],
            [7,7,7],
            [8,8,8],
            [9,9,9],
            [10,10,10],
            [11,11,11],
            [12,12,12],
            [13,13,13],
            [14,14,14],
            [15,15,15],
            [16,16,16],
            [17,17,17],
            [18,18,18],
            [19,19,19],
            [20,20,20],
            [21,21,21],
            [22,22,22],
            [23,23,23],
            [24,24,24],
            [25,25,25],
            [26,26,26],
            [27,27,27],
            [28,28,28],
            [29,29,29],
            [30,30,30],
            [31,31,31],
            [32,32,32],
            [32,32,32],
            [34,34,34],
            [35,35,35],
            [36,36,36],
            [36,36,36],
            [38,38,38],
            [39,39,39],
            [40,40,40],
            [40,40,40],
            [42,42,42],
            [43,43,43],
            [44,44,44],
            [44,44,44],
            [46,46,46],
            [47,47,47],
            [48,48,48],
            [48,48,48],
            [50,50,50],
            [51,51,51],
            [52,52,52],
            [52,52,52],
            [54,54,54],
            [55,55,55],
            [56,56,56],
            [56,56,56],
            [58,58,58],
            [59,59,59],
            [60,60,60],
            [60,60,60],
            [62,62,62],
            [63,63,63],
            [64,64,64],
            [65,65,65],
            [65,65,65],
            [67,67,67],
            [68,68,68],
            [69,69,69],
            [70,70,70],
            [71,71,71],
            [72,72,72],
            [73,73,73],
            [73,73,73],
            [75,75,75],
            [76,76,76],
            [77,77,77],
            [78,78,78],
            [79,79,79],
            [80,80,80],
            [81,81,81],
            [81,81,81],
            [83,83,83],
            [84,84,84],
            [85,85,85],
            [86,86,86],
            [87,87,87],
            [88,88,88],
            [89,89,89],
            [89,89,89],
            [91,91,91],
            [92,92,92],
            [93,93,93],
            [94,94,94],
            [95,95,95],
            [96,96,96],
            [97,97,97],
            [97,97,97],
            [99,99,99],
            [100,100,100],
            [101,101,101],
            [102,102,102],
            [103,103,103],
            [104,104,104],
            [105,105,105],
            [105,105,105],
            [107,107,107],
            [108,108,108],
            [109,109,109],
            [110,110,110],
            [111,111,111],
            [112,112,112],
            [113,113,113],
            [113,113,113],
            [115,115,115],
            [116,116,116],
            [117,117,117],
            [118,118,118],
            [119,119,119],
            [120,120,120],
            [121,121,121],
            [121,121,121],
            [123,123,123],
            [124,124,124],
            [125,125,125],
            [126,126,126],
            [127,127,127],
            [128,128,128],
            [129,129,129],
            [130,130,130],
            [131,131,131],
            [131,131,131],
            [133,133,133],
            [134,134,134],
            [135,135,135],
            [136,136,136],
            [137,137,137],
            [138,138,138],
            [139,139,139],
            [140,140,140],
            [141,141,141],
            [142,142,142],
            [143,143,143],
            [144,144,144],
            [145,145,145],
            [146,146,146],
            [147,147,147],
            [147,147,147],
            [149,149,149],
            [150,150,150],
            [151,151,151],
            [152,152,152],
            [153,153,153],
            [154,154,154],
            [155,155,155],
            [156,156,156],
            [157,157,157],
            [158,158,158],
            [159,159,159],
            [160,160,160],
            [161,161,161],
            [162,162,162],
            [163,163,163],
            [163,163,163],
            [165,165,165],
            [166,166,166],
            [167,167,167],
            [168,168,168],
            [169,169,169],
            [170,170,170],
            [171,171,171],
            [172,172,172],
            [173,173,173],
            [174,174,174],
            [175,175,175],
            [176,176,176],
            [177,177,177],
            [178,178,178],
            [179,179,179],
            [179,179,179],
            [181,181,181],
            [182,182,182],
            [183,183,183],
            [184,184,184],
            [185,185,185],
            [186,186,186],
            [187,187,187],
            [188,188,188],
            [189,189,189],
            [190,190,190],
            [191,191,191],
            [192,192,192],
            [193,193,193],
            [194,194,194],
            [195,195,195],
            [195,195,195],
            [197,197,197],
            [198,198,198],
            [199,199,199],
            [200,200,200],
            [201,201,201],
            [202,202,202],
            [203,203,203],
            [204,204,204],
            [205,205,205],
            [206,206,206],
            [207,207,207],
            [208,208,208],
            [209,209,209],
            [210,210,210],
            [211,211,211],
            [211,211,211],
            [213,213,213],
            [214,214,214],
            [215,215,215],
            [216,216,216],
            [217,217,217],
            [218,218,218],
            [219,219,219],
            [220,220,220],
            [221,221,221],
            [222,222,222],
            [223,223,223],
            [224,224,224],
            [225,225,225],
            [226,226,226],
            [227,227,227],
            [227,227,227],
            [229,229,229],
            [230,230,230],
            [231,231,231],
            [232,232,232],
            [233,233,233],
            [234,234,234],
            [235,235,235],
            [236,236,236],
            [237,237,237],
            [238,238,238],
            [239,239,239],
            [240,240,240],
            [241,241,241],
            [242,242,242],
            [243,243,243],
            [243,243,243],
            [245,245,245],
            [246,246,246],
            [247,247,247],
            [248,248,248],
            [249,249,249],
            [250,250,250],
            [251,251,251],
            [252,252,252],
            [253,253,253],
            [254,254,254],
            [255,255,255]
            ]
        )
        return color



    def GE():
        color=cp.array([
        [0,0,0],
        [0,2,1],
        [0,4,3],
        [0,6,5],
        [0,8,7],
        [0,10,9],
        [0,12,11],
        [0,14,13],
        [0,16,15],
        [0,18,17],
        [0,20,19],
        [0,22,21],
        [0,24,23],
        [0,26,25],
        [0,28,27],
        [0,30,29],
        [0,32,31],
        [0,34,33],
        [0,36,35],
        [0,38,37],
        [0,40,39],
        [0,42,41],
        [0,44,43],
        [0,46,45],
        [0,48,47],
        [0,50,49],
        [0,52,51],
        [0,54,53],
        [0,56,55],
        [0,58,57],
        [0,60,59],
        [0,62,61],
        [0,65,63],
        [0,67,65],
        [0,69,67],
        [0,71,69],
        [0,73,71],
        [0,75,73],
        [0,77,75],
        [0,79,77],
        [0,81,79],
        [0,83,81],
        [0,85,83],
        [0,87,85],
        [0,89,87],
        [0,91,89],
        [0,93,91],
        [0,95,93],
        [0,97,95],
        [0,99,97],
        [0,101,99],
        [0,103,101],
        [0,105,103],
        [0,107,105],
        [0,109,107],
        [0,111,109],
        [0,113,111],
        [0,115,113],
        [0,117,115],
        [0,119,117],
        [0,121,119],
        [0,123,121],
        [0,125,123],
        [0,128,125],
        [1,126,127],
        [3,124,129],
        [5,122,131],
        [7,120,133],
        [9,118,135],
        [11,116,137],
        [13,114,139],
        [15,112,141],
        [17,110,143],
        [19,108,145],
        [21,106,147],
        [23,104,149],
        [25,102,151],
        [27,100,153],
        [29,98,155],
        [31,96,157],
        [33,94,159],
        [35,92,161],
        [37,90,163],
        [39,88,165],
        [41,86,167],
        [43,84,169],
        [45,82,171],
        [47,80,173],
        [49,78,175],
        [51,76,177],
        [53,74,179],
        [55,72,181],
        [57,70,183],
        [59,68,185],
        [61,66,187],
        [63,64,189],
        [65,63,191],
        [67,61,193],
        [69,59,195],
        [71,57,197],
        [73,55,199],
        [75,53,201],
        [77,51,203],
        [79,49,205],
        [81,47,207],
        [83,45,209],
        [85,43,211],
        [86,41,213],
        [88,39,215],
        [90,37,217],
        [92,35,219],
        [94,33,221],
        [96,31,223],
        [98,29,225],
        [100,27,227],
        [102,25,229],
        [104,23,231],
        [106,21,233],
        [108,19,235],
        [110,17,237],
        [112,15,239],
        [114,13,241],
        [116,11,243],
        [118,9,245],
        [120,7,247],
        [122,5,249],
        [124,3,251],
        [126,1,253],
        [128,0,255],
        [130,2,252],
        [132,4,248],
        [134,6,244],
        [136,8,240],
        [138,10,236],
        [140,12,232],
        [142,14,228],
        [144,16,224],
        [146,18,220],
        [148,20,216],
        [150,22,212],
        [152,24,208],
        [154,26,204],
        [156,28,200],
        [158,30,196],
        [160,32,192],
        [162,34,188],
        [164,36,184],
        [166,38,180],
        [168,40,176],
        [170,42,172],
        [171,44,168],
        [173,46,164],
        [175,48,160],
        [177,50,156],
        [179,52,152],
        [181,54,148],
        [183,56,144],
        [185,58,140],
        [187,60,136],
        [189,62,132],
        [191,64,128],
        [193,66,124],
        [195,68,120],
        [197,70,116],
        [199,72,112],
        [201,74,108],
        [203,76,104],
        [205,78,100],
        [207,80,96],
        [209,82,92],
        [211,84,88],
        [213,86,84],
        [215,88,80],
        [217,90,76],
        [219,92,72],
        [221,94,68],
        [223,96,64],
        [225,98,60],
        [227,100,56],
        [229,102,52],
        [231,104,48],
        [233,106,44],
        [235,108,40],
        [237,110,36],
        [239,112,32],
        [241,114,28],
        [243,116,24],
        [245,118,20],
        [247,120,16],
        [249,122,12],
        [251,124,8],
        [253,126,4],
        [255,128,0],
        [255,130,4],
        [255,132,8],
        [255,134,12],
        [255,136,16],
        [255,138,20],
        [255,140,24],
        [255,142,28],
        [255,144,32],
        [255,146,36],
        [255,148,40],
        [255,150,44],
        [255,152,48],
        [255,154,52],
        [255,156,56],
        [255,158,60],
        [255,160,64],
        [255,162,68],
        [255,164,72],
        [255,166,76],
        [255,168,80],
        [255,170,85],
        [255,172,89],
        [255,174,93],
        [255,176,97],
        [255,178,101],
        [255,180,105],
        [255,182,109],
        [255,184,113],
        [255,186,117],
        [255,188,121],
        [255,190,125],
        [255,192,129],
        [255,194,133],
        [255,196,137],
        [255,198,141],
        [255,200,145],
        [255,202,149],
        [255,204,153],
        [255,206,157],
        [255,208,161],
        [255,210,165],
        [255,212,170],
        [255,214,174],
        [255,216,178],
        [255,218,182],
        [255,220,186],
        [255,222,190],
        [255,224,194],
        [255,226,198],
        [255,228,202],
        [255,230,206],
        [255,232,210],
        [255,234,214],
        [255,236,218],
        [255,238,222],
        [255,240,226],
        [255,242,230],
        [255,244,234],
        [255,246,238],
        [255,248,242],
        [255,250,246],
        [255,252,250],
        [255,255,255]]
        )
        return color

    def binary():
        color=cp.array([
            [255,255,255],
            [254,254,254],
            [253,253,253],
            [252,252,252],
            [251,251,251],
            [250,250,250],
            [249,249,249],
            [248,248,248],
            [247,247,247],
            [246,246,246],
            [245,245,245],
            [244,244,244],
            [243,243,243],
            [242,242,242],
            [241,241,241],
            [240,240,240],
            [239,239,239],
            [238,238,238],
            [237,237,237],
            [236,236,236],
            [235,235,235],
            [234,234,234],
            [233,233,233],
            [232,232,232],
            [231,231,231],
            [230,230,230],
            [229,229,229],
            [228,228,228],
            [227,227,227],
            [226,226,226],
            [225,225,225],
            [224,224,224],
            [223,223,223],
            [222,222,222],
            [221,221,221],
            [220,220,220],
            [219,219,219],
            [218,218,218],
            [217,217,217],
            [216,216,216],
            [215,215,215],
            [214,214,214],
            [213,213,213],
            [211,211,211],
            [211,211,211],
            [210,210,210],
            [209,209,209],
            [208,208,208],
            [207,207,207],
            [206,206,206],
            [205,205,205],
            [204,204,204],
            [203,203,203],
            [202,202,202],
            [201,201,201],
            [200,200,200],
            [199,199,199],
            [198,198,198],
            [197,197,197],
            [195,195,195],
            [195,195,195],
            [194,194,194],
            [193,193,193],
            [192,192,192],
            [191,191,191],
            [190,190,190],
            [189,189,189],
            [188,188,188],
            [187,187,187],
            [186,186,186],
            [185,185,185],
            [184,184,184],
            [183,183,183],
            [182,182,182],
            [181,181,181],
            [179,179,179],
            [179,179,179],
            [178,178,178],
            [177,177,177],
            [176,176,176],
            [175,175,175],
            [174,174,174],
            [173,173,173],
            [172,172,172],
            [171,171,171],
            [170,170,170],
            [169,169,169],
            [168,168,168],
            [167,167,167],
            [166,166,166],
            [165,165,165],
            [163,163,163],
            [163,163,163],
            [162,162,162],
            [161,161,161],
            [160,160,160],
            [159,159,159],
            [158,158,158],
            [157,157,157],
            [156,156,156],
            [155,155,155],
            [154,154,154],
            [153,153,153],
            [152,152,152],
            [151,151,151],
            [150,150,150],
            [149,149,149],
            [147,147,147],
            [147,147,147],
            [146,146,146],
            [145,145,145],
            [144,144,144],
            [143,143,143],
            [142,142,142],
            [141,141,141],
            [140,140,140],
            [139,139,139],
            [138,138,138],
            [137,137,137],
            [136,136,136],
            [135,135,135],
            [134,134,134],
            [133,133,133],
            [131,131,131],
            [131,131,131],
            [130,130,130],
            [129,129,129],
            [128,128,128],
            [127,127,127],
            [126,126,126],
            [125,125,125],
            [124,124,124],
            [123,123,123],
            [121,121,121],
            [121,121,121],
            [120,120,120],
            [119,119,119],
            [118,118,118],
            [117,117,117],
            [116,116,116],
            [114,114,114],
            [113,113,113],
            [113,113,113],
            [112,112,112],
            [111,111,111],
            [110,110,110],
            [109,109,109],
            [108,108,108],
            [107,107,107],
            [105,105,105],
            [105,105,105],
            [104,104,104],
            [103,103,103],
            [102,102,102],
            [101,101,101],
            [100,100,100],
            [98,98,98],
            [97,97,97],
            [97,97,97],
            [96,96,96],
            [95,95,95],
            [94,94,94],
            [93,93,93],
            [92,92,92],
            [91,91,91],
            [89,89,89],
            [89,89,89],
            [88,88,88],
            [87,87,87],
            [86,86,86],
            [85,85,85],
            [84,84,84],
            [82,82,82],
            [81,81,81],
            [81,81,81],
            [80,80,80],
            [79,79,79],
            [78,78,78],
            [77,77,77],
            [76,76,76],
            [75,75,75],
            [73,73,73],
            [73,73,73],
            [72,72,72],
            [71,71,71],
            [70,70,70],
            [69,69,69],
            [68,68,68],
            [66,66,66],
            [65,65,65],
            [65,65,65],
            [64,64,64],
            [63,63,63],
            [62,62,62],
            [61,61,61],
            [60,60,60],
            [59,59,59],
            [57,57,57],
            [56,56,56],
            [56,56,56],
            [55,55,55],
            [54,54,54],
            [53,53,53],
            [52,52,52],
            [50,50,50],
            [49,49,49],
            [48,48,48],
            [48,48,48],
            [47,47,47],
            [46,46,46],
            [45,45,45],
            [44,44,44],
            [43,43,43],
            [41,41,41],
            [40,40,40],
            [40,40,40],
            [39,39,39],
            [38,38,38],
            [37,37,37],
            [36,36,36],
            [34,34,34],
            [33,33,33],
            [32,32,32],
            [32,32,32],
            [31,31,31],
            [30,30,30],
            [29,29,29],
            [28,28,28],
            [27,27,27],
            [25,25,25],
            [24,24,24],
            [24,24,24],
            [23,23,23],
            [22,22,22],
            [21,21,21],
            [20,20,20],
            [18,18,18],
            [17,17,17],
            [16,16,16],
            [16,16,16],
            [15,15,15],
            [14,14,14],
            [13,13,13],
            [12,12,12],
            [11,11,11],
            [9,9,9],
            [8,8,8],
            [8,8,8],
            [7,7,7],
            [6,6,6],
            [5,5,5],
            [4,4,4],
            [2,2,2],
            [1,1,1],
            [0,0,0],
            [0,0,0],
        ])
        return color

def GE_color_matplotlib():
    GE=np.array([
    [0,0,0,255],
    [0,2,1,255],
    [0,4,3,255],
    [0,6,5,255],
    [0,8,7,255],
    [0,10,9,255],
    [0,12,11,255],
    [0,14,13,255],
    [0,16,15,255],
    [0,18,17,255],
    [0,20,19,255],
    [0,22,21,255],
    [0,24,23,255],
    [0,26,25,255],
    [0,28,27,255],
    [0,30,29,255],
    [0,32,31,255],
    [0,34,33,255],
    [0,36,35,255],
    [0,38,37,255],
    [0,40,39,255],
    [0,42,41,255],
    [0,44,43,255],
    [0,46,45,255],
    [0,48,47,255],
    [0,50,49,255],
    [0,52,51,255],
    [0,54,53,255],
    [0,56,55,255],
    [0,58,57,255],
    [0,60,59,255],
    [0,62,61,255],
    [0,65,63,255],
    [0,67,65,255],
    [0,69,67,255],
    [0,71,69,255],
    [0,73,71,255],
    [0,75,73,255],
    [0,77,75,255],
    [0,79,77,255],
    [0,81,79,255],
    [0,83,81,255],
    [0,85,83,255],
    [0,87,85,255],
    [0,89,87,255],
    [0,91,89,255],
    [0,93,91,255],
    [0,95,93,255],
    [0,97,95,255],
    [0,99,97,255],
    [0,101,99,255],
    [0,103,101,255],
    [0,105,103,255],
    [0,107,105,255],
    [0,109,107,255],
    [0,111,109,255],
    [0,113,111,255],
    [0,115,113,255],
    [0,117,115,255],
    [0,119,117,255],
    [0,121,119,255],
    [0,123,121,255],
    [0,125,123,255],
    [0,128,125,255],
    [1,126,127,255],
    [3,124,129,255],
    [5,122,131,255],
    [7,120,133,255],
    [9,118,135,255],
    [11,116,137,255],
    [13,114,139,255],
    [15,112,141,255],
    [17,110,143,255],
    [19,108,145,255],
    [21,106,147,255],
    [23,104,149,255],
    [25,102,151,255],
    [27,100,153,255],
    [29,98,155,255],
    [31,96,157,255],
    [33,94,159,255],
    [35,92,161,255],
    [37,90,163,255],
    [39,88,165,255],
    [41,86,167,255],
    [43,84,169,255],
    [45,82,171,255],
    [47,80,173,255],
    [49,78,175,255],
    [51,76,177,255],
    [53,74,179,255],
    [55,72,181,255],
    [57,70,183,255],
    [59,68,185,255],
    [61,66,187,255],
    [63,64,189,255],
    [65,63,191,255],
    [67,61,193,255],
    [69,59,195,255],
    [71,57,197,255],
    [73,55,199,255],
    [75,53,201,255],
    [77,51,203,255],
    [79,49,205,255],
    [81,47,207,255],
    [83,45,209,255],
    [85,43,211,255],
    [86,41,213,255],
    [88,39,215,255],
    [90,37,217,255],
    [92,35,219,255],
    [94,33,221,255],
    [96,31,223,255],
    [98,29,225,255],
    [100,27,227,255],
    [102,25,229,255],
    [104,23,231,255],
    [106,21,233,255],
    [108,19,235,255],
    [110,17,237,255],
    [112,15,239,255],
    [114,13,241,255],
    [116,11,243,255],
    [118,9,245,255],
    [120,7,247,255],
    [122,5,249,255],
    [124,3,251,255],
    [126,1,253,255],
    [128,0,255,255],
    [130,2,252,255],
    [132,4,248,255],
    [134,6,244,255],
    [136,8,240,255],
    [138,10,236,255],
    [140,12,232,255],
    [142,14,228,255],
    [144,16,224,255],
    [146,18,220,255],
    [148,20,216,255],
    [150,22,212,255],
    [152,24,208,255],
    [154,26,204,255],
    [156,28,200,255],
    [158,30,196,255],
    [160,32,192,255],
    [162,34,188,255],
    [164,36,184,255],
    [166,38,180,255],
    [168,40,176,255],
    [170,42,172,255],
    [171,44,168,255],
    [173,46,164,255],
    [175,48,160,255],
    [177,50,156,255],
    [179,52,152,255],
    [181,54,148,255],
    [183,56,144,255],
    [185,58,140,255],
    [187,60,136,255],
    [189,62,132,255],
    [191,64,128,255],
    [193,66,124,255],
    [195,68,120,255],
    [197,70,116,255],
    [199,72,112,255],
    [201,74,108,255],
    [203,76,104,255],
    [205,78,100,255],
    [207,80,96,255],
    [209,82,92,255],
    [211,84,88,255],
    [213,86,84,255],
    [215,88,80,255],
    [217,90,76,255],
    [219,92,72,255],
    [221,94,68,255],
    [223,96,64,255],
    [225,98,60,255],
    [227,100,56,255],
    [229,102,52,255],
    [231,104,48,255],
    [233,106,44,255],
    [235,108,40,255],
    [237,110,36,255],
    [239,112,32,255],
    [241,114,28,255],
    [243,116,24,255],
    [245,118,20,255],
    [247,120,16,255],
    [249,122,12,255],
    [251,124,8,255],
    [253,126,4,255],
    [255,128,0,255],
    [255,130,4,255],
    [255,132,8,255],
    [255,134,12,255],
    [255,136,16,255],
    [255,138,20,255],
    [255,140,24,255],
    [255,142,28,255],
    [255,144,32,255],
    [255,146,36,255],
    [255,148,40,255],
    [255,150,44,255],
    [255,152,48,255],
    [255,154,52,255],
    [255,156,56,255],
    [255,158,60,255],
    [255,160,64,255],
    [255,162,68,255],
    [255,164,72,255],
    [255,166,76,255],
    [255,168,80,255],
    [255,170,85,255],
    [255,172,89,255],
    [255,174,93,255],
    [255,176,97,255],
    [255,178,101,255],
    [255,180,105,255],
    [255,182,109,255],
    [255,184,113,255],
    [255,186,117,255],
    [255,188,121,255],
    [255,190,125,255],
    [255,192,129,255],
    [255,194,133,255],
    [255,196,137,255],
    [255,198,141,255],
    [255,200,145,255],
    [255,202,149,255],
    [255,204,153,255],
    [255,206,157,255],
    [255,208,161,255],
    [255,210,165,255],
    [255,212,170,255],
    [255,214,174,255],
    [255,216,178,255],
    [255,218,182,255],
    [255,220,186,255],
    [255,222,190,255],
    [255,224,194,255],
    [255,226,198,255],
    [255,228,202,255],
    [255,230,206,255],
    [255,232,210,255],
    [255,234,214,255],
    [255,236,218,255],
    [255,238,222,255],
    [255,240,226,255],
    [255,242,230,255],
    [255,244,234,255],
    [255,246,238,255],
    [255,248,242,255],
    [255,250,246,255],
    [255,252,250,255],
    [255,255,255,255]]
    )
    GE=GE/255.0
    GE=ListedColormap(GE)
    return GE

def GE_color_opencv():
    GE=np.array([[
    [0,0,0],
    [0,2,1],
    [0,4,3],
    [0,6,5],
    [0,8,7],
    [0,10,9],
    [0,12,11],
    [0,14,13],
    [0,16,15],
    [0,18,17],
    [0,20,19],
    [0,22,21],
    [0,24,23],
    [0,26,25],
    [0,28,27],
    [0,30,29],
    [0,32,31],
    [0,34,33],
    [0,36,35],
    [0,38,37],
    [0,40,39],
    [0,42,41],
    [0,44,43],
    [0,46,45],
    [0,48,47],
    [0,50,49],
    [0,52,51],
    [0,54,53],
    [0,56,55],
    [0,58,57],
    [0,60,59],
    [0,62,61],
    [0,65,63],
    [0,67,65],
    [0,69,67],
    [0,71,69],
    [0,73,71],
    [0,75,73],
    [0,77,75],
    [0,79,77],
    [0,81,79],
    [0,83,81],
    [0,85,83],
    [0,87,85],
    [0,89,87],
    [0,91,89],
    [0,93,91],
    [0,95,93],
    [0,97,95],
    [0,99,97],
    [0,101,99],
    [0,103,101],
    [0,105,103],
    [0,107,105],
    [0,109,107],
    [0,111,109],
    [0,113,111],
    [0,115,113],
    [0,117,115],
    [0,119,117],
    [0,121,119],
    [0,123,121],
    [0,125,123],
    [0,128,125],
    [1,126,127],
    [3,124,129],
    [5,122,131],
    [7,120,133],
    [9,118,135],
    [11,116,137],
    [13,114,139],
    [15,112,141],
    [17,110,143],
    [19,108,145],
    [21,106,147],
    [23,104,149],
    [25,102,151],
    [27,100,153],
    [29,98,155],
    [31,96,157],
    [33,94,159],
    [35,92,161],
    [37,90,163],
    [39,88,165],
    [41,86,167],
    [43,84,169],
    [45,82,171],
    [47,80,173],
    [49,78,175],
    [51,76,177],
    [53,74,179],
    [55,72,181],
    [57,70,183],
    [59,68,185],
    [61,66,187],
    [63,64,189],
    [65,63,191],
    [67,61,193],
    [69,59,195],
    [71,57,197],
    [73,55,199],
    [75,53,201],
    [77,51,203],
    [79,49,205],
    [81,47,207],
    [83,45,209],
    [85,43,211],
    [86,41,213],
    [88,39,215],
    [90,37,217],
    [92,35,219],
    [94,33,221],
    [96,31,223],
    [98,29,225],
    [100,27,227],
    [102,25,229],
    [104,23,231],
    [106,21,233],
    [108,19,235],
    [110,17,237],
    [112,15,239],
    [114,13,241],
    [116,11,243],
    [118,9,245],
    [120,7,247],
    [122,5,249],
    [124,3,251],
    [126,1,253],
    [128,0,255],
    [130,2,252],
    [132,4,248],
    [134,6,244],
    [136,8,240],
    [138,10,236],
    [140,12,232],
    [142,14,228],
    [144,16,224],
    [146,18,220],
    [148,20,216],
    [150,22,212],
    [152,24,208],
    [154,26,204],
    [156,28,200],
    [158,30,196],
    [160,32,192],
    [162,34,188],
    [164,36,184],
    [166,38,180],
    [168,40,176],
    [170,42,172],
    [171,44,168],
    [173,46,164],
    [175,48,160],
    [177,50,156],
    [179,52,152],
    [181,54,148],
    [183,56,144],
    [185,58,140],
    [187,60,136],
    [189,62,132],
    [191,64,128],
    [193,66,124],
    [195,68,120],
    [197,70,116],
    [199,72,112],
    [201,74,108],
    [203,76,104],
    [205,78,100],
    [207,80,96],
    [209,82,92],
    [211,84,88],
    [213,86,84],
    [215,88,80],
    [217,90,76],
    [219,92,72],
    [221,94,68],
    [223,96,64],
    [225,98,60],
    [227,100,56],
    [229,102,52],
    [231,104,48],
    [233,106,44],
    [235,108,40],
    [237,110,36],
    [239,112,32],
    [241,114,28],
    [243,116,24],
    [245,118,20],
    [247,120,16],
    [249,122,12],
    [251,124,8],
    [253,126,4],
    [255,128,0],
    [255,130,4],
    [255,132,8],
    [255,134,12],
    [255,136,16],
    [255,138,20],
    [255,140,24],
    [255,142,28],
    [255,144,32],
    [255,146,36],
    [255,148,40],
    [255,150,44],
    [255,152,48],
    [255,154,52],
    [255,156,56],
    [255,158,60],
    [255,160,64],
    [255,162,68],
    [255,164,72],
    [255,166,76],
    [255,168,80],
    [255,170,85],
    [255,172,89],
    [255,174,93],
    [255,176,97],
    [255,178,101],
    [255,180,105],
    [255,182,109],
    [255,184,113],
    [255,186,117],
    [255,188,121],
    [255,190,125],
    [255,192,129],
    [255,194,133],
    [255,196,137],
    [255,198,141],
    [255,200,145],
    [255,202,149],
    [255,204,153],
    [255,206,157],
    [255,208,161],
    [255,210,165],
    [255,212,170],
    [255,214,174],
    [255,216,178],
    [255,218,182],
    [255,220,186],
    [255,222,190],
    [255,224,194],
    [255,226,198],
    [255,228,202],
    [255,230,206],
    [255,232,210],
    [255,234,214],
    [255,236,218],
    [255,238,222],
    [255,240,226],
    [255,242,230],
    [255,244,234],
    [255,246,238],
    [255,248,242],
    [255,250,246],
    [255,252,250],
    [255,255,255]]]
    )
    GE = GE.transpose(1, 0, 2)
    GE = GE.astype(np.uint8)
    return GE

def GE_color_vispy():
    GE=np.array([[
    [0,0,0],
    [0,2,1],
    [0,4,3],
    [0,6,5],
    [0,8,7],
    [0,10,9],
    [0,12,11],
    [0,14,13],
    [0,16,15],
    [0,18,17],
    [0,20,19],
    [0,22,21],
    [0,24,23],
    [0,26,25],
    [0,28,27],
    [0,30,29],
    [0,32,31],
    [0,34,33],
    [0,36,35],
    [0,38,37],
    [0,40,39],
    [0,42,41],
    [0,44,43],
    [0,46,45],
    [0,48,47],
    [0,50,49],
    [0,52,51],
    [0,54,53],
    [0,56,55],
    [0,58,57],
    [0,60,59],
    [0,62,61],
    [0,65,63],
    [0,67,65],
    [0,69,67],
    [0,71,69],
    [0,73,71],
    [0,75,73],
    [0,77,75],
    [0,79,77],
    [0,81,79],
    [0,83,81],
    [0,85,83],
    [0,87,85],
    [0,89,87],
    [0,91,89],
    [0,93,91],
    [0,95,93],
    [0,97,95],
    [0,99,97],
    [0,101,99],
    [0,103,101],
    [0,105,103],
    [0,107,105],
    [0,109,107],
    [0,111,109],
    [0,113,111],
    [0,115,113],
    [0,117,115],
    [0,119,117],
    [0,121,119],
    [0,123,121],
    [0,125,123],
    [0,128,125],
    [1,126,127],
    [3,124,129],
    [5,122,131],
    [7,120,133],
    [9,118,135],
    [11,116,137],
    [13,114,139],
    [15,112,141],
    [17,110,143],
    [19,108,145],
    [21,106,147],
    [23,104,149],
    [25,102,151],
    [27,100,153],
    [29,98,155],
    [31,96,157],
    [33,94,159],
    [35,92,161],
    [37,90,163],
    [39,88,165],
    [41,86,167],
    [43,84,169],
    [45,82,171],
    [47,80,173],
    [49,78,175],
    [51,76,177],
    [53,74,179],
    [55,72,181],
    [57,70,183],
    [59,68,185],
    [61,66,187],
    [63,64,189],
    [65,63,191],
    [67,61,193],
    [69,59,195],
    [71,57,197],
    [73,55,199],
    [75,53,201],
    [77,51,203],
    [79,49,205],
    [81,47,207],
    [83,45,209],
    [85,43,211],
    [86,41,213],
    [88,39,215],
    [90,37,217],
    [92,35,219],
    [94,33,221],
    [96,31,223],
    [98,29,225],
    [100,27,227],
    [102,25,229],
    [104,23,231],
    [106,21,233],
    [108,19,235],
    [110,17,237],
    [112,15,239],
    [114,13,241],
    [116,11,243],
    [118,9,245],
    [120,7,247],
    [122,5,249],
    [124,3,251],
    [126,1,253],
    [128,0,255],
    [130,2,252],
    [132,4,248],
    [134,6,244],
    [136,8,240],
    [138,10,236],
    [140,12,232],
    [142,14,228],
    [144,16,224],
    [146,18,220],
    [148,20,216],
    [150,22,212],
    [152,24,208],
    [154,26,204],
    [156,28,200],
    [158,30,196],
    [160,32,192],
    [162,34,188],
    [164,36,184],
    [166,38,180],
    [168,40,176],
    [170,42,172],
    [171,44,168],
    [173,46,164],
    [175,48,160],
    [177,50,156],
    [179,52,152],
    [181,54,148],
    [183,56,144],
    [185,58,140],
    [187,60,136],
    [189,62,132],
    [191,64,128],
    [193,66,124],
    [195,68,120],
    [197,70,116],
    [199,72,112],
    [201,74,108],
    [203,76,104],
    [205,78,100],
    [207,80,96],
    [209,82,92],
    [211,84,88],
    [213,86,84],
    [215,88,80],
    [217,90,76],
    [219,92,72],
    [221,94,68],
    [223,96,64],
    [225,98,60],
    [227,100,56],
    [229,102,52],
    [231,104,48],
    [233,106,44],
    [235,108,40],
    [237,110,36],
    [239,112,32],
    [241,114,28],
    [243,116,24],
    [245,118,20],
    [247,120,16],
    [249,122,12],
    [251,124,8],
    [253,126,4],
    [255,128,0],
    [255,130,4],
    [255,132,8],
    [255,134,12],
    [255,136,16],
    [255,138,20],
    [255,140,24],
    [255,142,28],
    [255,144,32],
    [255,146,36],
    [255,148,40],
    [255,150,44],
    [255,152,48],
    [255,154,52],
    [255,156,56],
    [255,158,60],
    [255,160,64],
    [255,162,68],
    [255,164,72],
    [255,166,76],
    [255,168,80],
    [255,170,85],
    [255,172,89],
    [255,174,93],
    [255,176,97],
    [255,178,101],
    [255,180,105],
    [255,182,109],
    [255,184,113],
    [255,186,117],
    [255,188,121],
    [255,190,125],
    [255,192,129],
    [255,194,133],
    [255,196,137],
    [255,198,141],
    [255,200,145],
    [255,202,149],
    [255,204,153],
    [255,206,157],
    [255,208,161],
    [255,210,165],
    [255,212,170],
    [255,214,174],
    [255,216,178],
    [255,218,182],
    [255,220,186],
    [255,222,190],
    [255,224,194],
    [255,226,198],
    [255,228,202],
    [255,230,206],
    [255,232,210],
    [255,234,214],
    [255,236,218],
    [255,238,222],
    [255,240,226],
    [255,242,230],
    [255,244,234],
    [255,246,238],
    [255,248,242],
    [255,250,246],
    [255,252,250],
    [255,255,255]]]
    )

    GE = GE/255
    return GE
