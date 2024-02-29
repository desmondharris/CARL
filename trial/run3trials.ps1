echo "Launching Trial 1: UnilateralRight" "Connect EEG, open Lab Recorder, and wait for the stream TRIAL_OUTP_UNI_RIGHT..."
echo "NOTE: Script sleeping for 5 seconds"
sleep 5
echo "Collecting first run..."
Start-Process powershell -WindowStyle maximized -ArgumentList  "cd C:\Users\desmo\Desktop\CARL\trial; python display_trial.py UNI_RIGHT"
Read-Host -Prompt "Press any key to launch next run(don't forget to record to a new .xdf!)"
echo "Collecting second run..."
Start-Process powershell.exe -ArgumentList  "cd C:\Users\desmo\Desktop\CARL\trial; python display_trial.py UNI_RIGHT"


Read-Host -Prompt "Press any key to launch Trial 2"
echo "Launching Trial 2: UnilateralLeft" "Connect EEG, open Lab Recorder, and wait for the stream TRIAL_OUTP_UNI_LEFT..."
echo "NOTE: Script sleeping for 5 seconds"
sleep 5
echo "Collecting first run..."
Start-Process powershell -WindowStyle maximized -ArgumentList  "cd C:\Users\desmo\Desktop\CARL\trial; python display_trial.py UNI_LEFT"
Read-Host -Prompt "Press any key to launch next run (don't forget to record to a new .xdf!)"
echo "Collecting second run..."
Start-Process powershell.exe -ArgumentList  "cd C:\Users\desmo\Desktop\CARL\trial; python display_trial.py UNI_LEFT"

Read-Host -Prompt "Press any key to launch Trial 3"
echo "Launching Trial 3: Bilateral" "Connect EEG, open Lab Recorder, and wait for the stream TRIAL_OUTP_BI..."
echo "NOTE: Script sleeping for 5 seconds"
sleep 5
echo "Collecting first run..."
Start-Process powershell -WindowStyle maximized -ArgumentList  "cd C:\Users\desmo\Desktop\CARL\trial; python display_trial.py BI"
Read-Host -Prompt "Press any key to launch next run (don't forget to record to a new .xdf!)"
echo "Collecting second run..."
Start-Process powershell.exe -ArgumentList  "cd C:\Users\desmo\Desktop\CARL\trial; python display_trial.py BI"