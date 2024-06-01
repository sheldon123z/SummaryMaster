# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['summary_robot.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['builtins', '_ctypes', '_decimal', '_hashlib', '_lzma', '_ssl', '_zlib'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Summary Master',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['q.ico'],
)
app = BUNDLE(
    exe,
    name='Summary Master.app',
    icon='./q.ico',
    bundle_identifier=None,
)
