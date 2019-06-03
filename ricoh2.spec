# -*- mode: python -*-

block_cipher = None


a = Analysis(['RicohReader.py'],
             pathex=['C:\\Users\\...full_project_path'],
             binaries=[],
             datas=[('.\\images\\c3504ex.png','.'),('.\\images\\c6004ex.png','.'),('.\\images\\c6503.png','.'),('.\\images\\c6503f.png','.'),('.\\images\\icon.ico','.')],
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
		  Tree('.\\images',  prefix='images\\'),
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
		  icon='.\\images\\icon.ico'
			)
