from controller import *

if __name__ == '__main__':

    logger.info("test info")
    logger.warn("test warn")
    logger.error("test error")

    # override file
    file = open("tmp/recapFile.txt", "w+") 
    file.close()

    app.run(host='0.0.0.0', debug=True)