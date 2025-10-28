from PyQt5.QtWidgets import*
from PyQt5.QtCore import*
from PyQt5.QtGui import*
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT  as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np

import system
import image_processing
import file_actions

class MainUİ(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MGAA Medikal Görüntü Analiz Aracı')

        self.current_medical_file = None
        self.current_medical_file_shape = None
        self.current_list_item_image_path = None
        self.current_selected = None
        self.current_selected_name = None
        self.list_item_f = None
        
        #layout-side#
        self.main_layout = QHBoxLayout()

        #widget-side#
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)

        #taskbar-side#
        self.menubar_main = self.menuBar()
        self.file_system_menu = self.menubar_main.addMenu('Dosya sistemim')
        self.file_sys_menu_open = self.file_system_menu.addAction('Aç')
        self.file_sys_menu_close = self.file_system_menu.addAction('Kapat')

        self.medical_image_list_menu = self.menubar_main.addMenu('Medikal görüntülerim')
        self.med_img_lst_menu_open = self.medical_image_list_menu.addAction('Aç')
        self.med_img_lst_menu_close = self.medical_image_list_menu.addAction('Kapat')
        
        self.file_system_menu.setIcon(QIcon(r'icons\folder.png'))
        self.file_system_menu.setWindowIcon(QIcon(r'icons\folder.png'))

        self.medical_image_list_menu.setIcon(QIcon(r'icons\pharmacy.png'))
        self.medical_image_list_menu.setWindowIcon(QIcon(r'icons\pharmacy.png'))

        #splitter-side#
        self.mri_list_splitter = QSplitter(Qt.Vertical)
        self.mri_monitor_image_settings_splitter = QSplitter(Qt.Vertical)
        self.mri_monitor_splitter = QSplitter(Qt.Vertical)
        self.mri_monitor_view_settings_splitter = QSplitter(Qt.Vertical)
        self.mri_monitor_view_settings_splitter_container = QSplitter(Qt.Horizontal)
        self.monitor_splitter_container = QSplitter(Qt.Horizontal)
        self.file_system_splitter = QSplitter(Qt.Vertical)
        self.image_selecter_splitter = QSplitter(Qt.Vertical)

        self.depth_splitter = QSplitter(Qt.Vertical)
        self.threshold_splitter = QSplitter(Qt.Vertical)
        self.sobel_splitter = QSplitter(Qt.Vertical)
        self.gauss_splitter = QSplitter(Qt.Vertical)
        self.median_splitter = QSplitter(Qt.Vertical)
        self.blur_splitter = QSplitter(Qt.Vertical)
        self.edege_splitter = QSplitter(Qt.Vertical)

        self.select_threshold_splitter = QSplitter(Qt.Horizontal)
        
        #program-widget-side#
        self.mri_list = QListWidget()

        self.show_mri_image_button = QPushButton('Monitöre aktar')
        self.add_mri_image_button = QPushButton('Ekle')
        self.save_mri_image_button = QPushButton('Kaydet')
        self.delete_mri_image_button = QPushButton('Sil')

        self.tumor_detection_checkbox = QCheckBox()
        self.bright_dimmer_checkbox = QCheckBox()
        self.normal_setting_checkbox = QCheckBox()
        self.checbox_apply_button = QPushButton(text='Uygula')
        self.checbox_reset_button = QPushButton(text='Sıfırla')

        self.return_preverius_matrix = QPushButton(text='İşlemi geri al')
        self.update_matrix_object = QPushButton(text='İşlemi kaydet')

        self.tumor_detection_checkbox.setText('Tümör Tespiti')
        self.bright_dimmer_checkbox.setText('Görüntüyü Parlat')
        self.normal_setting_checkbox.setText('Normal Şekilde Göster')

        self.depth_label = QLabel(text='Slice')
        self.threshold_label = QLabel(text='Eşik')
        self.edge_label = QLabel(text='Kenarlar')
        self.sobel_label = QLabel(text='Kenar Netliği')
        self.gaussian_label = QLabel(text='Gaussiyen')
        self.median_label = QLabel(text='Medyan')
        self.blur_label = QLabel(text='Blur')

        self.depth_slider = QSlider(Qt.Horizontal)

        self.threshold_bins_slider = QSlider(Qt.Horizontal)
        self.threshold_maxval_slider = QSlider(Qt.Horizontal)

        self.edge_thres1_slider = QSlider(Qt.Horizontal)
        self.edge_thres2_slider = QSlider(Qt.Horizontal)

        self.sobel_button = QPushButton(text='Kenarları netleştir')
        self.sobel_to_normal_button = QPushButton(text='Eski görsele dön')

        self.gaussian_x_slider = QSlider(Qt.Horizontal)
        self.gaussian_y_slider = QSlider(Qt.Horizontal)
        self.gaussian_z_slider = QSlider(Qt.Horizontal)

        self.median_slider = QSlider(Qt.Horizontal)

        self.blur_slider = QSlider(Qt.Horizontal)

        self.figure_object_mrı_monitor,self.axes_object_mrı_monitor = plt.subplots(nrows=1,ncols=3,figsize=(14,4),facecolor='gray')

        self.fig_canvas_t1 = FigureCanvas(figure=self.figure_object_mrı_monitor)
        self.custom_toolbar = NavigationToolbar(canvas=self.fig_canvas_t1)

        self.file_path = QLineEdit()
        self.folder_path = QLineEdit()
        self.file_path.setAlignment(Qt.AlignCenter)
        self.folder_path.setAlignment(Qt.AlignCenter)
        self.file_path.setPlaceholderText('Dosya yolu')
        self.folder_path.setPlaceholderText('Klasör yolu')

        self.file_system_model = QFileSystemModel()
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.file_system_model)

        self.define_file_button = QPushButton(text='MRI dosyasını tanımla')
        self.define_folder_button = QPushButton(text='Klasör Tanımla')
        self.reset_path_button = QPushButton(text='Sıfırla')

        self.mrı_select_information = QLabel(text='İşlem yapılacak MRI görüntüleme türünü Seç')
        self.t1_checkbox = QCheckBox()
        self.t2_checkbox = QCheckBox()
        self.flair_checkbox = QCheckBox()

        self.threshold_binary_checkbox = QCheckBox()
        self.threshold_otsu_checkbox = QCheckBox()
        self.threshold_tozero_checkbox = QCheckBox()
        self.threshold_tozero_ınv_checkbox = QCheckBox()
        self.threshold_trunc_checkbox = QCheckBox()
        self.threshold_binary_inv_checkbox = QCheckBox()

        self.threshold_binary_checkbox.setText('İkili eşikleme')
        self.threshold_binary_inv_checkbox.setText('Ters ikili eşikleme')
        self.threshold_trunc_checkbox.setText('Sınırlı eşikleme')
        self.threshold_tozero_checkbox.setText('Sıfıra eşikleme')
        self.threshold_tozero_ınv_checkbox.setText('Ters sıfıra eşikleme')


        self.defined_fig,self.defined_ax = plt.subplots(nrows=1,ncols=1,figsize=(5,4),facecolor='gray')
        self.defined_ax.axis('off')
        self.defined_figurecanvas_object = FigureCanvas(self.defined_fig)
        self.defined_figurecanvas_object.setStyleSheet('border:1 px solid gray')

        self.add_to_list_button = QPushButton(text='Görüntüyü listeye ekle')
        self.delete_image_button = QPushButton(text='Görüntüyü Sil')

        try:
            self.axes_like = self.defined_ax.imshow(image_processing.to_matrix('t1.png'))
        except:
            self.axes_like = self.defined_ax.imshow([[0]*40,[1]*40,[0]*40])

        
        self.t1_checkbox.setText('T1 MRI')
        self.t2_checkbox.setText('T2 MRI')
        self.flair_checkbox.setText('Flair MRI')

        #widget-parent-settings#
        item = QListWidgetItem('MRI Görüntüleri burada gözükecektir..')
        item.setTextAlignment(Qt.AlignCenter)
        self.mri_list.addItem(item)
        self.mri_list.setIconSize(QSize(64,64))

        self.main_layout.addWidget(self.monitor_splitter_container)

        self.depth_splitter.addWidget(self.depth_label)
        self.depth_splitter.addWidget(self.depth_slider)

        self.threshold_splitter.addWidget(self.threshold_label)
        self.threshold_splitter.addWidget(self.threshold_bins_slider)
        self.threshold_splitter.addWidget(self.threshold_maxval_slider)

        self.sobel_splitter.addWidget(self.sobel_label)
        self.sobel_splitter.addWidget(self.sobel_button)
        self.sobel_splitter.addWidget(self.sobel_to_normal_button)

        self.gauss_splitter.addWidget(self.gaussian_label)
        self.gauss_splitter.addWidget(self.gaussian_x_slider)
        self.gauss_splitter.addWidget(self.gaussian_y_slider)
        self.gauss_splitter.addWidget(self.gaussian_z_slider)

        self.median_splitter.addWidget(self.median_label)
        self.median_splitter.addWidget(self.median_slider)

        self.blur_splitter.addWidget(self.blur_label)
        self.blur_splitter.addWidget(self.blur_slider)

        self.monitor_splitter_container.addWidget(self.mri_list_splitter)
        self.monitor_splitter_container.addWidget(self.mri_monitor_image_settings_splitter)
        self.monitor_splitter_container.addWidget(self.mri_monitor_splitter)    
        self.monitor_splitter_container.addWidget(self.image_selecter_splitter)
        self.monitor_splitter_container.addWidget(self.file_system_splitter)    

        self.mri_list_splitter.addWidget(self.mri_list)
        self.mri_list_splitter.addWidget(self.show_mri_image_button)
        #self.mri_list_splitter.addWidget(self.add_mri_image_button)
        self.mri_list_splitter.addWidget(self.delete_mri_image_button)
        self.mri_list_splitter.addWidget(self.save_mri_image_button)

        self.mri_monitor_image_settings_splitter.addWidget(QLabel(text='Mrı Görüntüsünün işlenme türünü seç'))
        self.mri_monitor_image_settings_splitter.addWidget(self.tumor_detection_checkbox)
        self.mri_monitor_image_settings_splitter.addWidget(self.bright_dimmer_checkbox)
        self.mri_monitor_image_settings_splitter.addWidget(self.normal_setting_checkbox)
        for contf_ in [QLabel(),QLabel(),QLabel(),QLabel(),QLabel(),QLabel(),QLabel(),QLabel(),QLabel(),QLabel(),QLabel(),QLabel(),QLabel(),QLabel(),QLabel()]:
            contf_.setStyleSheet('border: none')
            self.mri_monitor_image_settings_splitter.addWidget(contf_)
        self.mri_monitor_image_settings_splitter.addWidget(self.checbox_apply_button)
        self.mri_monitor_image_settings_splitter.addWidget(self.checbox_reset_button)

        self.mri_monitor_view_settings_splitter_container.addWidget(self.gauss_splitter)
        self.mri_monitor_view_settings_splitter_container.addWidget(self.threshold_splitter)
        self.mri_monitor_view_settings_splitter_container.addWidget(self.edege_splitter)
        self.mri_monitor_view_settings_splitter_container.addWidget(self.depth_splitter)
        self.mri_monitor_view_settings_splitter_container.addWidget(self.median_splitter)
        self.mri_monitor_view_settings_splitter_container.addWidget(self.blur_splitter)
        self.mri_monitor_view_settings_splitter_container.addWidget(self.sobel_splitter)

        #self.file_system_splitter.addWidget(self.file_path)
        self.file_system_splitter.addWidget(self.folder_path)
        self.file_system_splitter.addWidget(self.tree_view)
        self.file_system_splitter.addWidget(self.define_folder_button)
        self.file_system_splitter.addWidget(self.define_file_button)
        self.file_system_splitter.addWidget(self.reset_path_button)
        
        self.mri_monitor_splitter.addWidget(self.select_threshold_splitter)
        self.mri_monitor_splitter.addWidget(self.custom_toolbar)
        self.mri_monitor_splitter.addWidget(self.fig_canvas_t1)
        self.mri_monitor_splitter.addWidget(self.return_preverius_matrix)
        self.mri_monitor_splitter.addWidget(self.update_matrix_object)
        self.mri_monitor_splitter.addWidget(self.mri_monitor_view_settings_splitter_container)

        self.image_selecter_splitter.addWidget(self.mrı_select_information)
        self.image_selecter_splitter.addWidget(self.t1_checkbox)
        self.image_selecter_splitter.addWidget(self.t2_checkbox)
        self.image_selecter_splitter.addWidget(self.flair_checkbox)

        self.select_threshold_splitter.addWidget(self.threshold_binary_checkbox)
        self.select_threshold_splitter.addWidget(self.threshold_binary_inv_checkbox)
        self.select_threshold_splitter.addWidget(self.threshold_tozero_checkbox)
        self.select_threshold_splitter.addWidget(self.threshold_tozero_ınv_checkbox)
        self.select_threshold_splitter.addWidget(self.threshold_trunc_checkbox)
        self.select_threshold_splitter.addWidget(self.threshold_otsu_checkbox)

        self.cont_container = [QLabel(),QLabel(text='Tanımlanan görüntü')]

        for cont in range(len(self.cont_container)):
            self.cont_container[cont].setStyleSheet('border:none')
            self.cont_container[cont].setAlignment(Qt.AlignCenter)
            self.image_selecter_splitter.addWidget(self.cont_container[cont])
        self.image_selecter_splitter.addWidget(self.defined_figurecanvas_object)
        self.image_selecter_splitter.addWidget(self.add_to_list_button)
        self.image_selecter_splitter.addWidget(self.delete_image_button)

        for a in range(len(self.axes_object_mrı_monitor)):
            self.axes_object_mrı_monitor[a].axis('off')
        
        try:
            self.axes_object_mrı_monitor[0].imshow(image_processing.to_matrix('t1.png'))
            self.axes_object_mrı_monitor[1].imshow(image_processing.to_matrix('t2.png'))
            self.axes_object_mrı_monitor[2].imshow(image_processing.to_matrix('tumor.jpg'))

        except:
            pass
        self.axes_object_mrı_monitor[0].set_title('T1-MRI',color='white')
        self.axes_object_mrı_monitor[1].set_title('T2-MRI',color='white')
        self.axes_object_mrı_monitor[2].set_title('Flair-MRI',color='white')

        #timers-side#
        self.optimize_w_timer = QTimer(self)
        #self.optimize_w_timer.start(10)
        self.optimize_w_timer.timeout.connect(self.optimize_widget_sizes)

        #signal-slot-side#
        self.define_folder_button.clicked.connect(self.define_folder)
        self.define_file_button.clicked.connect(self.define_file)
        self.add_to_list_button.clicked.connect(self.list_item_igniter)
        self.delete_mri_image_button.clicked.connect(self.delete_list_item_function)
        self.show_mri_image_button.clicked.connect(self.monitor_image_export_igniter)
        self.checbox_apply_button.clicked.connect(self.other_actions_igniter)

        
        #signal-slot-matrix-actions-side#
        self.update_matrix_object.clicked.connect(self.get_current_matrix)
        self.return_preverius_matrix.clicked.connect(self.remove_image_from_axes)

        #signal-slot-slider-side#
        self.threshold_bins_slider.valueChanged.connect(self.threshold_igniter)
        self.threshold_maxval_slider.valueChanged.connect(self.threshold_igniter)

        self.gaussian_x_slider.valueChanged.connect(self.gaussian_igniter)
        self.gaussian_y_slider.valueChanged.connect(self.gaussian_igniter)
        self.gaussian_z_slider.valueChanged.connect(self.gaussian_igniter)

        self.median_slider.valueChanged.connect(self.median_igniter)

        self.sobel_button.clicked.connect(self.sobel_igniter)
        self.sobel_to_normal_button.clicked.connect(self.sobel_to_normal_matrix)

        self.file_sys_menu_open.triggered.connect(self.show_file_system)
        self.file_sys_menu_close.triggered.connect(self.hide_file_system)

        self.med_img_lst_menu_open.triggered.connect(self.show_image_settings)
        self.med_img_lst_menu_close.triggered.connect(self.hide_image_settings)

        self.depth_slider.valueChanged.connect(self.depth_slider_function)

        #css-define-side#
        self.css_qss_file = open(r'program_css.qss','r').read()
        self.setStyleSheet(str(self.css_qss_file))

        self.setCentralWidget(self.main_widget)

        attention_text = 'Bu program tıbbi bir programdır. Doğrudan teşhis koyamaz, yanlızca önerililerde bulunabilir. Programı kullanarak bunları kabul etmiş varsayılırsınız.'

        self.msgbox = QMessageBox.question(self,'Dikkat',attention_text,QMessageBox.Ok | QMessageBox.Cancel)
        if self.msgbox != QMessageBox.Cancel:
            self.swap_gui()
        
        else:
            pass

    def get_current_matrix(self):
        if self.t1_checkbox.isChecked() == True:
            self.axes_like = self.axes_object_mrı_monitor[0].get_images().pop()
            print(self.axes_like)

        if self.t2_checkbox.isChecked() == True:
            self.axes_like = self.axes_object_mrı_monitor[1].get_images().pop()
            print(self.axes_like)
            
        if self.flair_checkbox.isChecked() == True:
            self.axes_like = self.axes_object_mrı_monitor[2].get_images().pop()
            print(self.axes_like)   
    
    def depth_slider_function(self):
        if self.t1_checkbox.isChecked() == True:
            h,w,d = self.current_medical_file_shape

            current_slice = image_processing.mrı_slice_returner(self.current_medical_file,h,w,d)

            print(current_slice)

    def swap_gui(self):

        #self.mri_monitor_splitter.setParent(None)
        #self.monitor_splitter_container.setParent(None)
        #self.mri_list_splitter.setParent(None)
        self.mri_monitor_image_settings_splitter.setParent(None)
        self.file_system_splitter.setParent(None)
        #self.image_selecter_splitter.setParent(None)
        #self.mri_monitor_view_settings_splitter.setParent(None)

        self.mri_monitor_image_settings_splitter.setStyleSheet(str(self.css_qss_file))
        self.file_system_splitter.setStyleSheet(str(self.css_qss_file))

        self.dock1 = QDockWidget()
        self.dock2 = QDockWidget()

        self.dock1.setParent(self)
        self.dock1.setWidget(self.file_system_splitter)
        self.dock1.setFixedWidth(500)

        self.dock2.setParent(self)
        self.dock2.setWidget(self.mri_monitor_image_settings_splitter)
        self.dock2.setFixedHeight(450)
        self.dock2.setFixedWidth(300)

        self.dock1.hide()
        self.dock2.hide()
    
    def show_file_system(self):
        self.dock1.show()
    
    def hide_file_system(self):
        self.dock1.hide()
    
    def show_image_settings(self):
        self.dock2.show()
    
    def hide_image_settings(self):
        self.dock2.hide()
    
    

    def remove_image_from_axes(self):
        if self.t1_checkbox.isChecked() == True:
            self.axes_object_mrı_monitor[0].clear()
            self.axes_object_mrı_monitor[0].imshow([
                                                    [1,0,0,0,0,0,0,0,1],
                                                    [0,1,0,0,0,0,0,1,0],
                                                    [0,0,1,0,0,0,1,0,0],
                                                    [0,0,0,1,0,1,0,0,0],
                                                    [0,0,0,0,1,0,0,0,0],
                                                    [0,0,0,1,0,1,0,0,0],
                                                    [0,0,1,0,0,0,1,0,0],
                                                    [0,1,0,0,0,0,0,1,0],
                                                    [1,0,0,0,0,0,0,0,1]
                                                    ],cmap='gray')
            self.axes_like = self.axes_object_mrı_monitor[0].get_images()
            self.fig_canvas_t1.draw()
        
        if self.t2_checkbox.isChecked() == True:
            self.axes_object_mrı_monitor[1].clear()
            self.axes_object_mrı_monitor[1].imshow([
                                                    [1,0,0,0,0,0,0,0,1],
                                                    [0,1,0,0,0,0,0,1,0],
                                                    [0,0,1,0,0,0,1,0,0],
                                                    [0,0,0,1,0,1,0,0,0],
                                                    [0,0,0,0,1,0,0,0,0],
                                                    [0,0,0,1,0,1,0,0,0],
                                                    [0,0,1,0,0,0,1,0,0],
                                                    [0,1,0,0,0,0,0,1,0],
                                                    [1,0,0,0,0,0,0,0,1]
                                                    ],cmap='gray')
            self.axes_like = self.axes_object_mrı_monitor[1].get_images()
            self.fig_canvas_t1.draw()

        if self.flair_checkbox.isChecked() == True:
            self.axes_object_mrı_monitor[2].clear()
            self.axes_object_mrı_monitor[2].imshow([
                                                    [1,0,0,0,0,0,0,0,1],
                                                    [0,1,0,0,0,0,0,1,0],
                                                    [0,0,1,0,0,0,1,0,0],
                                                    [0,0,0,1,0,1,0,0,0],
                                                    [0,0,0,0,1,0,0,0,0],
                                                    [0,0,0,1,0,1,0,0,0],
                                                    [0,0,1,0,0,0,1,0,0],
                                                    [0,1,0,0,0,0,0,1,0],
                                                    [1,0,0,0,0,0,0,0,1]
                                                    ],cmap='gray')
            self.axes_like = self.axes_object_mrı_monitor[2].get_images()
            self.fig_canvas_t1.draw()
    
    def other_actions_igniter(self):
        #self.threshold_splitter.setEnabled(False)
        #self.threshold_splitter.setWindowOpacity(0.5)
        if self.tumor_detection_checkbox.isChecked() == True:
            self.matrix_a = self.axes_like.get_array()
            if self.t1_checkbox.isChecked() == True:
                self.tumor_detecetion_output = image_processing.tumor_detection_function(matrix=self.matrix_a)

                self.axes_object_mrı_monitor[0].imshow(self.tumor_detecetion_output,cmap='gray')
                self.fig_canvas_t1.draw()

    def median_igniter(self):
        self.ksizemv = self.median_slider.value()
        self.matrix = self.axes_like.get_array()
        if self.t1_checkbox.isChecked() == True:
            median_function = image_processing.median_function(self.matrix,self.ksizemv)

            if type(median_function) != str:
                self.axes_object_mrı_monitor[0].imshow(median_function)
                self.fig_canvas_t1.draw()
            
            else:
                pass

        if self.t2_checkbox.isChecked() == True:
            median_function = image_processing.median_function(self.matrix,self.ksizemv)

            if type(median_function) != str:
                self.axes_object_mrı_monitor[1].imshow(median_function,cmap='gray')
                self.fig_canvas_t1.draw()
            
            else:
                pass

        if self.flair_checkbox.isChecked() == True:
            median_function = image_processing.median_function(self.matrix,self.ksizemv)

            if type(median_function) != str:
                self.axes_object_mrı_monitor[2].imshow(median_function,cmap='gray')
                self.fig_canvas_t1.draw()
            
            else:
                pass

    def threshold_igniter(self):
        if self.t1_checkbox.isChecked() == True:
            if self.threshold_binary_checkbox.isChecked() == True:
                self.flag = 'binary'
                self.matrix = self.axes_like.get_array()
                self.thres = self.threshold_bins_slider.value()
                self.maxval = self.threshold_maxval_slider.value()

                threshold_matrix,normal_matrix = image_processing.threshold_function(self.matrix,self.thres,self.maxval,self.flag)

                self.axes_object_mrı_monitor[0].imshow(threshold_matrix,cmap='gray')
                self.fig_canvas_t1.draw()
            
            elif self.threshold_binary_inv_checkbox.isChecked() == True:
                self.flag = 'binary_inv'
                self.matrix = self.axes_like.get_array()
                self.thres = self.threshold_bins_slider.value()
                self.maxval = self.threshold_maxval_slider.value()

                threshold_matrix,normal_matrix = image_processing.threshold_function(self.matrix,self.thres,self.maxval,self.flag)

                self.axes_object_mrı_monitor[0].imshow(threshold_matrix,cmap='gray')
                self.fig_canvas_t1.draw()     

            elif self.threshold_trunc_checkbox.isChecked() == True:
                self.flag = 'threshold_trunc'
                self.matrix = self.axes_like.get_array()
                self.thres = self.threshold_bins_slider.value()
                self.maxval = self.threshold_maxval_slider.value()

                threshold_matrix,normal_matrix = image_processing.threshold_function(self.matrix,self.thres,self.maxval,self.flag)

                self.axes_object_mrı_monitor[0].imshow(threshold_matrix,cmap='gray')
                self.fig_canvas_t1.draw()    
            
            elif self.threshold_tozero_checkbox.isChecked() == True:
                self.flag = 'threshold_tozero'
                self.matrix = self.axes_like.get_array()
                self.thres = self.threshold_bins_slider.value()
                self.maxval = self.threshold_maxval_slider.value()

                threshold_matrix,normal_matrix = image_processing.threshold_function(self.matrix,self.thres,self.maxval,self.flag)

                self.axes_object_mrı_monitor[0].imshow(threshold_matrix,cmap='gray')
                self.fig_canvas_t1.draw()     

            elif self.threshold_tozero_ınv_checkbox.isChecked() == True:
                self.flag = 'threshold_tozero_inv'
                self.matrix = self.axes_like.get_array()
                self.thres = self.threshold_bins_slider.value()
                self.maxval = self.threshold_maxval_slider.value()

                threshold_matrix,normal_matrix = image_processing.threshold_function(self.matrix,self.thres,self.maxval,self.flag)

                self.axes_object_mrı_monitor[0].imshow(threshold_matrix,cmap='gray')
                self.fig_canvas_t1.draw()     

        elif self.t2_checkbox.isChecked() == True:
            if self.threshold_binary_checkbox.isChecked() == True:
                self.flag = 'binary'
                self.matrix = self.axes_like.get_array()
                self.thres = self.threshold_bins_slider.value()
                self.maxval = self.threshold_maxval_slider.value()

                threshold_matrix,normal_matrix = image_processing.threshold_function(self.matrix,self.thres,self.maxval,self.flag)

                self.axes_object_mrı_monitor[1].imshow(threshold_matrix,cmap='gray')
                self.fig_canvas_t1.draw()
            
            elif self.threshold_binary_inv_checkbox.isChecked() == True:
                self.flag = 'binary_inv'
                self.matrix = self.axes_like.get_array()
                self.thres = self.threshold_bins_slider.value()
                self.maxval = self.threshold_maxval_slider.value()

                threshold_matrix,normal_matrix = image_processing.threshold_function(self.matrix,self.thres,self.maxval,self.flag)

                self.axes_object_mrı_monitor[1].imshow(threshold_matrix,cmap='gray')
                self.fig_canvas_t1.draw()     

            elif self.threshold_trunc_checkbox.isChecked() == True:
                self.flag = 'threshold_trunc'
                self.matrix = self.axes_like.get_array()
                self.thres = self.threshold_bins_slider.value()
                self.maxval = self.threshold_maxval_slider.value()

                threshold_matrix,normal_matrix = image_processing.threshold_function(self.matrix,self.thres,self.maxval,self.flag)

                self.axes_object_mrı_monitor[1].imshow(threshold_matrix,cmap='gray')
                self.fig_canvas_t1.draw()    
            
            elif self.threshold_tozero_checkbox.isChecked() == True:
                self.flag = 'threshold_tozero'
                self.matrix = self.axes_like.get_array()
                self.thres = self.threshold_bins_slider.value()
                self.maxval = self.threshold_maxval_slider.value()

                threshold_matrix,normal_matrix = image_processing.threshold_function(self.matrix,self.thres,self.maxval,self.flag)

                self.axes_object_mrı_monitor[1].imshow(threshold_matrix,cmap='gray',alpha=0.5)
                self.fig_canvas_t1.draw()     

            elif self.threshold_tozero_ınv_checkbox.isChecked() == True:
                self.flag = 'threshold_tozero_inv'
                self.matrix = self.axes_like.get_array()
                self.thres = self.threshold_bins_slider.value()
                self.maxval = self.threshold_maxval_slider.value()

                threshold_matrix,normal_matrix = image_processing.threshold_function(self.matrix,self.thres,self.maxval,self.flag)

                self.axes_object_mrı_monitor[1].imshow(threshold_matrix,cmap='gray')
                self.fig_canvas_t1.draw()     

        elif self.flair_checkbox.isChecked() == True:
            if self.threshold_binary_checkbox.isChecked() == True:
                self.flag = 'binary'
                self.matrix = self.axes_like.get_array()
                self.thres = self.threshold_bins_slider.value()
                self.maxval = self.threshold_maxval_slider.value()

                threshold_matrix,normal_matrix = image_processing.threshold_function(self.matrix,self.thres,self.maxval,self.flag)

                self.axes_object_mrı_monitor[2].imshow(threshold_matrix,cmap='gray')
                self.fig_canvas_t1.draw()
            
            elif self.threshold_binary_inv_checkbox.isChecked() == True:
                self.flag = 'binary_inv'
                self.matrix = self.axes_like.get_array()
                self.thres = self.threshold_bins_slider.value()
                self.maxval = self.threshold_maxval_slider.value()

                threshold_matrix,normal_matrix = image_processing.threshold_function(self.matrix,self.thres,self.maxval,self.flag)

                self.axes_object_mrı_monitor[2].imshow(threshold_matrix,cmap='gray')
                self.fig_canvas_t1.draw()     

            elif self.threshold_trunc_checkbox.isChecked() == True:
                self.flag = 'threshold_trunc'
                self.matrix = self.axes_like.get_array()
                self.thres = self.threshold_bins_slider.value()
                self.maxval = self.threshold_maxval_slider.value()

                threshold_matrix,normal_matrix = image_processing.threshold_function(self.matrix,self.thres,self.maxval,self.flag)

                self.axes_object_mrı_monitor[2].imshow(threshold_matrix,cmap='gray')
                self.fig_canvas_t1.draw()    
            
            elif self.threshold_tozero_checkbox.isChecked() == True:
                self.flag = 'threshold_tozero'
                self.matrix = self.axes_like.get_array()
                self.thres = self.threshold_bins_slider.value()
                self.maxval = self.threshold_maxval_slider.value()

                threshold_matrix,normal_matrix = image_processing.threshold_function(self.matrix,self.thres,self.maxval,self.flag)

                self.axes_object_mrı_monitor[2].imshow(threshold_matrix,cmap='gray')
                self.fig_canvas_t1.draw()     

            elif self.threshold_tozero_ınv_checkbox.isChecked() == True:
                self.flag = 'threshold_tozero_inv'
                self.matrix = self.axes_like.get_array()
                self.thres = self.threshold_bins_slider.value()
                self.maxval = self.threshold_maxval_slider.value()

                threshold_matrix,normal_matrix = image_processing.threshold_function(self.matrix,self.thres,self.maxval,self.flag)

                self.axes_object_mrı_monitor[2].imshow(threshold_matrix,cmap='gray')
                self.fig_canvas_t1.draw()     

    def gaussian_igniter(self):
        if self.t1_checkbox.isChecked() == True:
            self.matrix = self.axes_like.get_array()
            self.ksize = (self.gaussian_x_slider.value(),self.gaussian_x_slider.value())
            self.sigmaX = self.gaussian_y_slider.value()
            self.sigmaY = self.gaussian_z_slider.value()

            self.gaussian_function_tuple_data = image_processing.gaussian_function(self.matrix,self.ksize,self.sigmaX,self.sigmaY)

            if self.gaussian_function_tuple_data:
                self.gaussian_matrixgv,self.normal_matrixgv = self.gaussian_function_tuple_data

                self.axes_object_mrı_monitor[0].imshow(self.gaussian_matrixgv,cmap='gray')
                self.fig_canvas_t1.draw()

            else:
                pass

        elif self.t2_checkbox.isChecked() == True:
            self.matrix = self.axes_like.get_array()
            self.ksize = (self.gaussian_x_slider.value(),self.gaussian_x_slider.value())
            self.sigmaX = self.gaussian_y_slider.value()
            self.sigmaY = self.gaussian_z_slider.value()

            self.gaussian_function_tuple_data = image_processing.gaussian_function(self.matrix,self.ksize,self.sigmaX,self.sigmaY)

            if self.gaussian_function_tuple_data:
                self.gaussian_matrixgv,self.normal_matrixgv = self.gaussian_function_tuple_data

                self.axes_object_mrı_monitor[1].imshow(self.gaussian_matrixgv,cmap='gray')
                self.fig_canvas_t1.draw()

            else:
                pass

        elif self.flair_checkbox.isChecked() == True:
            self.matrix = self.axes_like.get_array()
            self.ksize = (self.gaussian_x_slider.value(),self.gaussian_x_slider.value())
            self.sigmaX = self.gaussian_y_slider.value()
            self.sigmaY = self.gaussian_z_slider.value()

            self.gaussian_function_tuple_data = image_processing.gaussian_function(self.matrix,self.ksize,self.sigmaX,self.sigmaY)

            if self.gaussian_function_tuple_data:
                self.gaussian_matrixgv,self.normal_matrixgv = self.gaussian_function_tuple_data

                self.axes_object_mrı_monitor[2].imshow(self.gaussian_matrixgv,cmap='gray')
                self.fig_canvas_t1.draw()

            else:
                pass
    
    def sobel_igniter(self):
        if self.t1_checkbox.isChecked() == True:
            self.matrix = self.axes_like.get_array()

            self.axes_object_mrı_monitor[0].clear()
            self.fig_canvas_t1.draw()

            self.sobel_matrix,self.sobel_to_normal_matrix_value = image_processing.sobel_function(self.matrix)
            
            self.axes_object_mrı_monitor[0].imshow(self.sobel_matrix,cmap='gray')
            self.fig_canvas_t1.draw()

        if self.t2_checkbox.isChecked() == True:
            self.matrix = self.axes_like.get_array()

            self.axes_object_mrı_monitor[1].clear()
            self.fig_canvas_t1.draw()

            self.sobel_matrix,self.sobel_to_normal_matrix_value = image_processing.sobel_function(self.matrix)
            
            self.axes_object_mrı_monitor[1].imshow(self.sobel_matrix,cmap='gray')
            self.fig_canvas_t1.draw()

        if self.flair_checkbox.isChecked() == True:
            self.matrix = self.axes_like.get_array()

            self.axes_object_mrı_monitor[2].clear()
            self.fig_canvas_t1.draw()

            self.sobel_matrix,self.sobel_to_normal_matrix_value = image_processing.sobel_function(self.matrix)
            
            self.axes_object_mrı_monitor[2].imshow(self.sobel_matrix,cmap='gray')
            self.fig_canvas_t1.draw()
    
    def sobel_to_normal_matrix(self):
        try:
            if self.t1_checkbox.isChecked() == True:
                self.axes_object_mrı_monitor[0].clear()
                self.fig_canvas_t1.draw()
                
                self.axes_object_mrı_monitor[0].imshow(self.sobel_to_normal_matrix_value,cmap='gray')
                self.fig_canvas_t1.draw()

        except Exception as sobel_to_normal_matrix_exception:
            print(f'function: sobel_to_normal_matrix\nerror:{sobel_to_normal_matrix_exception}')
            pass

        try:
            if self.t2_checkbox.isChecked() == True:
                self.axes_object_mrı_monitor[1].clear()
                self.fig_canvas_t1.draw()
                
                self.axes_object_mrı_monitor[1].imshow(self.sobel_to_normal_matrix_value,cmap='gray')
                self.fig_canvas_t1.draw()

        except Exception as sobel_to_normal_matrix_exception:
            print(f'function: sobel_to_normal_matrix\nerror:{sobel_to_normal_matrix_exception}')
            pass

        try:
            if self.t3_checkbox.isChecked() == True:
                self.axes_object_mrı_monitor[2].clear()
                self.fig_canvas_t1.draw()
                
                self.axes_object_mrı_monitor[2].imshow(self.sobel_to_normal_matrix_value,cmap='gray')
                self.fig_canvas_t1.draw()

        except Exception as sobel_to_normal_matrix_exception:
            print(f'function: sobel_to_normal_matrix\nerror:{sobel_to_normal_matrix_exception}')
            pass

    def optimize_widget_sizes(self):
        self.checbox_reset_button.setFixedHeight(self.save_mri_image_button.height())
        self.checbox_apply_button.setFixedHeight(self.save_mri_image_button.height())
        self.add_to_list_button.setFixedHeight(self.define_file_button.height())
        self.delete_mri_image_button.setFixedHeight(self.reset_path_button.height())

    def list_item_igniter(self):
        self.list_function(self.current_selected,self.current_selected_name)

    def monitor_image_export_igniter(self):
        self.list_item_f = self.mri_list.currentItem()
        self.export_to_monitor(list_item=self.list_item_f)

    def list_function(self,image_path,image_name):
        image_matrix = self.axes_like.get_array()
        self.image_path_list_function = image_path
        self.image_name_list_function = image_name

        self.list_widget_item = QListWidgetItem(str(f'Dosya ismi: {self.image_name_list_function}\nDosya yolu: {self.image_path_list_function}'))
        self.list_item_f = self.list_widget_item

        self.list_widget_item.setIcon(QIcon(str(self.image_path_list_function)))
        self.mri_list.addItem(self.list_widget_item)

    def delete_list_item_function(self):
        selected_items = self.mri_list.selectedItems()
        for item in selected_items:
            f = self.mri_list.takeItem(self.mri_list.row(item))  
            del f       

    def define_folder(self):
        self.folder_path_str = self.folder_path.text()

        modelindex = self.file_system_model.setRootPath(self.folder_path_str)
        self.tree_view.setRootIndex(modelindex)

    def define_file(self):
        self.current_selected = self.file_system_model.filePath(self.tree_view.currentIndex())
        self.current_selected_name = self.file_system_model.fileName(self.tree_view.currentIndex())

        self.current_list_item_image_path = self.current_selected

        if True:
            if  self.current_selected.endswith('.png') or self.current_selected.endswith('jpg') or self.current_selected.endswith('jpeg'):
                print(self.current_selected)
                information_message = QMessageBox.information(self,'TANİMLAMA İSLEMİ BASARİLİ','Medikal goruntu dosyasi basari ile tanimlandi!')
            
                if self.current_selected.endswith('.png') or self.current_selected.endswith('.jpg'):
                    self.defined_ax.clear()
                    self.defined_figurecanvas_object.draw()
                    
                    self.axes_like = self.defined_ax.imshow(image_processing.to_matrix(self.current_selected))
                    self.defined_figurecanvas_object.draw()

            elif self.current_selected.endswith('.nii') or self.current_selected.endswith('.nii.gz'):
                method = file_actions.matrix_returner(path=self.current_selected,name=self.current_selected_name) 
                
                self.current_medical_file = method[0]
                self.current_medical_file_shape = self.current_medical_file.shape

                h,w,d = self.current_medical_file_shape

                if method:
                    self.defined_ax.imshow(self.current_medical_file[:,:,d - 1],cmap='gray')
                    self.defined_figurecanvas_object.draw()


                else:
                    print('dont found file',method)

            else:
                warnin_message = QMessageBox.warning(self,'TANİMLAMA İSLEMİ BASARİSİZ','Lütfen aşağıdaki belirtilen dosya uzantıları hariç bir dosyayı tanımlamaya çalışmayınız:\n\n.nii .dcm .png .jpg')
                
                    


