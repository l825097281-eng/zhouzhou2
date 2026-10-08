[app]

title = 舟舟算价助手
package.name = zhouzhou_price
package.domain = org.zhouzhou
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

requirements = python3,kivy

fullscreen = 0
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.orientation = portrait
android.debug = 0
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 0
build_dir = .buildozer
bin_dir = bin
