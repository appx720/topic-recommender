from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel,
    QRadioButton, QButtonGroup, QPushButton, QMessageBox, QSpacerItem, QSizePolicy
)
from PySide6.QtGui import QFontDatabase, QFont
from PySide6.QtCore import Signal


class MainWindow(QMainWindow):
    # Signal to notify the main application about the user's selection
    selection_made = Signal(dict)  # 데이터를 dict로 전달

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("주제 추천 프로그램")
        self.setFixedSize(600, 400)

        # Pretendard 폰트 로드
        font_id = QFontDatabase.addApplicationFont("Pretendard.ttf")
        font_families = QFontDatabase.applicationFontFamilies(font_id)

        if font_families:
            self.app_font = QFont(font_families[0])
        else:
            self.app_font = QFont("Arial")  # 대체 폰트

        # 메인 위젯 및 레이아웃 설정
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        main_widget.setLayout(main_layout)

        # 탐구 난이도 선택
        difficulty_label = QLabel("탐구 난이도를 선택하세요:")
        difficulty_label.setFont(self.app_font)
        main_layout.addWidget(difficulty_label)

        self.difficulty_buttons = QButtonGroup(self)
        difficulty_layout = QHBoxLayout()

        basic_button = QRadioButton("기초")
        basic_button.setFont(self.app_font)
        basic_button.setChecked(True)  # 기본값 설정
        basic_button.toggled.connect(self.update_ui_state)  # 상태 변경 시 호출
        self.difficulty_buttons.addButton(basic_button)
        difficulty_layout.addWidget(basic_button)

        advanced_button = QRadioButton("심화")
        advanced_button.setFont(self.app_font)
        self.difficulty_buttons.addButton(advanced_button)
        difficulty_layout.addWidget(advanced_button)

        main_layout.addLayout(difficulty_layout)

        # 주제 입력
        topic_label = QLabel("자신이 생각하고 있는 주제를 입력하세요:")
        topic_label.setFont(self.app_font)
        self.topic_label = topic_label  # 상태 변경을 위해 저장
        self.topic_input = QLineEdit()
        self.topic_input.setFont(self.app_font)
        self.topic_input.setPlaceholderText("주제를 입력하세요")
        self.topic_input.setFixedHeight(30)

        main_layout.addWidget(topic_label)
        main_layout.addWidget(self.topic_input)

        # 분야 입력
        field_label = QLabel("자신의 분야를 입력하세요:")
        field_label.setFont(self.app_font)
        self.field_input = QLineEdit()
        self.field_input.setFont(self.app_font)
        self.field_input.setPlaceholderText("분야를 입력하세요")
        self.field_input.setFixedHeight(30)

        main_layout.addWidget(field_label)
        main_layout.addWidget(self.field_input)

        # 분야 선택
        field_group_label = QLabel("1. 분야 지정:")
        field_group_label.setFont(self.app_font)
        main_layout.addWidget(field_group_label)

        self.field_buttons = QButtonGroup(self)
        field_layout = QHBoxLayout()

        for field in ["수학", "과학", "예술", "인문/사회", "공학", "생명"]:
            button = QRadioButton(field)
            button.setFont(self.app_font)
            self.field_buttons.addButton(button)
            field_layout.addWidget(button)

        main_layout.addLayout(field_layout)

        # 탐구 방법 선택
        method_group_label = QLabel("2. 탐구 방법 지정:")
        method_group_label.setFont(self.app_font)
        self.method_group_label = method_group_label  # 상태 변경을 위해 저장

        main_layout.addWidget(method_group_label)

        self.method_buttons = QButtonGroup(self)
        method_layout = QHBoxLayout()

        for method in ["문헌연구", "실험수행"]:
            button = QRadioButton(method)
            button.setFont(self.app_font)
            self.method_buttons.addButton(button)
            method_layout.addWidget(button)

        self.method_layout = method_layout  # 상태 변경을 위해 저장
        main_layout.addLayout(method_layout)

        # 주제 찾기 버튼
        self.search_button = QPushButton("주제 찾기")
        self.search_button.setFont(self.app_font)
        self.search_button.clicked.connect(self.emit_selection)  # Signal emit

        # 버튼 정렬 및 추가
        button_layout = QHBoxLayout()
        button_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        button_layout.addWidget(self.search_button)
        main_layout.addLayout(button_layout)

        # 초기 상태 업데이트
        self.update_ui_state()

    def update_ui_state(self):
        """Update UI components based on the selected difficulty."""
        is_basic = self.difficulty_buttons.checkedButton().text() == "기초"
        self.topic_label.setEnabled(not is_basic)
        self.topic_input.setEnabled(not is_basic)
        self.method_group_label.setEnabled(not is_basic)

        for button in self.method_buttons.buttons():
            button.setEnabled(not is_basic)

    def emit_selection(self):
        # Collect the input data
        topic = self.topic_input.text()
        field = self.field_input.text()
        selected_field = self.field_buttons.checkedButton()
        selected_method = self.method_buttons.checkedButton()
        selected_difficulty = self.difficulty_buttons.checkedButton()

        if not field or not selected_difficulty:
            QMessageBox.warning(self, "입력 오류", "모든 항목을 입력하고 선택해야 합니다.")
            return

        # 기초 탐구일 경우
        if selected_difficulty.text() == "기초":
            selection_data = {
                "topic": None,  # 기초 탐구는 주제 없이 추천
                "department": field,
                "selected_field": selected_field.text(),
                "difficulty": selected_difficulty.text(),
            }
        else:  # 심화 탐구일 경우
            if not topic or not selected_field or not selected_method:
                QMessageBox.warning(self, "입력 오류", "모든 항목을 입력하고 선택해야 합니다.")
                return

            selection_data = {
                "topic": topic,
                "department": field,
                "selected_field": selected_field.text(),
                "method": selected_method.text(),
                "difficulty": selected_difficulty.text(),
            }

        # Emit the selection data
        self.selection_made.emit(selection_data)
