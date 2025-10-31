[app]
title = ELBASHA Downloader
package.name = elbasha
package.domain = org.elbasha

source.dir = .
source.include_exts = py,txt

version = 1.0

requirements = python3,kivy,yt-dlp,requests,certifi

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
