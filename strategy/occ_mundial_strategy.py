import difflib
import os
import re
import time
from datetime import datetime

import openpyxl
import openpyxl.styles
import openpyxl.utils
import openpyxl.worksheet
import openpyxl.worksheet.dimensions
import pandas as pd
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from strategy.strategy import SearchingMotor


class OccMundialStrategy(SearchingMotor):
    """Strategy for find job in OCCMundial."""
    max_similarity = 0
    most_similar_suggestion = None
    MOST_SIMILAR_SUGGESTION = None

    def __init__(self, job_title: str, job_location: str) -> None:
        self.job_title = job_title
        self.job_location = job_location
        # self.browser = None
        self.excel_name = f"OCC {datetime.now()}"


    def get_browser(self, url: str):
        """Request to URL"""


    def find_job(self, url):
        """search job in occ page"""
        self.browser = super().create_browser()
        self.browser.get(url)
        position_input = self.browser.find_element(
            By.CSS_SELECTOR, '[data-testid="search-box-keyword"]'
            ).send_keys(self.job_title)
        location_input = self.browser.find_element(
            By.CSS_SELECTOR, '[data-testid="search-box-location"]')
        location_input.send_keys(self.job_location)
        try:
            suggestions_container = WebDriverWait(self.browser, 20).until(
                                expected_conditions.visibility_of_element_located(
                                    (By.CSS_SELECTOR, '.absolute.w-full.bg-white.top-full'))
                                    )
        except TimeoutException as exc:
            raise ValueError("No valid location, try it again.") from exc

        suggestions_elements = suggestions_container.find_elements(
                        By.CSS_SELECTOR, 'ul > li > span.text-base.text-blueCorp-600.leading-6')
        # suggestions_list = [sug_elem.text for sug_elem in suggestions_elements]
        for suggestion_element in suggestions_elements:
            suggestion_text = suggestion_element.text
            similarity = difflib.SequenceMatcher(None, self.job_location.lower(), suggestion_text.lower()).ratio()
            if similarity > self.max_similarity:
                self.max_similarity = similarity
                self.most_similar_suggestion = suggestion_element
        # Si se encuentra la sugerencia más similar, haz clic en ella
        self.most_similar_suggestion.click()

        find_button = self.browser.find_element(By.CSS_SELECTOR, '[data-testid="search-box-submit"]')
        find_button.click()

        order_by = WebDriverWait(self.browser, 5).until(
            expected_conditions.visibility_of_element_located((By.ID, 'sort-jobs')))
        order_by.click()
        date_order_button = WebDriverWait(self.browser, 5).until(
            expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="sort-jobs"]/div[2]/div/div[2]/p')))
        date_order_button.click()

        job_cards = WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_all_elements_located(
                (By.XPATH, '//*[starts-with(@id, "jobcard-")]')))
        # return job_cards


    # def create_excel(self, element):
        df = pd.DataFrame()
        for card in job_cards:
            card.click()

            # Data extraction
            job_card = WebDriverWait(self.browser, 7).until(
                expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, '.px-8.py-6.bg-white.rounded-card'))
            )
            title_element = job_card.find_element(By.CSS_SELECTOR, '.flex.justify-between.items-start.mt-2')

            details_elements = WebDriverWait(job_card.find_element(By.CSS_SELECTOR, '.text-lg.mb-4'), 7).until(
                expected_conditions.visibility_of_all_elements_located(
                    (By.XPATH,
                    "./following-sibling::div[contains(@class, 'mb-1') \
                    and not(contains(@class, 'border-t border-[#e4edff]'))]"))
                    )
            details_text = "\n".join([elem.text.replace('\n', ' ').replace(',', "\n") for elem in details_elements])

            url_to_apply = self.browser.current_url

            description_element = job_card.find_element(By.CSS_SELECTOR, '.mb-8.break-words')
            description_text = re.sub(fr'{re.escape("Descripción")}:?', '', description_element.text)

            # Data assignation
            temporal_df = pd.DataFrame({"Title": [title_element.text],
                                        "Description": [description_text],
                                        "Details": [details_text],
                                        "Vacant": [url_to_apply]})

            df = pd.concat([df, temporal_df], ignore_index=True)
        # export excel
        df.to_excel(self.excel_name, sheet_name=self.excel_name)


    # def customize_excel(self, excel):
        wb = openpyxl.load_workbook(f"{self.excel_name}.xlsx")
        ws = wb[self.excel_name]

        # Ajustar automáticamente el ancho de las columnas
        for column_cells in ws.columns:
            length = max(len(str(cell.value)) for cell in column_cells)
            adjusted_width = (length + 2) * 1.2  # Ajustar el ancho de la columna
            column_index = column_cells[0].column
            column_dimension = openpyxl.worksheet.dimensions.ColumnDimension(
                ws,
                min=column_index,
                max=column_index,
                width=adjusted_width
                )
            ws.column_dimensions[column_index] = column_dimension

        # Ajustar altura de filas
        for row in ws.iter_rows():
            for cell in row:
                if cell.value:
                    lines = str(cell.value).split('\n')
                    max_height = max(len(line) for line in lines)
                    adjusted_height = max_height * 0.75  # Ajustar la altura de la fila
                    cell.alignment = openpyxl.styles.Alignment(wrapText=True)
                    # cell.alignment.wrap_text = True
                    ws.row_dimensions[cell.row].height = adjusted_height


        # Guardar los cambios en el archivo Excel
        wb.save(f"{self.excel_name}.xlsx")
        os.system(f"open {self.excel_name}.xlsx")


    def close_browser(self):
        self.browser.close()


    def create_excel(self, element):
        return super().create_excel(element)
    
    def customize_excel(self, excel):
        return super().customize_excel(excel)