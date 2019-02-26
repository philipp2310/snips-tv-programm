#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import io
import sys
import paho.mqtt.publish as publish

# webView loads a html file and creates a single output line that can be transfered via MQTT
class webView:
    def __init__(self, htmlFile, appName, siteID='default'):
        self.appName = appName
        self.htmlFile = htmlFile
        self.html = ""
        self.topic = "wilma/"+siteID+"/"+appName
        self.read_file()

    def read_file(self):
        try:
            with io.open(self.htmlFile, 'r') as myfile:
                self.html = myfile.read().replace('\n', '')
        except EOFError:
            return []

# <style type="text/css">
#//CSS goes here
#</style>
#<script type="text/javascript">
#//Javascript goes here
#</script>
    def insert_includes(self):
        self.html = self.html
        
    def insert_data(self, field, data):
        self.html = self.html.replace('{{'+field+'}}',data,1)
        
    def send_to_display(self):
        publish.single(self.topic, self.html, hostname="localhost", port=1883)
        
    def do_replacements(self):
        proSieben = "<svg xmlns:svg='http://www.w3.org/2000/svg' xmlns='http://www.w3.org/2000/svg' version='1.0' width='10VW' height='10VW' viewBox='0 0 240 240'><polygon points='47.9181,86.2395 137.082,86.2395 137.082,110.95 47.9181,110.95 47.9181,86.2395 ' transform='matrix(2.28487,0,0,2.28487,-118.8506,-168.0882)' style='fill:#d90824'/><path d='M 193.89327,96.239271 L 193.89327,232.68508 L -9.3639709,232.68508 C -9.3639709,232.68508 15.572872,166.34411 80.972706,127.29248 C 143.0789,89.652219 193.89327,96.239271 193.89327,96.239271 L 193.89327,96.239271 z ' style='fill:#d90824'/></svg>"
        satEins = "<svg xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' version='1.1' width='10VW' height='10VW' viewBox='0 0 104.509 104.322'><g id='SAT1'><path id='SAT.1_1_' style='fill:#FFFFFF;' d='M98.959,75.709c-8.811,15.449-45.203,21.145-79.295,0.405l-0.001,0.002   c27.138,25.689,53.827,24.951,65.461,16.758c-6.996,5.668-15.482,9.566-24.782,11.011c-0.012-0.025-0.026-0.049-0.038-0.074   c-17.478,2.487-29.072-3.704-40.643-27.692c0,0,0.002-0.002,0.003-0.003c-0.002-0.002-0.005-0.004-0.007-0.006   c2.306,12.907,8.024,22.269,15.737,25.618c-7.042-2.399-13.405-6.261-18.733-11.221c-2.468-3.571,2.161-12.473,2.996-14.396   c-0.973,0.917-6.418,4.958-9.417,7.214C6.587,78.394,3.783,72.8,2.04,66.755c2.621,6.311,14.103,8.529,17.615,9.355   c-4.784-2.272-17.73-9.768-19.582-21.077C0.025,54.113,0,53.187,0,52.255c0-10.347,3.008-19.992,8.197-28.108   c-10.3,21.604,4.506,42.597,11.459,51.963C2.695,41.067,12.627,17.224,22.789,9.097C31.178,3.359,41.323,0,52.254,0   c2.827,0,5.6,0.228,8.305,0.66c-20.304,0.53-41.277,39.81-40.904,75.45C28.915,45.442,62.85,2.556,76.963,6.202   c8.946,4.81,16.329,12.148,21.192,21.06c-5.88,8.798-55.004,38.744-78.488,48.843c0,0,0,0.003-0.001,0.005   c22.554,1.406,81.884-16.905,83.766-34.416c0.003,0,0.006,0,0.01,0c0.7,3.411,1.068,6.942,1.068,10.56   C104.509,60.689,102.508,68.656,98.959,75.709z'/></g></svg>"
        kabelEins = "<svg width='10VW' height='10VW' viewBox='0 0 700 450' xmlns:dc='http://purl.org/dc/elements/1.1/' xmlns:cc='http://creativecommons.org/ns#' xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#' xmlns:svg='http://www.w3.org/2000/svg' xmlns='http://www.w3.org/2000/svg' version='1.1' width='906.10999' height='607.03003' viewBox='0 0 724.88799 485.62402' id='svg3027'><metadata id='metadata3064'><rdf:RDF><cc:Work rdf:about=''><dc:format>image/svg+xml</dc:format><dc:type rdf:resource='http://purl.org/dc/dcmitype/StillImage'/><dc:title/></cc:Work></rdf:RDF></metadata><defs id='defs3062'/><path d='m 0,0 0,171.75 c 1.2498075,27.05829 3.0945585,54.17915 8.34375,80.8125 8.336216,43.85567 24.691928,87.17414 53.4375,121.84375 26.658394,32.7074 63.74364,55.87079 103.625,68.96875 43.5058,14.88519 90.88196,18.85492 136.125,10.34375 37.08179,-7.23636 72.65453,-22.97871 102.0625,-46.8125 39.15646,-31.38261 66.80188,-76.33256 78.9375,-124.875 L 374,303.28125 c 1.16231,-36.0944 2.3188,-73.16188 2.65625,-109.28125 40.66874,-9.0361 80.50476,-26.14818 111.4375,-54.59375 23.42139,-21.28419 40.66315,-50.09243 44.875,-81.75 11.51072,-1.837214 23.09551,-3.131555 34.59375,-5.09375 50.14227,-8.41119 100.16378,-18.189709 149.03125,-32.375 9.64851,23.871282 18.55729,48.085125 25.21875,72.96875 6.73646,24.74615 11.59404,50.07273 13.46875,75.65625 4.84925,95.84757 -25.82171,193.19921 -85.625,268.375 -28.37064,35.79442 -63.0435,66.62246 -102,90.46875 -57.95356,35.68195 -125.09795,55.6506 -192.9375,59.5 -29.80791,2.21215 -59.92951,0.67401 -89.1875,-5.625 -39.81886,-8.29871 -77.94931,-23.41539 -114.03125,-42 C 158.86445,532.88229 146.06696,526.3362 134.46875,517.9375 98.96172,493.40383 65.827334,464.63827 40.40625,429.53125 24.808653,408.33455 12.535877,384.965 2,360.90625 1.3625981,359.46898 0.66239797,358.01852 0,356.59375 l 0,250.4375 906.125,0 L 906.125,0 0,0 z' transform='matrix(0.8,0,0,0.8,0,-2.2944709e-6)' id='path3030' style='fill:#ff3801;fill-opacity:1'/></svg>"
        vox = "<svg width='10VW' height='10VW' viewBox='0 0 1024 400' xmlns:dc='http://purl.org/dc/elements/1.1/' xmlns:cc='http://creativecommons.org/ns#' xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#' xmlns:svg='http://www.w3.org/2000/svg' xmlns='http://www.w3.org/2000/svg' xmlns:sodipodi='http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd' xmlns:inkscape='http://www.inkscape.org/namespaces/inkscape' width='1024' height='330' id='svg2' sodipodi:version='0.32' inkscape:version='0.46' version='1.0' sodipodi:docname='VOX.svg' inkscape:output_extension='org.inkscape.output.svg.inkscape'><defs id='defs4'/><sodipodi:namedview id='base' pagecolor='#ffffff' bordercolor='#666666' borderopacity='1.0' inkscape:pageopacity='0.0' inkscape:pageshadow='2' inkscape:zoom='0.70710678' inkscape:cx='398.83566' inkscape:cy='407.78511' inkscape:document-units='px' inkscape:current-layer='layer1' showgrid='false' inkscape:window-width='1024' inkscape:window-height='718' inkscape:window-x='-8' inkscape:window-y='-8'/><metadata id='metadata7'><rdf:RDF><cc:Work rdf:about=''><dc:format>image/svg+xml</dc:format><dc:type rdf:resource='http://purl.org/dc/dcmitype/StillImage'/></cc:Work></rdf:RDF></metadata><g inkscape:label='Ebene 1' inkscape:groupmode='layer' id='layer1'><g id='g4789'><path d='M 282.66694,328.5971 L 180.04619,328.5971 L 2.340149,4.9227558 L 162.05096,4.9227558 L 232.98446,142.41085 L 305.93707,4.9227558 L 432.87536,4.9227558 C 379.97494,36.673103 344.04758,95.921068 344.04758,162.57661 C 344.04758,178.43916 346.11716,194.31433 349.272,209.10424' style='fill:#FFFFFF;fill-opacity:1;fill-rule:evenodd;stroke:none' id='path2792'/><path d='M 720.55925,328.5971 L 606.29081,328.5971 C 667.70931,298.96681 711.04424,235.52921 711.04424,162.57661 C 711.04424,95.921068 675.10426,36.673103 621.18167,4.9227558 L 748.10735,4.9227558 L 790.40749,59.94323 L 832.69502,4.9227558 L 1012.5211,4.9227558 L 874.01085,158.3365 L 1022.0361,328.5971 L 846.45014,328.5971 L 787.20217,254.55923' style='fill:#FFFFFF;fill-opacity:1;fill-rule:evenodd;stroke:none' id='path2794'/><g style='fill:#e50000;fill-opacity:1' transform='matrix(42.064583,0,0,42.064583,-8385.0681,-6996.6186)' id='g3993'><path id='path2796' style='fill:#e50000;fill-opacity:1;fill-rule:evenodd;stroke:none' d='M 210.20739,170.21992 C 210.20739,169.34092 210.93519,168.61072 211.81659,168.61072 C 212.72109,168.61072 213.42549,169.34092 213.42549,170.21992 C 213.42549,171.12442 212.72109,171.83002 211.81659,171.83002 C 210.93519,171.83002 210.20739,171.12442 210.20739,170.21992'/></g></g></g></svg>"
        rtl = "<svg width='10VW' height='10VW' viewBox='0 0 1000 250' xmlns:dc='http://purl.org/dc/elements/1.1/' xmlns:cc='http://creativecommons.org/ns#' xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#' xmlns:svg='http://www.w3.org/2000/svg' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' xmlns:sodipodi='http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd' xmlns:inkscape='http://www.inkscape.org/namespaces/inkscape' width='1024' height='280' id='svg2409' sodipodi:version='0.32' inkscape:version='0.46' version='1.0' sodipodi:docname='RTL.svg' inkscape:output_extension='org.inkscape.output.svg.inkscape'><defs id='defs2411'><inkscape:perspective sodipodi:type='inkscape:persp3d' inkscape:vp_x='0 : 526.18109 : 1' inkscape:vp_y='0 : 1000 : 0' inkscape:vp_z='744.09448 : 526.18109 : 1' inkscape:persp3d-origin='372.04724 : 350.78739 : 1' id='perspective2417'/><metadata id='CorelCorpID_0Corel-Layer'/><style id='style6' type='text/css'>.fil9 {fill:none;fill-rule:nonzero}.fil4 {fill:#1F1A17}.fil3 {fill:#255393}.fil1 {fill:#B63546}.fil2 {fill:#E2AC19}.fil0 {fill:white}.fil8 {fill:white;fill-rule:nonzero}.fil5 {fill:#235598;fill-rule:nonzero}.fil6 {fill:#BD4748;fill-rule:nonzero}.fil7 {fill:#EDAC2F;fill-rule:nonzero}</style><inkscape:perspective id='perspective61' inkscape:persp3d-origin='372.04724 : 350.78739 : 1' inkscape:vp_z='744.09448 : 526.18109 : 1' inkscape:vp_y='0 : 1000 : 0' inkscape:vp_x='0 : 526.18109 : 1' sodipodi:type='inkscape:persp3d'/><inkscape:perspective sodipodi:type='inkscape:persp3d' inkscape:vp_x='0 : 80.5 : 1' inkscape:vp_y='0 : 1000 : 0' inkscape:vp_z='587 : 80.5 : 1' inkscape:persp3d-origin='293.5 : 53.666667 : 1' id='perspective38'/><defs id='defs10'><rect width='737.34302' height='365.832' x='0' y='0' id='XMLID_24_'/></defs><clipPath id='XMLID_33_'><use id='use14' x='0' y='0' width='587' height='161' xlink:href='#XMLID_24_'/></clipPath><defs id='defs18'><rect id='XMLID_23_' y='0' x='0' height='365.832' width='737.34302'/></defs><clipPath id='XMLID_34_'><use xlink:href='#XMLID_23_' height='161' width='587' y='0' x='0' id='use22'/></clipPath><defs id='defs26'><rect width='737.34302' height='365.832' x='0' y='0' id='XMLID_22_'/></defs><clipPath id='XMLID_35_'><use id='use30' x='0' y='0' width='587' height='161' xlink:href='#XMLID_22_'/></clipPath><defs id='defs34'><polyline points='32.162,78.613 32.162,238.962 618.639,238.962 618.639,78.613 ' id='XMLID_21_'/></defs><clipPath id='XMLID_36_'><use xlink:href='#XMLID_21_' height='161' width='587' y='0' x='0' id='use38'/></clipPath><inkscape:perspective id='perspective3313' inkscape:persp3d-origin='372.04724 : 350.78739 : 1' inkscape:vp_z='744.09448 : 526.18109 : 1' inkscape:vp_y='0 : 1000 : 0' inkscape:vp_x='0 : 526.18109 : 1' sodipodi:type='inkscape:persp3d'/></defs><sodipodi:namedview id='base' pagecolor='#ffffff' bordercolor='#666666' borderopacity='1.0' inkscape:pageopacity='0.0' inkscape:pageshadow='2' inkscape:zoom='0.7' inkscape:cx='632.15815' inkscape:cy='9.9653781' inkscape:document-units='px' inkscape:current-layer='layer1' showgrid='false' inkscape:window-width='1440' inkscape:window-height='850' inkscape:window-x='-8' inkscape:window-y='-8'/><metadata id='metadata2414'><rdf:RDF><cc:Work rdf:about=''><dc:format>image/svg+xml</dc:format><dc:type rdf:resource='http://purl.org/dc/dcmitype/StillImage'/></cc:Work></rdf:RDF></metadata><g inkscape:label='Ebene 1' inkscape:groupmode='layer' id='layer1'><g id='g3221'><g id='g2539'><polygon id='_12021680' class='fil4' points='83.1838,114.932 83.1838,114.695 85.5785,114.695 85.5785,114.932 84.582,114.932 84.582,116.779 84.1885,116.779 84.1885,114.932 83.1838,114.932 ' style='fill:#1f1a17;fill-rule:evenodd' transform='matrix(15.313361,0,0,15.313361,-1261.7633,-1515.8943)'/><polygon id='_12021392' class='fil4' points='92.754,114.695 92.754,114.932 91.029,114.932 91.029,115.59 92.6868,115.59 92.6868,115.827 91.029,115.827 91.029,116.542 92.8249,116.542 92.8249,116.779 90.6356,116.779 90.6356,114.695 92.754,114.695 ' style='fill:#1f1a17;fill-rule:evenodd' transform='matrix(15.313361,0,0,15.313361,-1261.7633,-1515.8943)'/><polygon id='_11983328' class='fil4' points='98.3851,116.542 99.8881,116.542 99.8881,116.779 97.9915,116.779 97.9915,114.695 98.3851,114.695 98.3851,116.542 ' style='fill:#1f1a17;fill-rule:evenodd' transform='matrix(15.313361,0,0,15.313361,-1261.7633,-1515.8943)'/><polygon id='_88564536' class='fil4' points='107.085,114.695 107.085,114.932 105.36,114.932 105.36,115.59 107.018,115.59 107.018,115.827 105.36,115.827 105.36,116.542 107.156,116.542 107.156,116.779 104.966,116.779 104.966,114.695 107.085,114.695 ' style='fill:#1f1a17;fill-rule:evenodd' transform='matrix(15.313361,0,0,15.313361,-1261.7633,-1515.8943)'/><polygon id='_12021272' class='fil4' points='114.688,114.695 113.616,116.779 113.193,116.779 112.113,114.695 112.532,114.695 113.415,116.459 114.269,114.695 114.688,114.695 ' style='fill:#1f1a17;fill-rule:evenodd' transform='matrix(15.313361,0,0,15.313361,-1261.7633,-1515.8943)'/><polygon id='_88564512' class='fil4' points='120.198,114.695 120.198,116.779 119.804,116.779 119.804,114.695 120.198,114.695 ' style='fill:#1f1a17;fill-rule:evenodd' transform='matrix(15.313361,0,0,15.313361,-1261.7633,-1515.8943)'/><path id='_88564704' class='fil4' d='M 683.0336,244.63685 C 679.89436,243.3689 677.64789,243.41331 675.27892,243.41331 C 664.50597,243.41331 662.58567,250.19713 667.96679,252.20777 C 669.63441,252.86472 671.94504,253.39456 675.0829,253.78505 C 678.92962,254.48181 682.77465,255.2291 686.62612,255.93198 C 690.66272,256.89213 694.3808,259.95787 694.57069,263.06495 C 695.02687,269.45215 686.24175,273.60973 676.17475,273.39381 C 670.01878,273.25599 665.40318,272.7338 661.23503,269.36793 C 658.09579,266.78303 657.97022,264.76779 657.83853,262.27325 L 663.41412,262.27325 C 663.35119,264.15526 664.37887,268.57776 672.45513,269.5425 C 673.86396,269.71248 676.23891,269.84877 678.61263,269.71248 C 681.04424,269.54097 683.54507,269.14741 685.21269,268.18114 C 688.22636,266.42929 690.53562,262.75715 684.95849,260.13091 C 682.20209,259.16617 678.35384,258.55823 675.20985,258.07279 C 668.86874,257.06517 671.94504,257.59501 665.66059,256.1479 C 663.6086,255.66247 660.01609,254.26589 659.44031,250.28135 C 658.67158,245.11463 663.79849,239.95555 675.14722,239.95555 C 679.06285,239.95555 683.67217,240.43793 686.49442,241.61859 C 692.84334,244.28617 693.22617,248.35646 693.03629,249.80051 L 687.20343,249.79898 C 687.329,247.9185 686.55705,246.12378 683.0336,244.63685 L 683.0336,244.63685 z' style='fill:#1f1a17;fill-rule:evenodd'/><polygon id='_88564776' class='fil4' points='133.364,114.695 133.364,116.779 132.971,116.779 132.971,114.695 133.364,114.695 ' style='fill:#1f1a17;fill-rule:evenodd' transform='matrix(15.313361,0,0,15.313361,-1261.7633,-1515.8943)'/><path id='_88564872' class='fil4' d='M 903.95931,256.67315 C 904.02362,261.17681 901.78022,266.56405 895.75594,270.1045 C 893.50947,271.41685 887.86956,273.34787 881.3966,273.39075 C 874.91905,273.34787 869.27776,271.41685 867.03114,270.1045 C 861.00548,266.56405 858.76361,261.17834 858.82639,256.67315 C 858.88918,252.16183 861.00548,246.78072 867.03114,243.23414 C 869.27914,241.92026 874.91752,239.99537 881.3966,239.95249 C 887.86956,239.99384 893.50947,241.92179 895.75594,243.23414 C 901.78022,246.77919 903.89652,252.16183 903.95931,256.67315 z M 864.91483,256.67315 C 864.78773,260.56581 866.90266,264.41712 870.04787,266.64827 C 872.93459,268.70639 877.2283,269.70941 881.3966,269.70941 C 885.55877,269.70941 889.85723,268.70639 892.73768,266.64827 C 895.88457,264.41712 897.99782,260.56581 897.86612,256.67315 C 897.99935,252.77437 895.88304,248.92306 892.73768,246.6919 C 889.85876,244.63379 885.55724,243.62617 881.3966,243.62617 C 877.22984,243.62617 872.93291,244.63379 870.04787,246.6919 C 866.90419,248.92153 864.7862,252.77437 864.91483,256.67315 z' style='fill:#1f1a17;fill-rule:evenodd'/><polygon id='_12020984' class='fil4' points='146.894,115.11 146.894,116.779 146.501,116.779 146.501,114.695 146.966,114.695 148.494,116.381 148.494,114.695 148.887,114.695 148.887,116.779 148.439,116.779 146.894,115.11 ' style='fill:#1f1a17;fill-rule:evenodd' transform='matrix(15.313361,0,0,15.313361,-1261.7633,-1515.8943)'/></g><g id='g3213'><rect transform='matrix(5.0571804,0,0,4.9141382,-570.94352,-377.13714)' width='48.855' height='25.124001' x='188.51601' y='85.525002' style='fill:#ffffff' clip-path='url(#XMLID_36_)' id='rect50'/><rect transform='matrix(5.0571804,0,0,4.9141382,-570.94352,-377.13714)' width='48.560001' height='29.362' x='257.13501' y='83.824997' style='fill:#ffffff' clip-path='url(#XMLID_36_)' id='rect52'/><path transform='matrix(5.0571804,0,0,4.9141382,-570.94352,-377.13714)' d='M 302.993,104.059 L 279.595,104.059 L 279.595,87.768 L 261.181,87.768 L 261.181,109.337 L 302.993,109.337 L 302.993,104.059 M 249.861,78.613 L 314.138,78.613 L 314.138,118.491 L 249.861,118.491 L 249.861,78.613 z' style='fill:#2056ae;fill-opacity:1;fill-rule:evenodd' clip-path='url(#XMLID_36_)' id='path54'/><path transform='matrix(5.0571804,0,0,4.9141382,-570.94352,-377.13714)' d='M 222.414,92.979 L 234.437,92.979 L 234.437,87.8 L 193.148,87.8 L 193.148,92.979 L 205.406,92.979 L 205.406,109.303 L 222.414,109.303 L 222.414,92.979 M 182.183,78.613 L 246.107,78.613 L 246.107,118.491 L 182.183,118.491 L 182.183,78.613 z' style='fill:#f9a70c;fill-opacity:1;fill-rule:evenodd' clip-path='url(#XMLID_36_)' id='path56'/><rect transform='matrix(5.0571804,0,0,4.9141382,-570.94352,-377.13714)' width='55.306' height='27.951' x='118.256' y='84.671997' style='fill:#ffffff;stroke:none;stroke-width:10.87584019;stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1' clip-path='url(#XMLID_36_)' id='rect48'/><path transform='matrix(5.0571804,0,0,4.9141382,-570.94352,-377.13714)' d='M 158.782,87.784 L 124.471,87.784 L 124.471,109.254 L 140.659,109.254 L 140.659,102.2 L 143.826,102.2 L 152.097,109.255 L 169.397,109.255 L 158.782,101.812 C 162.533,101.911 165.703,98.591 165.642,94.747 C 165.585,90.929 162.477,87.691 158.782,87.784 M 114.384,78.613 L 178.371,78.613 L 178.371,118.491 L 114.384,118.491 L 114.384,78.613 L 114.384,78.613 z M 140.659,92.865 L 148.635,92.865 C 150.571,93.554 150.689,96.463 148.87,97.338 L 140.659,97.36 L 140.659,92.865 z' style='fill:#ee2233;fill-opacity:1;fill-rule:evenodd' clip-path='url(#XMLID_36_)' id='path58'/></g></g></g></svg>"
        
        
        self.html = self.html.replace("ProSieben |",proSieben)
        self.html = self.html.replace("SAT.1 |",satEins)
        self.html = self.html.replace("RTL |",rtl)
        self.html = self.html.replace("kabel eins |",kabelEins)
        self.html = self.html.replace("VOX |",vox)
        
        
        
        
        
        
