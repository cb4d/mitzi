import logging

log = logging.getLogger()


def setup_log():
    global log
    log.setLevel(logging.DEBUG)

    # file logging
    fh = logging.FileHandler('/var/log/mitzi-snap.log')
    fh.setLevel(logging.DEBUG)

    # console logging
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the log
    log.addHandler(fh)
    log.addHandler(ch)
