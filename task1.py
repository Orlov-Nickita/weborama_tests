from typing import Dict, List
from loguru import logger
import pandas as pd
from pandas.core.series import Series
from pandas.core.frame import DataFrame


class CSVParser:
    """
    Класс для работы с парсингом csv файлов
    """
    def __init__(self, csv_file):
        self.csv_file: DataFrame = pd.read_csv(csv_file)

    def get_ids_series(self) -> Series:
        """
        Получаем серию из id и количества уникальных значений в этом столбце
        """
        return self.csv_file['id'].value_counts()

    def get_ids_with_3_occurrences(self) -> List[int]:
        """
        Получаем список значений id, которые встречаются 3 раза
        """
        ids_series = self.get_ids_series()
        return ids_series[ids_series == 3].index.to_list()

    def get_occurrence_counts_desc(self) -> Dict[int, int]:
        """
        Получаем словарь с частотностью значений id
        """
        ids_series = self.get_ids_series()
        return ids_series.value_counts().to_dict()


csv_parser = CSVParser(csv_file='table.csv')

logger.debug("ID, встречающиеся 3 раза:")
logger.info(csv_parser.get_ids_with_3_occurrences())
logger.debug("Частота повторений ID (Частота - Количество):")
logger.info(csv_parser.get_occurrence_counts_desc())
