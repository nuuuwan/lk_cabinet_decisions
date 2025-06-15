if __name__ == "__main__":
    import sys

    from utils import Log

    from cabinet import Pipeline

    log = Log("Pipeline")

    if len(sys.argv) != 2:
        raise ValueError("python pipeline.py <LIMIT>")

    LIMIT = int(sys.argv[1])
    log.info(f"{LIMIT=}")
    pipeline = Pipeline()
    pipeline.run(LIMIT)
