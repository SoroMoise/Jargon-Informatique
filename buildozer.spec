[app]

# (str) Title of your application
title = Jargon Informatique

# (str) Package name
package.name = jargoninformatique

# (str) Package domain (needed for android/ios packaging)
package.domain = org.jargoninformatique

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ico,sqlite

# (list) List of inclusions using pattern matching
#source.include_patterns = libs/*,images/*.png,src/images/*,src/base_de_donner/*

# (list) Source files to exclude (let empty to not exclude anything)
source.exclude_exts = spec, spec~

# (list) List of directory to exclude (let empty to not exclude anything)
source.exclude_dirs = tests, bin,.buildozer,test,.idea

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 1.5


# (list) Application requirements
requirements = python3,kivy,kivymd,sqlite3,Pillow

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
#requirements.source.PIL = ../../kivy

# (list) Garden requirements
#garden_requirements =

# (str) Presplash of the application
presplash.filename = %(source.dir)s/src/images/logo.ico

# (str) Icon of the application
icon.filename = %(source.dir)s/src/images/logo.ico

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

### Android specific ###

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (for new android toolchain)
android.presplash_color = #FFFFFF

# (list) Permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE

### (int) Target Android API, should be as high as possible.
android.api = 27

# (int) Minimum API your APK will support.
#android.minapi = 21

# (int) Android SDK version to use
#android.sdk = 20

# (str) Android NDK version to use
#android.ndk = 19b

# (int) Android NDK API to use. This is the minimum API your app will support, it should usually match android.minapi.
#android.ndk_api = 21

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

## (str) Android NDK directory (if empty, it will be automatically downloaded.)
##android.ndk_path =

## (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk_path =

## (str) ANT directory (if empty, it will be automatically downloaded.)
#android.ant_path =

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess Internet downloads or save time
# when an update is due and you just want to test/build your package
android.skip_update = True

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.arch = armeabi-v7a

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
