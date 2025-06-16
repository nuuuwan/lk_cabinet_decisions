if __name__ == "__main__":
    import sys

    from utils import Log

    from cabinet import Pipeline

    log = Log("Pipeline")

    if len(sys.argv) != 2:
        raise ValueError("python pipeline.py <max_n_hot>")

    max_n_hot = int(sys.argv[1])
    log.info(f"{max_n_hot=}")
    pipeline = Pipeline(do_shuffle=False)
    pipeline.run(max_n_hot)
