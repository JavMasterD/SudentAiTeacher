#
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTextEdit, QPushButton, QVBoxLayout
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt

from search_engine import load_book

class StudentsAiTeacher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("مساعد العلوم - المرحلة الإعدادية")
        self.setGeometry(100, 100, 700, 500)
        self.setup_ui()
        self.book_data = load_book()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("🤖 مساعد العلوم الذكي")
        title.setFont(QFont("Arial", 20))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        self.input = QTextEdit()
        self.input.setFont(QFont("Arial", 14))
        self.input.setPlaceholderText("اكتب سؤالك هنا...")
        layout.addWidget(self.input)

        self.button = QPushButton("🔍 بحث")
        self.button.setFont(QFont("Arial", 14))
        self.button.clicked.connect(self.handle_search)
        layout.addWidget(self.button)

        self.output = QTextEdit()
        self.output.setFont(QFont("Arial", 14))
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        # ألوان خلفية مبهجة
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#E8F5E9"))
        self.setPalette(palette)

        self.setLayout(layout)

    def handle_search(self):
        question = self.input.toPlainText().strip()
        results = []

        # حالة: تعريف
        if question.startswith("ما هو") or "تعريف" in question:
            for lesson in self.book_data:
                for definition in lesson.get("definitions", []):
                    if definition["term"] in question:
                        results.append({
                            "title": lesson["title"],
                            "text": f"{definition['term']}: {definition['definition']}"
                        })

        # حالة: مقارنة
        elif "الفرق بين" in question or "قارن بين" in question:
            for lesson in self.book_data:
                for comparison in lesson.get("comparisons", []):
                    if all(term in question for term in comparison["between"]):
                        results.append({
                            "title": lesson["title"],
                            "text": comparison["difference"]
                        })

        # حالة: أسئلة نموذجية
        else:
            for lesson in self.book_data:
                for qa in lesson.get("questions", []):
                    if question in qa["q"]:
                        results.append({
                            "title": lesson["title"],
                            "text": f"{qa['q']}\nالإجابة: {qa['a']}"
                        })

        # fallback: بحث عام في content
        if not results:
            for lesson in self.book_data:
                for paragraph in lesson.get("content", []):
                    if any(word in paragraph for word in question.split()):
                        results.append({
                            "title": lesson["title"],
                            "text": paragraph
                        })

        # عرض النتائج
        if results:
            final_text = "\n\n".join([f"📘 {r['title']}\n{r['text']}" for r in results])
        else:
            final_text = "لم أتمكن من العثور على إجابة دقيقة لهذا السؤال."

        self.output.setText(final_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentsAiTeacher()
    window.show()
    sys.exit(app.exec_())
