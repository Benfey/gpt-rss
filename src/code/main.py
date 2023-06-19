from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextBrowser, QLineEdit, QFileDialog
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
import feedparser
import sys

class RSSReader(QWidget):
    def __init__(self):
        super().__init__()

        self.url_entry = QLineEdit(self)
        self.load_url_button = QPushButton('Load RSS from URL', self)
        self.load_file_button = QPushButton('Load RSS from File', self)
        self.text_browser = QTextBrowser(self)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.url_entry)
        self.layout.addWidget(self.load_url_button)
        self.layout.addWidget(self.load_file_button)
        self.layout.addWidget(self.text_browser)

        self.load_url_button.clicked.connect(self.load_rss_from_url)
        self.load_file_button.clicked.connect(self.load_rss_from_file)
        self.text_browser.anchorClicked.connect(QDesktopServices.openUrl)

    def parse_rss(self, rss_url):
        feed = feedparser.parse(rss_url)
        content = ""
        for post in feed.entries:
            content += "<h2>" + post.title + "</h2>"
            content += "<a href='" + post.link + "'>" + post.link + "</a>"
            content += "<p>" + post.description + "</p><hr>"
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
        rss_url = self.url_entry.text()
        content = self.parse_rss(rss_url)
        self.text_browser.setHtml(content)

app = QApplication(sys.argv)

rss_reader = RSSReader()
rss_reader.show()

sys.exit(app.exec_())
