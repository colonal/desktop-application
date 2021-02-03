def main():
    return"""
    QWidget {
        background-color:#262626;
        border: 1px solid #262626;
        color: #b3b3b3;
        }
    QMainWindow{
            background-color:#262626;
            border: 1px solid #262626;
            color: #b3b3b3;
        }
    /*# ################# */

    QGroupBox {
            padding-top: 10;
            background-color: #262626;
            font:15pt Time Bold;
            color: white;
            /*border:1px solid gray;
            border-radius:10px*/
        }
    /*# ################# */
    QProgressBar{
            border: 1px solid #bbb;
            background: white;
            height: 10px;
            border-radius: 6px;
        }
    /*# ################# */

    QTableWidget{
        background-color : #b3b3b3;
        color : #0d0d0d;
        font: 14px Time Bold;
    }
    QHeaderView::section {
        color:white;
        background-color:#232326; 
    }
    /*# ################# */

    QListWidget{
            background-color:#404040;
            border-radius: 3px;
            color :#bfbfbf;
            border: 1px solid #8c8c8c;
            font-size: 15px;
            text-align: center;
        }
    QListWidget::item:selected {
        color : #fff;
        background-color : hsl(0, 100%, 13%) ;
        border-radius: 5px;
        /*border : 3px solid hsl(0, 100%, 13%);*/
        }
    /*# ################# */
    
    QToolButton:hover {
            border: 0px solid red;
            padding-top: 3px;
            padding-right: 5px;
            padding-bottom: 3px;
            padding-left: 5px;
        }
    /*# ################# */

    QPushButton{
        color : #b3b3b3;
        font:14px Time;
        border: 1px solid #666;

        }
    QPushButton:hover {
        border: 2px solid #78879b;
        color: silver;
        }
    /*# ################# */

    QSlider::groove:horizontal {
            border: 1px solid #999999;
            height: 18px;

            border-radius: 9px;
            }

    QSlider::handle:horizontal {
            width: 18px;
            background-image: url(icons/slider4.png)
            }

    QSlider::add-page:qlineargradient {
            background: lightgrey;
            border-top-right-radius: 9px;
            border-bottom-right-radius: 9px;
            border-top-left-radius: 0px;
            border-bottom-left-radius: 0px;
            }

    QSlider::sub-page:qlineargradient {
            background: blue;
            border-top-right-radius: 0px;
            border-bottom-right-radius: 0px;
            border-top-left-radius: 9px;
            border-bottom-left-radius: 9px;
            }
    /*# ################# */

    QMenuBar{
        color : #bfbfbf;
        }
    QMenuBar::item {
            
        padding: 4px;
    }
    QMenuBar::item:selected {
        padding: 4px;
        color : #000;
        background: #bfbfbf;
        border: 0px solid #32414B;
    }
    QMenu::item {
        margin-top: 5px;
        margin-bottom: 5px;
        margin-right: 20px;
        margin-left: 20px;
        padding: 4px;
        color : #666666;
    }
    QMenu::item:selected {
        padding: 6px;
        color : #fff;
        background: #262626;
        border: 0px solid #32414B;
    }
    /*# ################# */

    QComboBox {
        background-color:#262626;
        color : #b3b3b3;
        font:14px Time;
        border: 1px solid #666;
    }

    QComboBox QAbstractItemView { 
        border: 1px solid #e0e6eb;
        border-radius: 1;
        padding: 1px;
        color : #b3b3b3;
        background-color: #262626;
        selection-background-color: #262626;
    }

    QComboBox QAbstractItemView:hover {      
        background-color: #595959;
        border: 1px solid #94a9b8;
        color: #fff;
    
    }

    QComboBox QAbstractItemView:selected {
        background: #eff2f6;
        color: #9cb3c9;
    }

    QComboBox QAbstractItemView:alternate {
        background: #ffffff;
    }



    QComboBox:hover {
        border: 2px solid #78879b;
        color: #1464A0;
    }

    QComboBox:on {
        color: #1464A0;
        selection-background-color: #1464A0;
    }

    QComboBox::item:checked {
        font-weight: bold;
    
    }

    QComboBox::item:selected {
        border: 1px solid transparent;
    
    }
    QComboBox::item:alternate {
        border: 1px solid transparent;
        padding: 6px;
    
    }

    /*# ################# *//*# ################# */
    QMessageBox {
        background-color:#262626;
        border: 1px solid #262626;
        color: #b3b3b3;
        }
    QMessageBox QPushButton{
        font:12px Time;
        padding: 5px 15px; 
        width: 100px;
        background-color:#262626;
        border: 1px solid #262626;
        color: #b3b3b3;
        }
    QMessageBox QPushButton:hover {
        border: 1px solid #78879b;
        border-bottom:2 solid red;
        color: silver;
        border-radius: 5px;
        }
    QMessageBox QLabel{
        color: #b3b3b3; 
        font-size: 13px;
        }
    """
def Slider():
    return"""
    QSlider::groove:horizontal {
            border: 0px solid #999999;
            height: 9px;

            border-radius: 2px;
            }

    QSlider::handle:horizontal {
            width: 10px;
            height: 10px;
            background-image: url(icons/slider6.png)
            }

    QSlider::add-page:qlineargradient {
            background: lightgrey;
            border-top-right-radius: 4px;
            border-bottom-right-radius: 4px;
            border-top-left-radius: 0px;
            border-bottom-left-radius: 0px;
            }

    QSlider::sub-page:qlineargradient {
            background: blue;
            border-top-right-radius: 0px;
            border-bottom-right-radius: 0px;
            border-top-left-radius: 4px;
            border-bottom-left-radius: 4px;
            }
    
    """

def QMessgesBox():
    return"""
    QMessageBox {
        background-color:#262626;
        border: 1px solid #262626;
        color: #b3b3b3;
        }
    QPushButton{
        font:12px Time;
        padding: 5px 15px; 
        width: 400px;
        background-color:#262626;
        border: 1px solid #262626;
        color: #b3b3b3;
        }
    QPushButton:hover {
        border: 1px solid #78879b;
        border-bottom:2 solid red;
        color: silver;
        border-radius: 5px;
        }
    QLabel{
        color: #b3b3b3; 
        font-size: 13px;
        }
    """