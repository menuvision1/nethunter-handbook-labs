"""Create a non-installable ZIP for Chapter 31. Not a real signed APK."""
from pathlib import Path
import zipfile
MANIFEST='''<?xml version="1.0" encoding="utf-8"?>
<!-- Synthetic teaching XML; not an installable application. -->
<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="com.example.trainingapp">
  <uses-permission android:name="android.permission.INTERNET"/>
  <application android:debuggable="true">
    <activity android:name=".MainActivity" android:exported="true"/>
  </application>
</manifest>
'''
def create(path):
    with zipfile.ZipFile(path,'x') as z:
        z.writestr('AndroidManifest.xml',MANIFEST)
        z.writestr('classes.dex','NOT REAL DEX: teaching placeholder')
        z.writestr('META-INF/CERT.RSA','NOT A CERTIFICATE OR SIGNATURE')
        z.writestr('res/strings.txt','app_name=Training App\n')
if __name__=='__main__':
    create(Path('sample-training.apk'))
    print('Created synthetic non-installable sample-training.apk')
