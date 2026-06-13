[app]

title = Sovereign AI
package.name = sovereignai
package.domain = org.logic
source.dir = .
source.include_exts = py,png,jpg,json,txt
version = 1.0
requirements = python3,kivy==2.3.0
orientation = portrait
fullscreen = 1
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.api = 34
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a
android.enable_androidx = True
android.accept_sdk_license = True

[buildozer]
log_level = 2
show_progress = 1
