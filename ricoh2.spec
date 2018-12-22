# -*- mode: python -*-

block_cipher = None


a = Analysis(['project-name.py'],
             pathex=['project-path'],
             binaries=[],
             datas=[('.\\c3504ex.png','.'),('.\\c6004ex.png','.'),('.\\c6503.png','.'),('.\\c6503f.png','.'),('.\\icon.ico','.'),('.\\link.ico','.')],
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
