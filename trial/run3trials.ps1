echo "Launching Trial 1: UnilateralRight" "Connect EEG, open Lab Recorder, and wait for the stream TRIAL_OUTP_UNI_RIGHT..."


echo "Collecting first run..."
Start-Process powershell -WindowStyle maximized -ArgumentList  "cd C:\Users\desmo\Desktop\CARL\trial; python display_trial.py UNI_RIGHT"
Read-Host -Prompt "Press any key to launch next run(don't forget to record to a new .xdf!)"
echo "Collecting second run..."
Start-Process powershell.exe -ArgumentList  "cd C:\Users\desmo\Desktop\CARL\trial; python display_trial.py UNI_RIGHT"


Read-Host -Prompt "Press any key to launch Trial 2"
echo "Launching Trial 2: UnilateralLeft" "Connect EEG, open Lab Recorder, and wait for the stream TRIAL_OUTP_UNI_LEFT..."


echo "Collecting first run..."
Start-Process powershell -WindowStyle maximized -ArgumentList  "cd C:\Users\desmo\Desktop\CARL\trial; python display_trial.py UNI_LEFT"
Read-Host -Prompt "Press any key to launch next run (don't forget to record to a new .xdf!)"
echo "Collecting second run..."
Start-Process powershell.exe -ArgumentList  "cd C:\Users\desmo\Desktop\CARL\trial; python display_trial.py UNI_LEFT"

Read-Host -Prompt "Press any key to launch Trial 3"
echo "Launching Trial 3: Bilateral" "Connect EEG, open Lab Recorder, and wait for the stream TRIAL_OUTP_BI..."
echo "Collecting first run..."
Start-Process powershell.exe -ArgumentList  "cd C:\Users\desmo\Desktop\CARL\trial; python display_trial.py BI-ONEHAND"
Read-Host -Prompt "Press any key to launch next run (don't forget to record to a new .xdf!)"
echo "Collecting second run..."
Start-Process powershell.exe -ArgumentList  "cd C:\Users\desmo\Desktop\CARL\trial; python display_trial.py BI-ONEHAND"
echo "Experiment complete!"

Read-Host -Prompt "Press any key to launch trial 4"
echo "Launching Trial 4: Bilateral Two Hand" "Connect EEG, open Lab Recorder, and wait for the stream TRIAL_OUTP_BI..."
echo "Collecting first run..."
Start-Process powershell.exe -ArgumentList  "cd C:\Users\desmo\Desktop\CARL\trial; python display_trial.py BI-TWOHAND"
Read-Host -Prompt "Press any key to launch next run (don't forget to record to a new .xdf!)"
echo "Collecting second run..."
Start-Process powershell.exe -ArgumentList  "cd C:\Users\desmo\Desktop\CARL\trial; python display_trial.py BI-TWOHAND"
echo "Experiment complete!"