# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['proxybeuker.py'],
             pathex=['/Users/pieter/Downloads/CODE_PROJECTS/ProxyBeuker/proxybeuker'],
             binaries=[],
             datas=[('ico.ico','.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='proxybeuker',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='ico.icns')
app = BUNDLE(exe,
             name='proxybeuker.app',
             icon='ico.icns',
             bundle_identifier=None,
             info_plist={
    'NSPrincipleClass': 'NSApplication',
    'NSAppleScriptEnabled': False,
    'NSHighResolutionCapable': 'True'
     })


