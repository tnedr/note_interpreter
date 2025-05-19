from note_interpreter.log import log

if __name__ == "__main__":
    log.debug("This is a DEBUG message (should be cyan)")
    log.info("This is an INFO message (should be green)")
    log.warning("This is a WARNING message (should be yellow)")
    log.error("This is an ERROR message (should be red)")
    log.print("This is a PRINT message (should be default terminal color)") 