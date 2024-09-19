from commons.loggerfactory import LoggerFactory
from commons.utils import resource_path

LoggerFactory(resource_path("logging.ini"))
logger = LoggerFactory.getLogger("main")

if __name__ == '__main__':
    logger.info("Starting gradio ui application ...")
    from scripts.bots.gradio_bot import GradioBot
    gradio_bot = GradioBot()
    gradio_bot.start()
