# -*- mode: python -*-

block_cipher = None


a = Analysis(['isolate.py'],
             pathex=['/Users/Kevin/Downloads/PIETER_GIT/fk_git/fk'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='isolate',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='ico.icns')
app = BUNDLE(exe,
             name='isolate.app',
             icon='ico.icns',
             bundle_identifier=None)
