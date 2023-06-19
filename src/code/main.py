from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextBrowser, QLineEdit, QFileDialog, QProgressBar, QComboBox
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QDesktopServices
import feedparser
import sys

class RSSReader(QWidget):
    def __init__(self):
        super().__init__()

        self.url_entry = QComboBox(self)
        self.url_entry.setEditable(True)
        self.load_url_button = QPushButton('Load RSS from URL', self)
        self.refresh_button = QPushButton('Refresh', self)
        self.load_file_button = QPushButton('Load RSS from File', self)
        self.text_browser = QTextBrowser(self)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 0)
        self.progress_bar.hide()

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.url_entry)
        self.layout.addWidget(self.load_url_button)
        self.layout.addWidget(self.refresh_button)
        self.layout.addWidget(self.load_file_button)
        self.layout.addWidget(self.text_browser)
        self.layout.addWidget(self.progress_bar)

        self.load_url_button.clicked.connect(self.load_rss_from_url)
        self.refresh_button.clicked.connect(self.refresh_rss)
        self.load_file_button.clicked.connect(self.load_rss_from_file)
        self.text_browser.anchorClicked.connect(QDesktopServices.openUrl)

        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #b3b3b3;
            }
            QLineEdit, QTextBrowser {
                background-color: #323232;
                color: #b3b3b3;
            }
            QPushButton {
                background-color: #3a3a3a;
                color: #b3b3b3;
            }
            QPushButton:hover {
                background-color: #484848;
            }
            QTextBrowser {
                color: #b3b3b3;
            }
            QTextBrowser a {
                color: #ffffff;
                text-decoration: underline;
                font-weight: bold;
            }
        """)


    def parse_rss(self, rss_url):
        feed = feedparser.parse(rss_url)
        content = ""
        for post in feed.entries:
            content += "<h2>" + post.title + "</h2>"
            content += "<a href='" + post.link + "' style='color: #ffffff; text-decoration: underline; font-weight: bold;'>" + post.link + "</a>"
            content += "<p>" + post.description + "</p><hr>"
        # Add a CSS rule to the HTML to set the color of all links to white
        content = "<style>a { color: #ffffff; text-decoration: underline; font-weight: bold; }</style>" + content
        return content

    def load_rss_from_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open file', '')
        if file_path:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                content = ""
                for line in lines:
                    content += self.parse_rss(line.strip())
                self.text_browser.setHtml(content)

    def load_rss_from_url(self):
        rss_url = self.url_entry.currentText()
        if rss_url:
            self.progress_bar.show()
            content = self.parse_rss(rss_url)
            self.text_browser.setHtml(content)
            self.progress_bar.hide()
            if self.url_entry.findText(rss_url) == -1:
                self.url_entry.addItem(rss_url)

    def refresh_rss(self):
        self.load_rss_from_url()

app = QApplication(sys.argv)

rss_reader = RSSReader()
rss_reader.resize(1920, 1080)  # Set the default size to 1920x1080
rss_reader.show()

sys.exit(app.exec_())
