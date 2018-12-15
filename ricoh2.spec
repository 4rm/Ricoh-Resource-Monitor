# -*- mode: python -*-

block_cipher = None


a = Analysis(['ricoh2.py'],
             pathex=['C:\\Users\\Emilio\\Documents\\Schoolwork 16th Grade\\Ricoh Resource Reader\\ricohreader1214'],
             binaries=[],
             datas=[('.\\c3504ex.png','.'),('.\\c6004ex.png','.'),('.\\c6503.png','.'),('.\\c6503f.png','.'),('.\\icon.ico','.')],
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
          name='Ricoh Resource Monitor',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False,
		  icon='icon.ico'
			)
