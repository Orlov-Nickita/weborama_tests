import sys
import warnings
from collections import defaultdict
from typing import Dict
from ebooklib import epub
from bs4 import BeautifulSoup
from loguru import logger

warnings.filterwarnings('ignore', message='In the future version')


class BookParser:
    """
    Класс для работы с парсингом книг epub и fb2
    """
    def __init__(self, file_path):
        self.file_path: str = file_path

    def extract_info_from_epub(self) -> Dict[str, str]:
        """
        Извлекает данные из книги формата epub
        :return: Dict
        """
        book_info = defaultdict()
        needed_column = ['title', 'creator', 'publisher', 'date']
        book = epub.read_epub(self.file_path)
        for i in book.metadata:
            for j in book.metadata[i]:
                if j in needed_column:
                    book_info[j] = book.metadata[i][j][0][0]
        return book_info

    def extract_info_from_fb2(self) -> Dict[str, str]:
        """
        Извлекает данные из книги формата fb2
        :return: Dict
        """
        book_info = defaultdict()
        with open(self.file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        soup = BeautifulSoup(content, 'xml')
        book_info['title'] = soup.find(name='book-title').text
        book_info['author'] = soup.find(name='author').text.strip()
        book_info['year'] = soup.find(name='date').text
        book_info['publisher'] = soup.find(name='publish-info').text
        return book_info

    def get_book_info(self) -> Dict[str, str]:
        """
        Главная функция по парсингу книги
        :return: Dict
        """
        if self.file_path.endswith('.epub'):
            book_information: Dict = self.extract_info_from_epub()
        elif self.file_path.endswith('.fb2'):
            book_information: Dict = self.extract_info_from_fb2()
        else:
            logger.error("Unsupported file format")
            book_information: Dict = {}
        return book_information


if __name__ == '__main__':
    if len(sys.argv) > 1:
        book_parser = BookParser(file_path=sys.argv[1])
        bookinfo = book_parser.get_book_info()
        logger.info(bookinfo)
    else:
        logger.error("Укажите путь к файлу в качестве аргумента командной строки")
