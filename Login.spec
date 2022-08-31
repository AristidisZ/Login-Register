# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


added_files = [
		 ( 'C:\\Users\\ARisss\\Desktop\\Main\\Login-Register\\data.db', '.'),
		 ( 'C:\\Users\\ARisss\\Desktop\\Main\\Login-Register\\Dialog_cart_order.ui', '.'),
		 ( 'C:\\Users\\ARisss\\Desktop\\Main\\Login-Register\\Dialog_employee.ui', '.'),
		 ( 'C:\\Users\\ARisss\\Desktop\\Main\\Login-Register\\Dialog_medication.ui', '.'),
		 ( 'C:\\Users\\ARisss\\Desktop\\Main\\Login-Register\\Dialog_orders.ui', '.'),
		 ( 'C:\\Users\\ARisss\\Desktop\\Main\\Login-Register\\Login.ui', '.'),
		 ( 'C:\\Users\\ARisss\\Desktop\\Main\\Login-Register\\Main_admin.ui', '.'),
		 ( 'C:\\Users\\ARisss\\Desktop\\Main\\Login-Register\\MainWindow_admin.ui', '.'),
		 ( 'C:\\Users\\ARisss\\Desktop\\Main\\Login-Register\\SignUp.ui', '.'),
		 ( 'C:\\Users\\ARisss\\Desktop\\Main\\Login-Register\\resources.qrc', '.'),
		 ]

a = Analysis(['Login.py'],
             pathex=['C:\\Users\\ARisss\\Desktop\\Main\\Login-Register'],
             binaries=[],
             datas=added_files,
             hiddenimports=['sip', 'PyQt5.Qsci', 'PyQt5'],
             hookspath=[],
             runtime_hooks=[],
             excludes=['tkinter', 'PyQt5.QtWebEngineWidgets'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='pharmacy',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon='pharmacy.ico')

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=['VCRUNTIME140.dll', 'MSVCP140.dll', 'qwindows.dll', 'qwindowsvistastyle.dll'],
               name='pharmacy')