from display_trial import LSLApp

trials = [("UNI_LEFT", "LEFTHAND-TRAIN"), ("UNI_LEFT", "LEFTHAND-TEST"),
          ("UNI_LEFT", "RIGHTHAND-TRAIN"), ("UNI_LEFT", "RIGHTHAND-TEST"),
          ("BI-ONEHAND", "BIRECTION-1-TRAIN"), ("BI-ONEHAND", "BIRECTION-1-TEST"),
          ("BI-TWOHAND", "BIRECTION-2-TRAIN"), ("BI-TWOHAND", "BIRECTION-2-TEST")]

for trialtype, streamname in trials:
    input(f"Press any key to launch {streamname}: ")
    print(f"Launching! The LSL stream will be named {streamname}")
    app = LSLApp(trialtype, streamname)
    app.start()
