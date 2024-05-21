from strategy.context import MotorProcessor
from strategy.occ_mundial_strategy import OccMundialStrategy

job_title = "python"
job_location = "Mexico"
motor_url = "https://www.occ.com.mx"



occ_strategy = OccMundialStrategy(
    job_title=job_title,
    job_location=job_location
    )
motor_processor = MotorProcessor(strategy=occ_strategy, url=motor_url)
cards = motor_processor.search_job()
# motor_processor.create_excel(cards=cards)
# motor_processor.close_browser()
