from loguru import logger


logg = logger
logg.add("logs.log", format="{time} | {level} | {message}", level="DEBUG")
