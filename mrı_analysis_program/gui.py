from PyQt5.QtWidgets import*
from PyQt5.QtCore import*
from PyQt5.QtGui import*
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT  as NavigationToolbar

import system
import matplotlib.pyplot as plt
import image_processing

class MainUİ(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MGAA Medikal Görüntü Analiz Aracı')
        
        #layout-side#
        self.main_layout = QHBoxLayout()

        #widget-side#
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        
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
        
        #program-widget-side#
        self.mri_list = QListWidget()

        self.show_mri_image_button = QPushButton('Göster')
        self.add_mri_image_button = QPushButton('Ekle')
        self.save_mri_image_button = QPushButton('Kaydet')
        self.delete_mri_image_button = QPushButton('Sil')

        self.tumor_detection_checkbox = QCheckBox()
        self.bright_dimmer_checkbox = QCheckBox()
        self.normal_setting_checkbox = QCheckBox()
        self.checbox_apply_button = QPushButton(text='Uygula')
        self.checbox_reset_button = QPushButton(text='Sıfırla')
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

        self.sobel_val_slider = QSlider(Qt.Horizontal)

        self.gaussian_x_slider = QSlider(Qt.Horizontal)
        self.gaussian_y_slider = QSlider(Qt.Horizontal)
        self.gaussian_z_slider = QSlider(Qt.Horizontal)

        self.median_slider = QSlider(Qt.Horizontal)

        self.blur_slider = QSlider(Qt.Horizontal)

        fig,ax = plt.subplots(nrows=1,ncols=3,figsize=(14,4),facecolor='black')
        self.fig_canvas_t1 = FigureCanvas(figure=fig)
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

        self.defined_fig,self.defined_ax = plt.subplots(nrows=1,ncols=1,figsize=(5,4),facecolor='black')
        self.defined_ax.axis('off')
        self.defined_figurecanvas_object = FigureCanvas(self.defined_fig)
        self.defined_figurecanvas_object.setStyleSheet('border:1 px solid black')

        self.defined_ax.imshow(image_processing.to_matrix('t1.png'))

        self.t1_checkbox.setText('T1 MRI')
        self.t2_checkbox.setText('T2 MRI')
        self.flair_checkbox.setText('Flair MRI')

        #widget-parent-settings#
        icons = ['t1.png','t2.png','flair.png']

        for icon in icons:
            self.mri_list_item = QListWidgetItem(icon)
            self.mri_list_item.setIcon(QIcon(self.mri_list_item.text()))
            self.mri_list.setIconSize(QSize(64,64))
            self.mri_list.addItem(self.mri_list_item)

        self.main_layout.addWidget(self.monitor_splitter_container)

        self.depth_splitter.addWidget(self.depth_label)
        self.depth_splitter.addWidget(self.depth_slider)

        self.threshold_splitter.addWidget(self.threshold_label)
        self.threshold_splitter.addWidget(self.threshold_bins_slider)
        self.threshold_splitter.addWidget(self.threshold_maxval_slider)

        self.sobel_splitter.addWidget(self.sobel_label)
        self.sobel_splitter.addWidget(self.sobel_val_slider)

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
        self.mri_list_splitter.addWidget(self.add_mri_image_button)
        self.mri_list_splitter.addWidget(self.delete_mri_image_button)
        self.mri_list_splitter.addWidget(self.save_mri_image_button)

        self.mri_monitor_image_settings_splitter.addWidget(self.tumor_detection_checkbox)
        self.mri_monitor_image_settings_splitter.addWidget(self.bright_dimmer_checkbox)
        self.mri_monitor_image_settings_splitter.addWidget(self.normal_setting_checkbox)
        self.mri_monitor_image_settings_splitter.addWidget(self.checbox_apply_button)
        self.mri_monitor_image_settings_splitter.addWidget(self.checbox_reset_button)

        self.mri_monitor_view_settings_splitter_container.addWidget(self.gauss_splitter)
        self.mri_monitor_view_settings_splitter_container.addWidget(self.threshold_splitter)
        self.mri_monitor_view_settings_splitter_container.addWidget(self.edege_splitter)
        self.mri_monitor_view_settings_splitter_container.addWidget(self.sobel_splitter)
        self.mri_monitor_view_settings_splitter_container.addWidget(self.depth_splitter)
        self.mri_monitor_view_settings_splitter_container.addWidget(self.median_splitter)
        self.mri_monitor_view_settings_splitter_container.addWidget(self.blur_splitter)

        #self.file_system_splitter.addWidget(self.file_path)
        self.file_system_splitter.addWidget(self.folder_path)
        self.file_system_splitter.addWidget(self.tree_view)
        self.file_system_splitter.addWidget(self.define_folder_button)
        self.file_system_splitter.addWidget(self.define_file_button)
        self.file_system_splitter.addWidget(self.reset_path_button)

        self.mri_monitor_splitter.addWidget(self.custom_toolbar)
        self.mri_monitor_splitter.addWidget(self.fig_canvas_t1)
        self.mri_monitor_splitter.addWidget(self.mri_monitor_view_settings_splitter_container)

        self.image_selecter_splitter.addWidget(self.mrı_select_information)
        self.image_selecter_splitter.addWidget(self.t1_checkbox)
        self.image_selecter_splitter.addWidget(self.t2_checkbox)
        self.image_selecter_splitter.addWidget(self.flair_checkbox)

        self.cont_container = [QLabel(),QLabel(text='Tanımlanan görüntü')]

        for cont in range(len(self.cont_container)):
            self.cont_container[cont].setStyleSheet('border:none')
            self.cont_container[cont].setAlignment(Qt.AlignCenter)
            self.image_selecter_splitter.addWidget(self.cont_container[cont])
        self.image_selecter_splitter.addWidget(self.defined_figurecanvas_object)

        for a in range(len(ax)):
            ax[a].axis('off')
        
        ax[0].imshow(image_processing.to_matrix('t1.png'))
        ax[1].imshow(image_processing.to_matrix('t2.png'))
        ax[2].imshow(image_processing.to_matrix('flair.png'))

        ax[0].set_title('T1-MRI',color='white')
        ax[1].set_title('T2-MRI',color='white')
        ax[2].set_title('Flair-MRI',color='white')

        #timers-side#
        self.optimize_w_timer = QTimer(self)
        self.optimize_w_timer.start(10)
        self.optimize_w_timer.timeout.connect(self.optimize_widget_sizes)

        #signal-slot-side#
        self.define_folder_button.clicked.connect(self.define_folder)
        self.define_file_button.clicked.connect(self.define_file)

        #css-define-side#
        file = open(r'program_css.qss','r').read()
        self.setStyleSheet(str(file))

        self.setCentralWidget(self.main_widget)


    def optimize_widget_sizes(self):
        self.checbox_reset_button.setFixedHeight(self.save_mri_image_button.height())
        self.checbox_apply_button.setFixedHeight(self.save_mri_image_button.height())

    def define_folder(self):
        folder_path = self.folder_path.text()
        modelindex = self.file_system_model.setRootPath(folder_path)
        self.tree_view.setRootIndex(modelindex)

    def define_file(self):
        current_selected = self.file_system_model.filePath(self.tree_view.currentIndex())

        try:
            if current_selected.endswith('.nii') or current_selected.endswith('.dcm') or current_selected.endswith('.png') or current_selected.endswith('jpg'):
                print(current_selected)
                information_message = QMessageBox.information(self,'TANİMLAMA İSLEMİ BASARİLİ','Medikal goruntu dosyasi basari ile tanimlandi!')
            
                if current_selected.endswith('.png') or current_selected.endswith('.jpg'):
                    self.defined_ax.imshow(image_processing.to_matrix(current_selected))
                    self.defined_figurecanvas_object.draw()

            else:
                warnin_message = QMessageBox.warning(self,'TANİMLAMA İSLEMİ BASARİSİZ','Lütfen aşağıdaki belirtilen dosya uzantıları hariç bir dosyayı tanımlamaya çalışmayınız:\n\n.nii .dcm .png .jpg')
                
                    
        except Exception as exception_1:
            print(exception_1)

def startGui():
    sp = QApplication(system._s.argv)
    sw = MainUİ()
    sw.show()
    system_scope = system.SystemActions().exit_gui_thread()