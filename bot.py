
if __name__ == '__main__':
    print("Starting gradio ui application ...")
    from scripts.bots.gradio_bot import GradioBot
    gradio_bot = GradioBot()
    gradio_bot.start()
