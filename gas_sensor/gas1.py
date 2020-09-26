from mq import *
import sys, time
import pandas as pd
import datetime

try:
    print("Press CTRL+C to abort.")

    mq = MQ();
    while True:
        perc = mq.MQPercentage()
        sys.stdout.write("\r")
        sys.stdout.write("\033[K")
        sys.stdout.write("LPG: %g ppm, CO: %g ppm, Smoke: %g ppm" % (perc["GAS_LPG"], perc["CO"], perc["SMOKE"]))
        sys.stdout.flush()

        data = [[datetime.datetime.now(), perc["GAS_LPG"], perc["CO"], perc["SMOKE"]]]
        submission = pd.DataFrame(data)
        submission.to_csv('./GAS_DATASET.csv', header=False, mode='a', index=False)
        time.sleep(1)


except:
    print("\nAbort by user")