from PyQt5.QtWidgets import*
from PyQt5.QtCore import*
from PyQt5.QtGui import*
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT  as NavigationToolbar
import matplotlib.pyplot as plt
import numpy as np

import system
import image_processing
import file_actions

class MainUİ(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MGAA Medikal Görüntü Analiz Aracı')

        self.current_medical_file = None
        self.current_medical_file_shape = None
        self.current_list_item_image_path = None
        self.current_selected = None
        self.current_selected_name = None
        self.list_item_f = None
        
        #layout-side#
        self.main_layout = QHBoxLayout()

        #widget-side#
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)

        #taskbar-side#
        self.menubar_main = self.menuBar()
        self.file_system_menu = self.menubar_main.addMenu('Dosya sistemim')
        self.file_sys_menu_open = self.file_system_menu.addAction('Aç')
        self.file_sys_menu_close = self.file_system_menu.addAction('Kapat')

        self.medical_image_list_menu = self.menubar_main.addMenu('Medikal görüntülerim')
        self.med_img_lst_menu_open = self.medical_image_list_menu.addAction('Aç')
        self.med_img_lst_menu_close = self.medical_image_list_menu.addAction('Kapat')
        
        self.file_system_menu.setIcon(QIcon(r'icons\folder.png'))
        self.file_system_menu.setWindowIcon(QIcon(r'icons\folder.png'))

        self.medical_image_list_menu.setIcon(QIcon(r'icons\pharmacy.png'))
        self.medical_image_list_menu.setWindowIcon(QIcon(r'icons\pharmacy.png'))

        #splitter-side#
        self.mri_list_splitter = QSplitter(Qt.Vertical)
        self.mri_monitor_image_settings_splitter = QSplitter(Qt.Vertical)
        self.mri_monitor_splitter = QSplitter(Qt.Vertical)
        self.mri_monitor_view_settings_splitter = QSplitter(Qt.Vertical)
        self.mri_monitor_view_settings_splitter_container = QSplitter(Qt.Horizontal)
        self.monitor_splitter_container = QSplitter(Qt.Horizontal)
        self.file_system_splitter = QSplitter(Qt.Vertical)
        self.image_selecter_splitter = QSplitter(Qt.Vertical)

        self.depth_splitter = QSplitter(Qt.Vertical)
        self.threshold_splitter = QSplitter(Qt.Vertical)
        self.sobel_splitter = QSplitter(Qt.Vertical)
        self.gauss_splitter = QSplitter(Qt.Vertical)
        self.median_splitter = QSplitter(Qt.Vertical)
        self.blur_splitter = QSplitter(Qt.Vertical)
        self.edege_splitter = QSplitter(Qt.Vertical)

        self.select_threshold_splitter = QSplitter(Qt.Horizontal)
        
        #program-widget-side#
        self.mri_list = QListWidget()

        self.show_mri_image_button = QPushButton('Monitöre aktar')
        self.add_mri_image_button = QPushButton('Ekle')
        self.save_mri_image_button = QPushButton('Kaydet')
        self.delete_mri_image_button = QPushButton('Sil')

        self.tumor_detection_checkbox = QCheckBox()
        self.bright_dimmer_checkbox = QCheckBox()
        self.normal_setting_checkbox = QCheckBox()
        self.checbox_apply_button = QPushButton(text='Uygula')
        self.checbox_reset_button = QPushButton(text='Sıfırla')

        self.return_preverius_matrix = QPushButton(text='İşlemi geri al')
        self.update_matrix_object = QPushButton(text='İşlemi kaydet')

        self.tumor_detection_checkbox.setText('Tümör Tespiti')
        self.bright_dimmer_checkbox.setText('Görüntüyü Parlat')
        self.normal_setting_checkbox.setText('Normal Şekilde Göster')

        self.depth_label = QLabel(text='Slice')
        self.threshold_label = QLabel(text='Eşik')
        self.edge_label = QLabel(text='Kenarlar')
        self.sobel_label = QLabel(text='Kenar Netliği')
        self.gaussian_label = QLabel(text='Gaussiyen')
        self.median_label = QLabel(text='Medyan')
        self.blur_label = QLabel(text='Blur')

        self.depth_slider = QSlider(Qt.Horizontal)

        self.threshold_bins_slider = QSlider(Qt.Horizontal)
        self.threshold_maxval_slider = QSlider(Qt.Horizontal)

        self.edge_thres1_slider = QSlider(Qt.Horizontal)
        self.edge_thres2_slider = QSlider(Qt.Horizontal)

        self.sobel_button = QPushButton(text='Kenarları netleştir')
        self.sobel_to_normal_button = QPushButton(text='Eski görsele dön')

        self.gaussian_x_slider = QSlider(Qt.Horizontal)
        self.gaussian_y_slider = QSlider(Qt.Horizontal)
        self.gaussian_z_slider = QSlider(Qt.Horizontal)

        self.median_slider = QSlider(Qt.Horizontal)

        self.blur_slider = QSlider(Qt.Horizontal)

        self.figure_object_mrı_monitor,self.axes_object_mrı_monitor = plt.subplots(nrows=1,ncols=3,figsize=(14,4),facecolor='gray')

        self.fig_canvas_t1 = FigureCanvas(figure=self.figure_object_mrı_monitor)
        self.custom_toolbar = NavigationToolbar(canvas=self.fig_canvas_t1)

        self.file_path = QLineEdit()
        self.folder_path = QLineEdit()
        self.file_path.setAlignment(Qt.AlignCenter)
        self.folder_path.setAlignment(Qt.AlignCenter)
        self.file_path.setPlaceholderText('Dosya yolu')
        self.folder_path.setPlaceholderText('Klasör yolu')

        self.file_system_model = QFileSystemModel()
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.file_system_model)

        self.define_file_button = QPushButton(text='MRI dosyasını tanımla')
        self.define_folder_button = QPushButton(text='Klasör Tanımla')
        self.reset_path_button = QPushButton(text='Sıfırla')

        self.mrı_select_information = QLabel(text='İşlem yapılacak MRI görüntüleme türünü Seç')
        self.t1_checkbox = QCheckBox()
        self.t2_checkbox = QCheckBox()
        self.flair_checkbox = QCheckBox()

        self.threshold_binary_checkbox = QCheckBox()
        self.threshold_otsu_checkbox = QCheckBox()
        self.threshold_tozero_checkbox = QCheckBox()
        self.threshold_tozero_ınv_checkbox = QCheckBox()
        self.threshold_trunc_checkbox = QCheckBox()
        self.threshold_binary_inv_checkbox = QCheckBox()

        self.threshold_binary_checkbox.setText('İkili eşikleme')
        self.threshold_binary_inv_checkbox.setText('Ters ikili eşikleme')
        self.threshold_trunc_checkbox.setText('Sınırlı eşikleme')
        self.threshold_tozero_checkbox.setText('Sıfıra eşikleme')
        self.threshold_tozero_ınv_checkbox.setText('Ters sıfıra eşikleme')


        self.defined_fig,self.defined_ax = plt.subplots(nrows=1,ncols=1,figsize=(5,4),facecolor='gray')
        self.defined_ax.axis('off')
        self.defined_figurecanvas_object = FigureCanvas(self.defined_fig)
        self.defined_figurecanvas_object.setStyleSheet('border:1 px solid gray')

        self.add_to_list_button = QPushButton(text='Görüntüyü listeye ekle')
        self.delete_image_button = QPushButton(text='Görüntüyü Sil')

        try:
            self.axes_like = self.defined_ax.imshow(image_processing.to_matrix('t1.png'))
        except:
            self.axes_like = self.defined_ax.imshow([[0]*40,[1]*40,[0]*40])

        
        self.t1_checkbox.setText('T1 MRI')
        self.t2_checkbox.setText('T2 MRI')
        self.flair_checkbox.setText('Flair MRI')

        #widget-parent-settings#
        item = QListWidgetItem('MRI Görüntüleri burada gözükecektir..')
        item.setTextAlignment(Qt.AlignCenter)
        self.mri_list.addItem(item)
        self.mri_list.setIconSize(QSize(64,64))

        self.main_layout.addWidget(self.monitor_splitter_container)

        self.depth_splitter.addWidget(self.depth_label)
        self.depth_splitter.addWidget(self.depth_slider)

        self.threshold_splitter.addWidget(self.threshold_label)
        self.threshold_splitter.addWidget(self.threshold_bins_slider)
        self.threshold_splitter.addWidget(self.threshold_maxval_slider)

        self.sobel_splitter.addWidget(self.sobel_label)
        self.sobel_splitter.addWidget(self.sobel_button)
        self.sobel_splitter.addWidget(self.sobel_to_normal_button)

        self.gauss_splitter.addWidget(self.gaussian_label)
        self.gauss_splitter.addWidget(self.gaussian_x_slider)
        self.gauss_splitter.addWidget(self.gaussian_y_slider)
        self.gauss_splitter.addWidget(self.gaussian_z_slider)

        self.median_splitter.addWidget(self.median_label)
        self.median_splitter.addWidget(self.median_slider)

        self.blur_splitter.addWidget(self.blur_label)
        self.blur_splitter.addWidget(self.blur_slider)

        self.monitor_splitter_container.addWidget(self.mri_list_splitter)
        self.monitor_splitter_container.addWidget(self.mri_monitor_image_settings_splitter)
        self.monitor_splitter_container.addWidget(self.mri_monitor_splitter)    
        self.monitor_splitter_container.addWidget(self.image_selecter_splitter)
        self.monitor_splitter_container.addWidget(self.file_system_splitter)    

        self.mri_list_splitter.addWidget(self.mri_list)
        self.mri_list_splitter.addWidget(self.show_mri_image_button)
        #self.mri_list_splitter.addWidget(self.add_mri_image_button)
        self.mri_list_splitter.addWidget(self.delete_mri_image_button)
        self.mri_list_splitter.addWidget(self.save_mri_image_button)

        self.mri_monitor_image_settings_splitter.addWidget(QLabel(text='Mrı Görüntüsünün işlenme türünü seç'))
        self.mri_monitor_image_settings_splitter.addWidget(self.tumor_detection_checkbox)
        self.mri_monitor_image_settings_splitter.addWidget(self.bright_dimmer_checkbox)
        self.mri_monitor_image_settings_splitter.addWidget(self.normal_setting_checkbox)
        for contf_ in [QLabel(),QLabel(),QLabel(),QLabel(),QLabel(),QLabel(),QLabel(),QLabel(),QLabel(),QLabel(),QLabel(),QLabel(),QLabel(),QLabel(),QLabel()]:
            contf_.setStyleSheet('border: none')
            self.mri_monitor_image_settings_splitter.addWidget(contf_)
        self.mri_monitor_image_settings_splitter.addWidget(self.checbox_apply_button)
        self.mri_monitor_image_settings_splitter.addWidget(self.checbox_reset_button)

        self.mri_monitor_view_settings_splitter_container.addWidget(self.gauss_splitter)
        self.mri_monitor_view_settings_splitter_container.addWidget(self.threshold_splitter)
        self.mri_monitor_view_settings_splitter_container.addWidget(self.edege_splitter)
        self.mri_monitor_view_settings_splitter_container.addWidget(self.depth_splitter)
        self.mri_monitor_view_settings_splitter_container.addWidget(self.median_splitter)
        self.mri_monitor_view_settings_splitter_container.addWidget(self.blur_splitter)
        self.mri_monitor_view_settings_splitter_container.addWidget(self.sobel_splitter)

        #self.file_system_splitter.addWidget(self.file_path)
        self.file_system_splitter.addWidget(self.folder_path)
        self.file_system_splitter.addWidget(self.tree_view)
        self.file_system_splitter.addWidget(self.define_folder_button)
        self.file_system_splitter.addWidget(self.define_file_button)
        self.file_system_splitter.addWidget(self.reset_path_button)
        
        self.mri_monitor_splitter.addWidget(self.select_threshold_splitter)
        self.mri_monitor_splitter.addWidget(self.custom_toolbar)
        self.mri_monitor_splitter.addWidget(self.fig_canvas_t1)
        self.mri_monitor_splitter.addWidget(self.return_preverius_matrix)
        self.mri_monitor_splitter.addWidget(self.update_matrix_object)
        self.mri_monitor_splitter.addWidget(self.mri_monitor_view_settings_splitter_container)

        self.image_selecter_splitter.addWidget(self.mrı_select_information)
        self.image_selecter_splitter.addWidget(self.t1_checkbox)
        self.image_selecter_splitter.addWidget(self.t2_checkbox)
        self.image_selecter_splitter.addWidget(self.flair_checkbox)

        self.select_threshold_splitter.addWidget(self.threshold_binary_checkbox)
        self.select_threshold_splitter.addWidget(self.threshold_binary_inv_checkbox)
        self.select_threshold_splitter.addWidget(self.threshold_tozero_checkbox)
        self.select_threshold_splitter.addWidget(self.threshold_tozero_ınv_checkbox)
        self.select_threshold_splitter.addWidget(self.threshold_trunc_checkbox)
        self.select_threshold_splitter.addWidget(self.threshold_otsu_checkbox)

        self.cont_container = [QLabel(),QLabel(text='Tanımlanan görüntü')]

        for cont in range(len(self.cont_container)):
            self.cont_container[cont].setStyleSheet('border:none')
            self.cont_container[cont].setAlignment(Qt.AlignCenter)
            self.image_selecter_splitter.addWidget(self.cont_container[cont])
        self.image_selecter_splitter.addWidget(self.defined_figurecanvas_object)
        self.image_selecter_splitter.addWidget(self.add_to_list_button)
        self.image_selecter_splitter.addWidget(self.delete_image_button)

        for a in range(len(self.axes_object_mrı_monitor)):
            self.axes_object_mrı_monitor[a].axis('off')
        
        try:
            self.axes_object_mrı_monitor[0].imshow(image_processing.to_matrix('t1.png'))
            self.axes_object_mrı_monitor[1].imshow(image_processing.to_matrix('t2.png'))
            self.axes_object_mrı_monitor[2].imshow(image_processing.to_matrix('tumor.jpg'))

        except:
            pass
        self.axes_object_mrı_monitor[0].set_title('T1-MRI',color='white')
        self.axes_object_mrı_monitor[1].set_title('T2-MRI',color='white')
        self.axes_object_mrı_monitor[2].set_title('Flair-MRI',color='white')

        #timers-side#
        self.optimize_w_timer = QTimer(self)
        #self.optimize_w_timer.start(10)
        self.optimize_w_timer.timeout.connect(self.optimize_widget_sizes)

        #signal-slot-side#
        self.define_folder_button.clicked.connect(self.define_folder)
        self.define_file_button.clicked.connect(self.define_file)
        self.add_to_list_button.clicked.connect(self.list_item_igniter)
        self.delete_mri_image_button.clicked.connect(self.delete_list_item_function)
        self.show_mri_image_button.clicked.connect(self.monitor_image_export_igniter)
        self.checbox_apply_button.clicked.connect(self.other_actions_igniter)

        
        #signal-slot-matrix-actions-side#
        self.update_matrix_object.clicked.connect(self.get_current_matrix)
        self.return_preverius_matrix.clicked.connect(self.remove_image_from_axes)

        #signal-slot-slider-side#
        self.threshold_bins_slider.valueChanged.connect(self.threshold_igniter)
        self.threshold_maxval_slider.valueChanged.connect(self.threshold_igniter)

        self.gaussian_x_slider.valueChanged.connect(self.gaussian_igniter)
        self.gaussian_y_slider.valueChanged.connect(self.gaussian_igniter)
        self.gaussian_z_slider.valueChanged.connect(self.gaussian_igniter)

        self.median_slider.valueChanged.connect(self.median_igniter)

        self.sobel_button.clicked.connect(self.sobel_igniter)
        self.sobel_to_normal_button.clicked.connect(self.sobel_to_normal_matrix)

        self.file_sys_menu_open.triggered.connect(self.show_file_system)
        self.file_sys_menu_close.triggered.connect(self.hide_file_system)

        self.med_img_lst_menu_open.triggered.connect(self.show_image_settings)
        self.med_img_lst_menu_close.triggered.connect(self.hide_image_settings)

        self.depth_slider.valueChanged.connect(self.depth_slider_function)

        #css-define-side#
        self.css_qss_file = open(r'program_css.qss','r').read()
        self.setStyleSheet(str(self.css_qss_file))

        self.setCentralWidget(self.main_widget)

        attention_text = 'Bu program tıbbi bir programdır. Doğrudan teşhis koyamaz, yanlızca önerililerde bulunabilir. Programı kullanarak bunları kabul etmiş varsayılırsınız.'

        self.msgbox = QMessageBox.question(self,'Dikkat',attention_text,QMessageBox.Ok | QMessageBox.Cancel)
        if self.msgbox != QMessageBox.Cancel:
            self.swap_gui()
        
        else:
            pass

    def get_current_matrix(self):
        if self.t1_checkbox.isChecked() == True:
            self.axes_like = self.axes_object_mrı_monitor[0].get_images().pop()
            print(self.axes_like)

        if self.t2_checkbox.isChecked() == True:
            self.axes_like = self.axes_object_mrı_monitor[1].get_images().pop()
            print(self.axes_like)
            
        if self.flair_checkbox.isChecked() == True:
            self.axes_like = self.axes_object_mrı_monitor[2].get_images().pop()
            print(self.axes_like)   
    
    def depth_slider_function(self):
        if self.t1_checkbox.isChecked() == True:
            h,w,d = self.current_medical_file_shape

            current_slice = image_processing.mrı_slice_returner(self.current_medical_file,h,w,d)

            print(current_slice)

    def swap_gui(self):

        #self.mri_monitor_splitter.setParent(None)
        #self.monitor_splitter_container.setParent(None)
        #self.mri_list_splitter.setParent(None)
        self.mri_monitor_image_settings_splitter.setParent(None)
        self.file_system_splitter.setParent(None)
        #self.image_selecter_splitter.setParent(None)
        #self.mri_monitor_view_settings_splitter.setParent(None)

        self.mri_monitor_image_settings_splitter.setStyleSheet(str(self.css_qss_file))
        self.file_system_splitter.setStyleSheet(str(self.css_qss_file))

        self.dock1 = QDockWidget()
        self.dock2 = QDockWidget()

        self.dock1.setParent(self)
        self.dock1.setWidget(self.file_system_splitter)
        self.dock1.setFixedWidth(500)

        self.dock2.setParent(self)
        self.dock2.setWidget(self.mri_monitor_image_settings_splitter)
        self.dock2.setFixedHeight(450)
        self.dock2.setFixedWidth(300)

        self.dock1.hide()
        self.dock2.hide()
    
    def show_file_system(self):
        self.dock1.show()
    
    def hide_file_system(self):
        self.dock1.hide()
    
    def show_image_settings(self):
        self.dock2.show()
    
    def hide_image_settings(self):
        self.dock2.hide()
    
    

    def remove_image_from_axes(self):
        if self.t1_checkbox.isChecked() == True:
            self.axes_object_mrı_monitor[0].clear()
            self.axes_object_mrı_monitor[0].imshow([
                                                    [1,0,0,0,0,0,0,0,1],
                                                    [0,1,0,0,0,0,0,1,0],
                                                    [0,0,1,0,0,0,1,0,0],
                                                    [0,0,0,1,0,1,0,0,0],
                                                    [0,0,0,0,1,0,0,0,0],
                                                    [0,0,0,1,0,1,0,0,0],
                                                    [0,0,1,0,0,0,1,0,0],
                                                    [0,1,0,0,0,0,0,1,0],
                                                    [1,0,0,0,0,0,0,0,1]
                                                    ],cmap='gray')
            self.axes_like = self.axes_object_mrı_monitor[0].get_images()
            self.fig_canvas_t1.draw()
        
        if self.t2_checkbox.isChecked() == True:
            self.axes_object_mrı_monitor[1].clear()
            self.axes_object_mrı_monitor[1].imshow([
                                                    [1,0,0,0,0,0,0,0,1],
                                                    [0,1,0,0,0,0,0,1,0],
                                                    [0,0,1,0,0,0,1,0,0],
                                                    [0,0,0,1,0,1,0,0,0],
                                                    [0,0,0,0,1,0,0,0,0],
                                                    [0,0,0,1,0,1,0,0,0],
                                                    [0,0,1,0,0,0,1,0,0],
                                                    [0,1,0,0,0,0,0,1,0],
                                                    [1,0,0,0,0,0,0,0,1]
                                                    ],cmap='gray')
            self.axes_like = self.axes_object_mrı_monitor[1].get_images()
            self.fig_canvas_t1.draw()

        if self.flair_checkbox.isChecked() == True:
            self.axes_object_mrı_monitor[2].clear()
            self.axes_object_mrı_monitor[2].imshow([
                                                    [1,0,0,0,0,0,0,0,1],
                                                    [0,1,0,0,0,0,0,1,0],
                                                    [0,0,1,0,0,0,1,0,0],
                                                    [0,0,0,1,0,1,0,0,0],
                                                    [0,0,0,0,1,0,0,0,0],
                                                    [0,0,0,1,0,1,0,0,0],
                                                    [0,0,1,0,0,0,1,0,0],
                                                    [0,1,0,0,0,0,0,1,0],
                                                    [1,0,0,0,0,0,0,0,1]
                                                    ],cmap='gray')
            self.axes_like = self.axes_object_mrı_monitor[2].get_images()
            self.fig_canvas_t1.draw()
    
    def other_actions_igniter(self):
        #self.threshold_splitter.setEnabled(False)
        #self.threshold_splitter.setWindowOpacity(0.5)
        if self.tumor_detection_checkbox.isChecked() == True:
            self.matrix_a = self.axes_like.get_array()
            if self.t1_checkbox.isChecked() == True:
                self.tumor_detecetion_output = image_processing.tumor_detection_function(matrix=self.matrix_a)

                self.axes_object_mrı_monitor[0].imshow(self.tumor_detecetion_output,cmap='gray')
                self.fig_canvas_t1.draw()

    def median_igniter(self):
        self.ksizemv = self.median_slider.value()
        self.matrix = self.axes_like.get_array()
        if self.t1_checkbox.isChecked() == True:
            median_function = image_processing.median_function(self.matrix,self.ksizemv)

            if type(median_function) != str:
                self.axes_object_mrı_monitor[0].imshow(median_function)
                self.fig_canvas_t1.draw()
            
            else:
                pass

        if self.t2_checkbox.isChecked() == True:
            median_function = image_processing.median_function(self.matrix,self.ksizemv)

            if type(median_function) != str:
                self.axes_object_mrı_monitor[1].imshow(median_function,cmap='gray')
                self.fig_canvas_t1.draw()
            
            else:
                pass

        if self.flair_checkbox.isChecked() == True:
            median_function = image_processing.median_function(self.matrix,self.ksizemv)

            if type(median_function) != str:
                self.axes_object_mrı_monitor[2].imshow(median_function,cmap='gray')
                self.fig_canvas_t1.draw()
            
            else:
                pass

    def threshold_igniter(self):
        if self.t1_checkbox.isChecked() == True:
            if self.threshold_binary_checkbox.isChecked() == True:
                self.flag = 'binary'
                self.matrix = self.axes_like.get_array()
                self.thres = self.threshold_bins_slider.value()
                self.maxval = self.threshold_maxval_slider.value()

                threshold_matrix,normal_matrix = image_processing.threshold_function(self.matrix,self.thres,self.maxval,self.flag)

                self.axes_object_mrı_monitor[0].imshow(threshold_matrix,cmap='gray')
                self.fig_canvas_t1.draw()
            
            elif self.threshold_binary_inv_checkbox.isChecked() == True:
                self.flag = 'binary_inv'
                self.matrix = self.axes_like.get_array()
                self.thres = self.threshold_bins_slider.value()
                self.maxval = self.threshold_maxval_slider.value()

                threshold_matrix,normal_matrix = image_processing.threshold_function(self.matrix,self.thres,self.maxval,self.flag)

                self.axes_object_mrı_monitor[0].imshow(threshold_matrix,cmap='gray')
                self.fig_canvas_t1.draw()     

            elif self.threshold_trunc_checkbox.isChecked() == True:
                self.flag = 'threshold_trunc'
                self.matrix = self.axes_like.get_array()
                self.thres = self.threshold_bins_slider.value()
                self.maxval = self.threshold_maxval_slider.value()

                threshold_matrix,normal_matrix = image_processing.threshold_function(self.matrix,self.thres,self.maxval,self.flag)

                self.axes_object_mrı_monitor[0].imshow(threshold_matrix,cmap='gray')
                self.fig_canvas_t1.draw()    
            
            elif self.threshold_tozero_checkbox.isChecked() == True:
                self.flag = 'threshold_tozero'
                self.matrix = self.axes_like.get_array()
                self.thres = self.threshold_bins_slider.value()
                self.maxval = self.threshold_maxval_slider.value()

                threshold_matrix,normal_matrix = image_processing.threshold_function(self.matrix,self.thres,self.maxval,self.flag)

                self.axes_object_mrı_monitor[0].imshow(threshold_matrix,cmap='gray')
                self.fig_canvas_t1.draw()     

            elif self.threshold_tozero_ınv_checkbox.isChecked() == True:
                self.flag = 'threshold_tozero_inv'
                self.matrix = self.axes_like.get_array()
                self.thres = self.threshold_bins_slider.value()
                self.maxval = self.threshold_maxval_slider.value()

                threshold_matrix,normal_matrix = image_processing.threshold_function(self.matrix,self.thres,self.maxval,self.flag)

                self.axes_object_mrı_monitor[0].imshow(threshold_matrix,cmap='gray')
                self.fig_canvas_t1.draw()     

        elif self.t2_checkbox.isChecked() == True:
            if self.threshold_binary_checkbox.isChecked() == True:
                self.flag = 'binary'
                self.matrix = self.axes_like.get_array()
                self.thres = self.threshold_bins_slider.value()
                self.maxval = self.threshold_maxval_slider.value()

                threshold_matrix,normal_matrix = image_processing.threshold_function(self.matrix,self.thres,self.maxval,self.flag)

                self.axes_object_mrı_monitor[1].imshow(threshold_matrix,cmap='gray')
                self.fig_canvas_t1.draw()
            
            elif self.threshold_binary_inv_checkbox.isChecked() == True:
                self.flag = 'binary_inv'
                self.matrix = self.axes_like.get_array()
                self.thres = self.threshold_bins_slider.value()
                self.maxval = self.threshold_maxval_slider.value()

                threshold_matrix,normal_matrix = image_processing.threshold_function(self.matrix,self.thres,self.maxval,self.flag)

                self.axes_object_mrı_monitor[1].imshow(threshold_matrix,cmap='gray')
                self.fig_canvas_t1.draw()     

            elif self.threshold_trunc_checkbox.isChecked() == True:
                self.flag = 'threshold_trunc'
                self.matrix = self.axes_like.get_array()
                self.thres = self.threshold_bins_slider.value()
                self.maxval = self.threshold_maxval_slider.value()

                threshold_matrix,normal_matrix = image_processing.threshold_function(self.matrix,self.thres,self.maxval,self.flag)

                self.axes_object_mrı_monitor[1].imshow(threshold_matrix,cmap='gray')
                self.fig_canvas_t1.draw()    
            
            elif self.threshold_tozero_checkbox.isChecked() == True:
                self.flag = 'threshold_tozero'
                self.matrix = self.axes_like.get_array()
                self.thres = self.threshold_bins_slider.value()
                self.maxval = self.threshold_maxval_slider.value()

                threshold_matrix,normal_matrix = image_processing.threshold_function(self.matrix,self.thres,self.maxval,self.flag)

                self.axes_object_mrı_monitor[1].imshow(threshold_matrix,cmap='gray',alpha=0.5)
                self.fig_canvas_t1.draw()     

            elif self.threshold_tozero_ınv_checkbox.isChecked() == True:
                self.flag = 'threshold_tozero_inv'
                self.matrix = self.axes_like.get_array()
                self.thres = self.threshold_bins_slider.value()
                self.maxval = self.threshold_maxval_slider.value()

                threshold_matrix,normal_matrix = image_processing.threshold_function(self.matrix,self.thres,self.maxval,self.flag)

                self.axes_object_mrı_monitor[1].imshow(threshold_matrix,cmap='gray')
                self.fig_canvas_t1.draw()     

        elif self.flair_checkbox.isChecked() == True:
            if self.threshold_binary_checkbox.isChecked() == True:
                self.flag = 'binary'
                self.matrix = self.axes_like.get_array()
                self.thres = self.threshold_bins_slider.value()
                self.maxval = self.threshold_maxval_slider.value()

                threshold_matrix,normal_matrix = image_processing.threshold_function(self.matrix,self.thres,self.maxval,self.flag)

                self.axes_object_mrı_monitor[2].imshow(threshold_matrix,cmap='gray')
                self.fig_canvas_t1.draw()
            
            elif self.threshold_binary_inv_checkbox.isChecked() == True:
                self.flag = 'binary_inv'
                self.matrix = self.axes_like.get_array()
                self.thres = self.threshold_bins_slider.value()
                self.maxval = self.threshold_maxval_slider.value()

                threshold_matrix,normal_matrix = image_processing.threshold_function(self.matrix,self.thres,self.maxval,self.flag)

                self.axes_object_mrı_monitor[2].imshow(threshold_matrix,cmap='gray')
                self.fig_canvas_t1.draw()     

            elif self.threshold_trunc_checkbox.isChecked() == True:
                self.flag = 'threshold_trunc'
                self.matrix = self.axes_like.get_array()
                self.thres = self.threshold_bins_slider.value()
                self.maxval = self.threshold_maxval_slider.value()

                threshold_matrix,normal_matrix = image_processing.threshold_function(self.matrix,self.thres,self.maxval,self.flag)

                self.axes_object_mrı_monitor[2].imshow(threshold_matrix,cmap='gray')
                self.fig_canvas_t1.draw()    
            
            elif self.threshold_tozero_checkbox.isChecked() == True:
                self.flag = 'threshold_tozero'
                self.matrix = self.axes_like.get_array()
                self.thres = self.threshold_bins_slider.value()
                self.maxval = self.threshold_maxval_slider.value()

                threshold_matrix,normal_matrix = image_processing.threshold_function(self.matrix,self.thres,self.maxval,self.flag)

                self.axes_object_mrı_monitor[2].imshow(threshold_matrix,cmap='gray')
                self.fig_canvas_t1.draw()     

            elif self.threshold_tozero_ınv_checkbox.isChecked() == True:
                self.flag = 'threshold_tozero_inv'
                self.matrix = self.axes_like.get_array()
                self.thres = self.threshold_bins_slider.value()
                self.maxval = self.threshold_maxval_slider.value()

                threshold_matrix,normal_matrix = image_processing.threshold_function(self.matrix,self.thres,self.maxval,self.flag)

                self.axes_object_mrı_monitor[2].imshow(threshold_matrix,cmap='gray')
                self.fig_canvas_t1.draw()     

    def gaussian_igniter(self):
        if self.t1_checkbox.isChecked() == True:
            self.matrix = self.axes_like.get_array()
            self.ksize = (self.gaussian_x_slider.value(),self.gaussian_x_slider.value())
            self.sigmaX = self.gaussian_y_slider.value()
            self.sigmaY = self.gaussian_z_slider.value()

            self.gaussian_function_tuple_data = image_processing.gaussian_function(self.matrix,self.ksize,self.sigmaX,self.sigmaY)

            if self.gaussian_function_tuple_data:
                self.gaussian_matrixgv,self.normal_matrixgv = self.gaussian_function_tuple_data

                self.axes_object_mrı_monitor[0].imshow(self.gaussian_matrixgv,cmap='gray')
                self.fig_canvas_t1.draw()

            else:
                pass

        elif self.t2_checkbox.isChecked() == True:
            self.matrix = self.axes_like.get_array()
            self.ksize = (self.gaussian_x_slider.value(),self.gaussian_x_slider.value())
            self.sigmaX = self.gaussian_y_slider.value()
            self.sigmaY = self.gaussian_z_slider.value()

            self.gaussian_function_tuple_data = image_processing.gaussian_function(self.matrix,self.ksize,self.sigmaX,self.sigmaY)

            if self.gaussian_function_tuple_data:
                self.gaussian_matrixgv,self.normal_matrixgv = self.gaussian_function_tuple_data

                self.axes_object_mrı_monitor[1].imshow(self.gaussian_matrixgv,cmap='gray')
                self.fig_canvas_t1.draw()

            else:
                pass

        elif self.flair_checkbox.isChecked() == True:
            self.matrix = self.axes_like.get_array()
            self.ksize = (self.gaussian_x_slider.value(),self.gaussian_x_slider.value())
            self.sigmaX = self.gaussian_y_slider.value()
            self.sigmaY = self.gaussian_z_slider.value()

            self.gaussian_function_tuple_data = image_processing.gaussian_function(self.matrix,self.ksize,self.sigmaX,self.sigmaY)

            if self.gaussian_function_tuple_data:
                self.gaussian_matrixgv,self.normal_matrixgv = self.gaussian_function_tuple_data

                self.axes_object_mrı_monitor[2].imshow(self.gaussian_matrixgv,cmap='gray')
                self.fig_canvas_t1.draw()

            else:
                pass
    
    def sobel_igniter(self):
        if self.t1_checkbox.isChecked() == True:
            self.matrix = self.axes_like.get_array()

            self.axes_object_mrı_monitor[0].clear()
            self.fig_canvas_t1.draw()

            self.sobel_matrix,self.sobel_to_normal_matrix_value = image_processing.sobel_function(self.matrix)
            
            self.axes_object_mrı_monitor[0].imshow(self.sobel_matrix,cmap='gray')
            self.fig_canvas_t1.draw()

        if self.t2_checkbox.isChecked() == True:
            self.matrix = self.axes_like.get_array()

            self.axes_object_mrı_monitor[1].clear()
            self.fig_canvas_t1.draw()

            self.sobel_matrix,self.sobel_to_normal_matrix_value = image_processing.sobel_function(self.matrix)
            
            self.axes_object_mrı_monitor[1].imshow(self.sobel_matrix,cmap='gray')
            self.fig_canvas_t1.draw()

        if self.flair_checkbox.isChecked() == True:
            self.matrix = self.axes_like.get_array()

            self.axes_object_mrı_monitor[2].clear()
            self.fig_canvas_t1.draw()

            self.sobel_matrix,self.sobel_to_normal_matrix_value = image_processing.sobel_function(self.matrix)
            
            self.axes_object_mrı_monitor[2].imshow(self.sobel_matrix,cmap='gray')
            self.fig_canvas_t1.draw()
    
    def sobel_to_normal_matrix(self):
        try:
            if self.t1_checkbox.isChecked() == True:
                self.axes_object_mrı_monitor[0].clear()
                self.fig_canvas_t1.draw()
                
                self.axes_object_mrı_monitor[0].imshow(self.sobel_to_normal_matrix_value,cmap='gray')
                self.fig_canvas_t1.draw()

        except Exception as sobel_to_normal_matrix_exception:
            print(f'function: sobel_to_normal_matrix\nerror:{sobel_to_normal_matrix_exception}')
            pass

        try:
            if self.t2_checkbox.isChecked() == True:
                self.axes_object_mrı_monitor[1].clear()
                self.fig_canvas_t1.draw()
                
                self.axes_object_mrı_monitor[1].imshow(self.sobel_to_normal_matrix_value,cmap='gray')
                self.fig_canvas_t1.draw()

        except Exception as sobel_to_normal_matrix_exception:
            print(f'function: sobel_to_normal_matrix\nerror:{sobel_to_normal_matrix_exception}')
            pass

        try:
            if self.t3_checkbox.isChecked() == True:
                self.axes_object_mrı_monitor[2].clear()
                self.fig_canvas_t1.draw()
                
                self.axes_object_mrı_monitor[2].imshow(self.sobel_to_normal_matrix_value,cmap='gray')
                self.fig_canvas_t1.draw()

        except Exception as sobel_to_normal_matrix_exception:
            print(f'function: sobel_to_normal_matrix\nerror:{sobel_to_normal_matrix_exception}')
            pass

    def optimize_widget_sizes(self):
        self.checbox_reset_button.setFixedHeight(self.save_mri_image_button.height())
        self.checbox_apply_button.setFixedHeight(self.save_mri_image_button.height())
        self.add_to_list_button.setFixedHeight(self.define_file_button.height())
        self.delete_mri_image_button.setFixedHeight(self.reset_path_button.height())

    def list_item_igniter(self):
        self.list_function(self.current_selected,self.current_selected_name)

    def monitor_image_export_igniter(self):
        self.list_item_f = self.mri_list.currentItem()
        self.export_to_monitor(list_item=self.list_item_f)

    def list_function(self,image_path,image_name):
        image_matrix = self.axes_like.get_array()
        self.image_path_list_function = image_path
        self.image_name_list_function = image_name

        self.list_widget_item = QListWidgetItem(str(f'Dosya ismi: {self.image_name_list_function}\nDosya yolu: {self.image_path_list_function}'))
        self.list_item_f = self.list_widget_item

        self.list_widget_item.setIcon(QIcon(str(self.image_path_list_function)))
        self.mri_list.addItem(self.list_widget_item)

    def delete_list_item_function(self):
        selected_items = self.mri_list.selectedItems()
        for item in selected_items:
            f = self.mri_list.takeItem(self.mri_list.row(item))  
            del f       

    def define_folder(self):
        self.folder_path_str = self.folder_path.text()

        modelindex = self.file_system_model.setRootPath(self.folder_path_str)
        self.tree_view.setRootIndex(modelindex)

    def define_file(self):
        self.current_selected = self.file_system_model.filePath(self.tree_view.currentIndex())
        self.current_selected_name = self.file_system_model.fileName(self.tree_view.currentIndex())

        self.current_list_item_image_path = self.current_selected

        if True:
            if  self.current_selected.endswith('.png') or self.current_selected.endswith('jpg') or self.current_selected.endswith('jpeg'):
                print(self.current_selected)
                information_message = QMessageBox.information(self,'TANİMLAMA İSLEMİ BASARİLİ','Medikal goruntu dosyasi basari ile tanimlandi!')
            
                if self.current_selected.endswith('.png') or self.current_selected.endswith('.jpg'):
                    self.defined_ax.clear()
                    self.defined_figurecanvas_object.draw()
                    
                    self.axes_like = self.defined_ax.imshow(image_processing.to_matrix(self.current_selected))
                    self.defined_figurecanvas_object.draw()

            elif self.current_selected.endswith('.nii') or self.current_selected.endswith('.nii.gz'):
                method = file_actions.matrix_returner(path=self.current_selected,name=self.current_selected_name) 
                
                self.current_medical_file = method[0]
                self.current_medical_file_shape = self.current_medical_file.shape

                h,w,d = self.current_medical_file_shape

                if method:
                    self.defined_ax.imshow(self.current_medical_file[:,:,d - 1],cmap='gray')
                    self.defined_figurecanvas_object.draw()


                else:
                    print('dont found file',method)

            else:
                warnin_message = QMessageBox.warning(self,'TANİMLAMA İSLEMİ BASARİSİZ','Lütfen aşağıdaki belirtilen dosya uzantıları hariç bir dosyayı tanımlamaya çalışmayınız:\n\n.nii .dcm .png .jpg')
                
                    


    def export_to_monitor(self,list_item):
        try:
            if self.mri_list.item(self.mri_list.currentRow()).text() == 'Belirtilmedi':
                pass

            else:
                name = self.mri_list.item(self.mri_list.currentRow()).text().split('\n')[0].split(':')[1].strip()
                path_c = self.mri_list.item(self.mri_list.currentRow()).text().split('\n')[1].split(':')[1].strip()
                path = self.mri_list.item(self.mri_list.currentRow()).text().split('\n')[1].split(':')[2].strip()

            image_matrix = None
        except Exception as messagebox_error:
            error_message = QMessageBox.critical(self,'İşlem yapılamadı!!',f'Lütfen listeden bir mrı seçin!!,{messagebox_error}')
            
        finally:
            pass

        if self.t1_checkbox.isChecked() == True:
            if path.endswith('.nii') or self.current_selected.endswith('.nii.gz'):
                    try:
                        self.dat,self.hei,self.wid,self.dep = file_actions.matrix_returner(name=name,path=path)
                        image_matrix = self.dat
                        self.current_medical_file = self.dat
                        self.current_medical_file_shape = self.current_medical_file.shape
                            
                        self.axes_object_mrı_monitor[0].imshow(image_matrix[:,:,self.dep - 1],cmap='gray')
                        self.fig_canvas_t1.draw()
                        print('f1')
                    except:
                        try:
                            self.dat,self.hei,self.wid,self.dep = file_actions.matrix_returner(name=name,path=name)
                            image_matrix = self.dat
                            self.current_medical_file = self.dat
                            self.current_medical_file_shape = self.current_medical_file.shape

                            self.axes_object_mrı_monitor[0].imshow(image_matrix[:,:,self.dep - 1],cmap='gray')
                            self.fig_canvas_t1.draw()
                            print('f1')
                        
                        except:
                            error_message = QMessageBox.critical(self,'İşlem yapılamadı!!',f'Lütfen Başka bir dosya seçin veya dosyanın düzgün olup olmadığını kontrol edin!')

            else:
                try:
                    if path == 'Belirtilmedi':
                        try:
                            file_name = self.mri_list.item(self.mri_list.currentRow()).text().split('\n')[0].split(':')[1].strip()

                            image_matrix = image_processing.to_matrix(name)
                                
                            self.axes_object_mrı_monitor[0].imshow(image_matrix,cmap='gray')
                            self.fig_canvas_t1.draw()
                            print('f1')
                        
                        except:
                            try:
                                file_name = self.mri_list.item(self.mri_list.currentRow()).text().split('\n')[0].split(':')[1].strip()

                                image_matrix = image_processing.to_matrix(path)
                                    
                                self.axes_object_mrı_monitor[0].imshow(image_matrix,cmap='gray')
                                self.fig_canvas_t1.draw()
                                print('f1')
                            
                            except:
                                error_message = QMessageBox.critical(self,'İşlem yapılamadı!!',f'Lütfen listeden bir mrı seçin!')
            

                    
                    else:
                        try:
                            file_name = self.mri_list.item(self.mri_list.currentRow()).text().split('\n')[0].split(':')[1].strip()

                            image_matrix = image_processing.to_matrix(name)
                                
                            self.axes_object_mrı_monitor[0].imshow(image_matrix,cmap='gray')
                            self.fig_canvas_t1.draw()
                            print('f1')
                        except:
                            try:
                                file_name = self.mri_list.item(self.mri_list.currentRow()).text().split('\n')[0].split(':')[1].strip()

                                image_matrix = image_processing.to_matrix(path)
                                    
                                self.axes_object_mrı_monitor[0].imshow(image_matrix,cmap='gray')
                                self.fig_canvas_t1.draw()
                                print('f1')
                            except:
                                error_message = QMessageBox.critical(self,'İşlem yapılamadı!!',f'Lütfen listeden bir mrı seçin!')
            
            
                except:
                    try:
                        if path.endswith('.nii') or self.current_selected.endswith('.nii.gz'):
                            warning_message = QMessageBox.warning(self,'Dosyan bulunamıyor','Sistem dosyayı bulamadı. Lütfen dosyayı manuel olarak Tekrar seçiniz!') 

                            current_url,string = QFileDialog(self).getOpenFileUrl(self)           
                
                            self.dat,self.hei,self.wid,self.dep = file_actions.matrix_returner(name=name,path=path)
                            image_matrix = self.dat
                            self.current_medical_file = self.dat
                            self.current_medical_file_shape = self.current_medical_file.shape
                                
                            self.axes_object_mrı_monitor[0].imshow(image_matrix[:,:,self.dep - 1],cmap='gray')
                            self.fig_canvas_t1.draw()
                            print('f2')
                        
                        else:
                            try:
                                warning_message = QMessageBox.warning(self,'Dosyan bulunamıyor','Sistem dosyayı bulamadı. Lütfen dosyayı manuel olarak Tekrar seçiniz!') 

                                current_url,string = QFileDialog(self).getOpenFileUrl(self)           
                    
                                self.dat,self.hei,self.wid,self.dep = file_actions.matrix_returner(name=name,path=path)
                                image_matrix = self.dat
                                self.current_medical_file = self.dat
                                self.current_medical_file_shape = self.current_medical_file.shape
                                    
                                self.axes_object_mrı_monitor[0].imshow(image_matrix[:,:,self.dep - 1],cmap='gray')
                                self.fig_canvas_t1.draw()
                                print('f2')
                            except:
                                pass

                    except:
                        try:
                            
                            warning_message = QMessageBox.warning(self,'Dosya bulunamıyor','Sistem dosyayı bulamadı. Lütfen dosyayı manuel olarak Tekrar seçiniz!') 

                            current_name = 'none'     

                            self.axes_object_mrı_monitor[0].imshow(image_matrix[:,:,self.dep - 1],cmap='gray')
                            self.fig_canvas_t1.draw()
                            
                            print('f3')
                        except:
                            print('noneeeee')


             
                try:
                    self.dat,self.hei,self.wid,self.dep = file_actions.matrix_returner(name=name,path=path)
                    image_matrix = self.dat 
                    self.current_medical_file = self.dat
                    self.current_medical_file_shape = self.current_medical_file.shape

                    if image_matrix == None:
                        pass
                    
                    else:
                        self.axes_object_mrı_monitor[0].imshow(image_matrix[:,:,self.dep - 1],cmap='gray')
                        self.fig_canvas_t1.draw()
                        print('f4')
                except:
                    print(path)
                    pass

        elif self.t2_checkbox.isChecked() == True:
                if path.endswith('.nii') or self.current_selected.endswith('.nii.gz'):
                    try:
                        self.dat,self.hei,self.wid,self.dep = file_actions.matrix_returner(name=name,path=path)
                        image_matrix = self.dat
                        self.current_medical_file = self.dat
                        self.current_medical_file_shape = self.current_medical_file.shape
                            
                        self.axes_object_mrı_monitor[1].imshow(image_matrix[:,:,self.dep - 1],cmap='gray')
                        self.fig_canvas_t1.draw()
                        print('f1')
                    except:
                        try:
                            self.dat,self.hei,self.wid,self.dep = file_actions.matrix_returner(name=name,path=name)
                            image_matrix = self.dat
                            self.current_medical_file = self.dat
                            self.current_medical_file_shape = self.current_medical_file.shape

                            self.axes_object_mrı_monitor[1].imshow(image_matrix[:,:,self.dep - 1],cmap='gray')
                            self.fig_canvas_t1.draw()
                            print('f1')
                        
                        except:
                            error_message = QMessageBox.critical(self,'İşlem yapılamadı!!',f'Lütfen Başka bir dosya seçin veya dosyanın düzgün olup olmadığını kontrol edin!')

                else:
                    try:
                        if path == 'Belirtilmedi':
                            try:
                                file_name = self.mri_list.item(self.mri_list.currentRow()).text().split('\n')[0].split(':')[1].strip()

                                image_matrix = image_processing.to_matrix(name)
                                    
                                self.axes_object_mrı_monitor[1].imshow(image_matrix,cmap='gray')
                                self.fig_canvas_t1.draw()
                                print('f1')
                            
                            except:
                                try:
                                    file_name = self.mri_list.item(self.mri_list.currentRow()).text().split('\n')[0].split(':')[1].strip()

                                    image_matrix = image_processing.to_matrix(path)
                                        
                                    self.axes_object_mrı_monitor[1].imshow(image_matrix,cmap='gray')
                                    self.fig_canvas_t1.draw()
                                    print('f1')
                                
                                except:
                                    error_message = QMessageBox.critical(self,'İşlem yapılamadı!!',f'Lütfen listeden bir mrı seçin!')
                

                        
                        else:
                            try:
                                file_name = self.mri_list.item(self.mri_list.currentRow()).text().split('\n')[0].split(':')[1].strip()

                                image_matrix = image_processing.to_matrix(name)
                                    
                                self.axes_object_mrı_monitor[1].imshow(image_matrix,cmap='gray')
                                self.fig_canvas_t1.draw()
                                print('f1')
                            except:
                                try:
                                    file_name = self.mri_list.item(self.mri_list.currentRow()).text().split('\n')[0].split(':')[1].strip()

                                    image_matrix = image_processing.to_matrix(path)
                                        
                                    self.axes_object_mrı_monitor[1].imshow(image_matrix,cmap='gray')
                                    self.fig_canvas_t1.draw()
                                    print('f1')
                                except:
                                    error_message = QMessageBox.critical(self,'İşlem yapılamadı!!',f'Lütfen listeden bir mrı seçin!')
                
                
                    except:
                        try:
                            if path.endswith('.nii') or self.current_selected.endswith('.nii.gz'):
                                warning_message = QMessageBox.warning(self,'Dosyan bulunamıyor','Sistem dosyayı bulamadı. Lütfen dosyayı manuel olarak Tekrar seçiniz!') 

                                current_url,string = QFileDialog(self).getOpenFileUrl(self)           
                    
                                self.dat,self.hei,self.wid,self.dep = file_actions.matrix_returner(name=name,path=path)
                                image_matrix = self.dat
                                self.current_medical_file = self.dat
                                self.current_medical_file_shape = self.current_medical_file.shape
                                    
                                self.axes_object_mrı_monitor[1].imshow(image_matrix[:,:,self.dep - 1],cmap='gray')
                                self.fig_canvas_t1.draw()
                                print('f2')
                            
                            else:
                                try:
                                    warning_message = QMessageBox.warning(self,'Dosyan bulunamıyor','Sistem dosyayı bulamadı. Lütfen dosyayı manuel olarak Tekrar seçiniz!') 

                                    current_url,string = QFileDialog(self).getOpenFileUrl(self)           
                        
                                    self.dat,self.hei,self.wid,self.dep = file_actions.matrix_returner(name=name,path=path)
                                    image_matrix = self.dat
                                    self.current_medical_file = self.dat
                                    self.current_medical_file_shape = self.current_medical_file.shape
                                        
                                    self.axes_object_mrı_monitor[1].imshow(image_matrix[:,:,self.dep - 1],cmap='gray')
                                    self.fig_canvas_t1.draw()
                                    print('f2')
                                except:
                                    pass

                        except:
                            try:
                                
                                warning_message = QMessageBox.warning(self,'Dosya bulunamıyor','Sistem dosyayı bulamadı. Lütfen dosyayı manuel olarak Tekrar seçiniz!') 

                                current_name = 'none'     

                                self.axes_object_mrı_monitor[1].imshow(image_matrix[:,:,self.dep - 1],cmap='gray')
                                self.fig_canvas_t1.draw()
                                
                                print('f3')
                            except:
                                print('noneeeee')


                
                    try:
                        self.dat,self.hei,self.wid,self.dep = file_actions.matrix_returner(name=name,path=path)
                        image_matrix = self.dat 
                        self.current_medical_file = self.dat
                        self.current_medical_file_shape = self.current_medical_file.shape

                        if image_matrix == None:
                            pass
                        
                        else:
                            self.axes_object_mrı_monitor[1].imshow(image_matrix[:,:,self.dep - 1],cmap='gray')
                            self.fig_canvas_t1.draw()
                            print('f4')
                    except:
                        print(path)
                        pass


        elif self.flair_checkbox.isChecked() == True:
                if path.endswith('.nii') or self.current_selected.endswith('.nii.gz'):
                    try:
                        self.dat,self.hei,self.wid,self.dep = file_actions.matrix_returner(name=name,path=path)
                        image_matrix = self.dat
                        self.current_medical_file = self.dat
                        self.current_medical_file_shape = self.current_medical_file.shape
                            
                        self.axes_object_mrı_monitor[2].imshow(image_matrix[:,:,self.dep - 1],cmap='gray')
                        self.fig_canvas_t1.draw()
                        print('f1')
                    except:
                        try:
                            self.dat,self.hei,self.wid,self.dep = file_actions.matrix_returner(name=name,path=name)
                            image_matrix = self.dat
                            self.current_medical_file = self.dat
                            self.current_medical_file_shape = self.current_medical_file.shape

                            self.axes_object_mrı_monitor[2].imshow(image_matrix[:,:,self.dep - 1],cmap='gray')
                            self.fig_canvas_t1.draw()
                            print('f1')
                        
                        except:
                            error_message = QMessageBox.critical(self,'İşlem yapılamadı!!',f'Lütfen Başka bir dosya seçin veya dosyanın düzgün olup olmadığını kontrol edin!')

                else:
                    try:
                        if path == 'Belirtilmedi':
                            try:
                                file_name = self.mri_list.item(self.mri_list.currentRow()).text().split('\n')[0].split(':')[1].strip()

                                image_matrix = image_processing.to_matrix(name)

                                self.axes_object_mrı_monitor[2].imshow(image_matrix,cmap='gray')
                                self.fig_canvas_t1.draw()
                                print('f1')
                            
                            except:
                                try:
                                    file_name = self.mri_list.item(self.mri_list.currentRow()).text().split('\n')[0].split(':')[1].strip()

                                    image_matrix = image_processing.to_matrix(path)
                                        
                                    self.axes_object_mrı_monitor[2].imshow(image_matrix,cmap='gray')
                                    self.fig_canvas_t1.draw()
                                    print('f1')
                                
                                except:
                                    error_message = QMessageBox.critical(self,'İşlem yapılamadı!!',f'Lütfen listeden bir mrı seçin!')
                

                        
                        else:
                            try:
                                file_name = self.mri_list.item(self.mri_list.currentRow()).text().split('\n')[0].split(':')[1].strip()

                                image_matrix = image_processing.to_matrix(name)
                                    
                                self.axes_object_mrı_monitor[2].imshow(image_matrix,cmap='gray')
                                self.fig_canvas_t1.draw()
                                print('f1')
                            except:
                                try:
                                    file_name = self.mri_list.item(self.mri_list.currentRow()).text().split('\n')[0].split(':')[1].strip()

                                    image_matrix = image_processing.to_matrix(path)
                                        
                                    self.axes_object_mrı_monitor[2].imshow(image_matrix,cmap='gray')
                                    self.fig_canvas_t1.draw()
                                    print('f1')
                                except:
                                    error_message = QMessageBox.critical(self,'İşlem yapılamadı!!',f'Lütfen listeden bir mrı seçin!')
                
                
                    except:
                        try:
                            if path.endswith('.nii') or self.current_selected.endswith('.nii.gz'):
                                warning_message = QMessageBox.warning(self,'Dosyan bulunamıyor','Sistem dosyayı bulamadı. Lütfen dosyayı manuel olarak Tekrar seçiniz!') 

                                current_url,string = QFileDialog(self).getOpenFileUrl(self)           
                    
                                self.dat,self.hei,self.wid,self.dep = file_actions.matrix_returner(name=name,path=path)
                                image_matrix = self.dat
                                self.current_medical_file = self.dat
                                self.current_medical_file_shape = self.current_medical_file.shape

                                self.axes_object_mrı_monitor[2].imshow(image_matrix[:,:,self.dep - 1],cmap='gray')
                                self.fig_canvas_t1.draw()
                                print('f2')
                            
                            else:
                                try:
                                    warning_message = QMessageBox.warning(self,'Dosyan bulunamıyor','Sistem dosyayı bulamadı. Lütfen dosyayı manuel olarak Tekrar seçiniz!') 

                                    current_url,string = QFileDialog(self).getOpenFileUrl(self)           
                        
                                    self.dat,self.hei,self.wid,self.dep = file_actions.matrix_returner(name=name,path=path)
                                    image_matrix = self.dat
                                    self.current_medical_file = self.dat
                                    self.current_medical_file_shape = self.current_medical_file.shape
                                        
                                    self.axes_object_mrı_monitor[2].imshow(image_matrix[:,:,self.dep - 1],cmap='gray')
                                    self.fig_canvas_t1.draw()
                                    print('f2')
                                except:
                                    pass

                        except:
                            try:
                                
                                warning_message = QMessageBox.warning(self,'Dosya bulunamıyor','Sistem dosyayı bulamadı. Lütfen dosyayı manuel olarak Tekrar seçiniz!') 

                                current_name = 'none'     

                                self.axes_object_mrı_monitor[2].imshow(image_matrix[:,:,self.dep - 1],cmap='gray')
                                self.fig_canvas_t1.draw()
                                
                                print('f3')
                            except:
                                print('noneeeee')


                
                    try:
                        self.dat,self.hei,self.wid,self.dep = file_actions.matrix_returner(name=name,path=path)
                        image_matrix = self.dat 
                        self.current_medical_file = self.dat
                        self.current_medical_file_shape = self.current_medical_file.shape

                        if image_matrix == None:
                            pass
                        
                        else:
                            self.axes_object_mrı_monitor[2].imshow(image_matrix[:,:,self.dep - 1],cmap='gray')
                            self.fig_canvas_t1.draw()
                            print('f4')
                    except:
                        print(path)
                        pass


def startGui():
    sp = QApplication(system._s.argv)
    sw = MainUİ()
    sw.show()
    system_scope = system.SystemActions().exit_gui_thread()

