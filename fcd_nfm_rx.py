#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: FCD FM Receiver
# Author: OZ9AEC
# Description: Simple FM receiver using the Funcube Dongle
# Generated: Fri Aug 12 08:35:51 2016
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from PyQt4.QtCore import QObject, pyqtSlot
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fcd
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import sip
import sys

from distutils.version import StrictVersion
class fcd_nfm_rx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "FCD FM Receiver")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("FCD FM Receiver")
        try:
             self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
             pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "fcd_nfm_rx")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 96000
        self.offset_fine = offset_fine = 0
        self.offset_coarse = offset_coarse = 0
        self.freq = freq = 144.47e6
        self.xlate_filter_taps = xlate_filter_taps = firdes.low_pass(1, samp_rate, 48000, 5000, firdes.WIN_HAMMING, 6.76)
        self.width = width = 10000
        self.trans = trans = 1500
        self.sql_lev = sql_lev = -100
        self.rx_freq = rx_freq = freq+(offset_coarse+offset_fine)
        self.rf_gain = rf_gain = 20
        self.display_selector = display_selector = 0
        self.af_gain = af_gain = 1

        ##################################################
        # Blocks
        ##################################################
        self._width_range = Range(2000, 40000, 100, 10000, 200)
        self._width_win = RangeWidget(self._width_range, self.set_width, "Filter", "counter")
        self.top_grid_layout.addWidget(self._width_win, 7,0,1,1)
        self._trans_range = Range(500, 5000, 1, 1500, 200)
        self._trans_win = RangeWidget(self._trans_range, self.set_trans, "Trans", "counter")
        self.top_grid_layout.addWidget(self._trans_win, 8,0,1,1)
        self._sql_lev_range = Range(-100, 0, 1, -100, 200)
        self._sql_lev_win = RangeWidget(self._sql_lev_range, self.set_sql_lev, "SQL", "counter")
        self.top_grid_layout.addWidget(self._sql_lev_win, 7,2,1,1)
        self._rx_freq_tool_bar = Qt.QToolBar(self)
        
        if None:
          self._rx_freq_formatter = None
        else:
          self._rx_freq_formatter = lambda x: x
        
        self._rx_freq_tool_bar.addWidget(Qt.QLabel("Receive"+": "))
        self._rx_freq_label = Qt.QLabel(str(self._rx_freq_formatter(self.rx_freq)))
        self._rx_freq_tool_bar.addWidget(self._rx_freq_label)
        self.top_grid_layout.addWidget(self._rx_freq_tool_bar, 4,3,1,1)
          
        self._offset_fine_range = Range(-1000, 1000, 1, 0, 200)
        self._offset_fine_win = RangeWidget(self._offset_fine_range, self.set_offset_fine, "Fine Tune", "counter")
        self.top_grid_layout.addWidget(self._offset_fine_win, 6,0,1,2)
        self._offset_coarse_range = Range(-48000, 48000, 100, 0, 200)
        self._offset_coarse_win = RangeWidget(self._offset_coarse_range, self.set_offset_coarse, "Coarse Tune", "counter")
        self.top_grid_layout.addWidget(self._offset_coarse_win, 6,2,1,2)
        self._freq_tool_bar = Qt.QToolBar(self)
        self._freq_tool_bar.addWidget(Qt.QLabel("FCD Freq"+": "))
        self._freq_line_edit = Qt.QLineEdit(str(self.freq))
        self._freq_tool_bar.addWidget(self._freq_line_edit)
        self._freq_line_edit.returnPressed.connect(
        	lambda: self.set_freq(eng_notation.str_to_num(str(self._freq_line_edit.text().toAscii()))))
        self.top_grid_layout.addWidget(self._freq_tool_bar, 5,1,1,1)
        self._display_selector_options = [0,1]
        self._display_selector_labels = ['Baseband','RF']
        self._display_selector_tool_bar = Qt.QToolBar(self)
        self._display_selector_tool_bar.addWidget(Qt.QLabel("Spectrum"+": "))
        self._display_selector_combo_box = Qt.QComboBox()
        self._display_selector_tool_bar.addWidget(self._display_selector_combo_box)
        for label in self._display_selector_labels: self._display_selector_combo_box.addItem(label)
        self._display_selector_callback = lambda i: Qt.QMetaObject.invokeMethod(self._display_selector_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._display_selector_options.index(i)))
        self._display_selector_callback(self.display_selector)
        self._display_selector_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_display_selector(self._display_selector_options[i]))
        self.top_grid_layout.addWidget(self._display_selector_tool_bar, 5,0,1,1)
        self._af_gain_range = Range(0, 5, 0.1, 1, 200)
        self._af_gain_win = RangeWidget(self._af_gain_range, self.set_af_gain, "VOL", "counter")
        self.top_grid_layout.addWidget(self._af_gain_win, 8,1,1,1)
        self._rf_gain_range = Range(-5, 30, 1, 20, 200)
        self._rf_gain_win = RangeWidget(self._rf_gain_range, self.set_rf_gain, "RF", "counter")
        self.top_grid_layout.addWidget(self._rf_gain_win, 7,1,1,1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	512, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	rx_freq*display_selector, #fc
        	samp_rate, #bw
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.05)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_freq_sink_x_0.disable_legend()
        
        if complex == type(float()):
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 0,0,5,4)
        self.low_pass_filter = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, width/2, trans, firdes.WIN_HAMMING, 6.76))
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(1, (xlate_filter_taps), -(offset_coarse+offset_fine), samp_rate)
        self.fcd_source_c_1 = fcd.source_c("hw:0")
        self.fcd_source_c_1.set_freq(freq)
            
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vff((af_gain, ))
        self.audio_sink = audio.sink(48000, "", True)
        self.analog_simple_squelch_cc_0 = analog.simple_squelch_cc(sql_lev, 1)
        self.analog_nbfm_rx_0 = analog.nbfm_rx(
        	audio_rate=48000,
        	quad_rate=96000,
        	tau=75e-6,
        	max_dev=5e3,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_nbfm_rx_0, 0), (self.blocks_multiply_const_vxx_1, 0))    
        self.connect((self.analog_simple_squelch_cc_0, 0), (self.analog_nbfm_rx_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.audio_sink, 1))    
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.audio_sink, 0))    
        self.connect((self.fcd_source_c_1, 0), (self.freq_xlating_fir_filter_xxx_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.low_pass_filter, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.qtgui_freq_sink_x_0, 0))    
        self.connect((self.low_pass_filter, 0), (self.analog_simple_squelch_cc_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "fcd_nfm_rx")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_xlate_filter_taps(firdes.low_pass(1, self.samp_rate, 48000, 5000, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter.set_taps(firdes.low_pass(1, self.samp_rate, self.width/2, self.trans, firdes.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_0.set_frequency_range(self.rx_freq*self.display_selector, self.samp_rate)

    def get_offset_fine(self):
        return self.offset_fine

    def set_offset_fine(self, offset_fine):
        self.offset_fine = offset_fine
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(-(self.offset_coarse+self.offset_fine))
        self.set_rx_freq(self._rx_freq_formatter(self.freq+(self.offset_coarse+self.offset_fine)))

    def get_offset_coarse(self):
        return self.offset_coarse

    def set_offset_coarse(self, offset_coarse):
        self.offset_coarse = offset_coarse
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(-(self.offset_coarse+self.offset_fine))
        self.set_rx_freq(self._rx_freq_formatter(self.freq+(self.offset_coarse+self.offset_fine)))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.fcd_source_c_1.set_freq(self.freq)
        Qt.QMetaObject.invokeMethod(self._freq_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.freq)))
        self.set_rx_freq(self._rx_freq_formatter(self.freq+(self.offset_coarse+self.offset_fine)))

    def get_xlate_filter_taps(self):
        return self.xlate_filter_taps

    def set_xlate_filter_taps(self, xlate_filter_taps):
        self.xlate_filter_taps = xlate_filter_taps
        self.freq_xlating_fir_filter_xxx_0.set_taps((self.xlate_filter_taps))

    def get_width(self):
        return self.width

    def set_width(self, width):
        self.width = width
        self.low_pass_filter.set_taps(firdes.low_pass(1, self.samp_rate, self.width/2, self.trans, firdes.WIN_HAMMING, 6.76))

    def get_trans(self):
        return self.trans

    def set_trans(self, trans):
        self.trans = trans
        self.low_pass_filter.set_taps(firdes.low_pass(1, self.samp_rate, self.width/2, self.trans, firdes.WIN_HAMMING, 6.76))

    def get_sql_lev(self):
        return self.sql_lev

    def set_sql_lev(self, sql_lev):
        self.sql_lev = sql_lev
        self.analog_simple_squelch_cc_0.set_threshold(self.sql_lev)

    def get_rx_freq(self):
        return self.rx_freq

    def set_rx_freq(self, rx_freq):
        self.rx_freq = rx_freq
        self.qtgui_freq_sink_x_0.set_frequency_range(self.rx_freq*self.display_selector, self.samp_rate)
        Qt.QMetaObject.invokeMethod(self._rx_freq_label, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.rx_freq)))

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self.fcd_source_c_1.set_lna_gain(self.rf_gain)

    def get_display_selector(self):
        return self.display_selector

    def set_display_selector(self, display_selector):
        self.display_selector = display_selector
        self.qtgui_freq_sink_x_0.set_frequency_range(self.rx_freq*self.display_selector, self.samp_rate)
        self._display_selector_callback(self.display_selector)

    def get_af_gain(self):
        return self.af_gain

    def set_af_gain(self, af_gain):
        self.af_gain = af_gain
        self.blocks_multiply_const_vxx_1.set_k((self.af_gain, ))


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    if(StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0")):
        Qt.QApplication.setGraphicsSystem(gr.prefs().get_string('qtgui','style','raster'))
    qapp = Qt.QApplication(sys.argv)
    tb = fcd_nfm_rx()
    tb.start()
    tb.show()
    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()
    tb = None #to clean up Qt widgets
