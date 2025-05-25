import sys, os
import threading
import markdown
import textwrap
from queue import Queue
from PySide6.QtWidgets import QApplication, QDialog, QTextEdit, QVBoxLayout
from PySide6.QtCore import QTimer
from dotenv import load_dotenv


from ui import MainWindow
import google.generativeai as genai

class Prompt:
    def __init__(self, data):
        self.data = data

    def get(self):
        if self.data["difficulty"] == "기초":
            return f"{self.data['department']} 분야에서 {self.data['selected_field']}와 관련된 탐구 내용 추천해줘."
        else:
            return f"{self.data['topic']}라는 주제에 대해서 {self.data['selected_field']} 분야, 그리고 {self.data['department']}와 관련있는 탐구 내용을 추천해줘. '{self.data['method']}'의 방법으로 할 수 있는 걸로 찾아줘."

def connect_ai():
    genai.configure(api_key=os.getenv("API_KEY"))
    return genai.GenerativeModel("gemini-2.0-flash")

def generate_answer(queue, model, prompt_text):
    if check_token():
        result = model.generate_content(prompt_text)
        queue.put(to_string(result.text))
    else:
        queue.put("API 키가 유효하지 않습니다.")

def to_string(answer):
    text = answer.replace("•", "* ")
    indented_text = textwrap.indent(text, "> ")
    return markdown.markdown(indented_text)

def check_token():
    return True

def get_data(data, model):
    prmpt = Prompt(data)
    result_queue = Queue()

    # 백그라운드 스레드에서 답변 생성
    t = threading.Thread(target=generate_answer, args=(result_queue, model, prmpt.get()), daemon=True)
    t.start()

    timer = QTimer()
    timer.setInterval(100)
    timer.timeout.connect(lambda: check_queue(result_queue, timer))
    timer.start()

def check_queue(result_queue, timer):
    if not result_queue.empty():
        result = result_queue.get()
        timer.stop()

        dialog = QDialog()
        dialog.setWindowTitle("결과")
        dialog.resize(1000, 700)

        layout = QVBoxLayout()
        result_view = QTextEdit()
        result_view.setReadOnly(True)
        result_view.setHtml(result)
        layout.addWidget(result_view)

        dialog.setLayout(layout)

        dialog.exec()

def main():
    load_dotenv()

    model = connect_ai()
    app = QApplication(sys.argv)

    window = MainWindow()
    window.selection_made.connect(lambda data: get_data(data, model))
    window.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()
