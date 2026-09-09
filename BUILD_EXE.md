# TAG2.GG Tracker EXE 빌드 방법

이 문서는 Windows에서 `TAG2GGTracker.exe`를 다시 만드는 방법을 설명한다.

## 1. 필요한 파일

다음 파일을 같은 폴더에 둔다.

```text
C:\1\ttt2_tracker\
├─ tracker.py
├─ gui_launcher.py
├─ TTT2TrackerGUI.spec
├─ version_info.txt
├─ app-icon.svg
├─ app-icon-192.png
├─ app-icon-256.png
├─ app-icon-512.png
└─ app-icon.ico
```

`tracker.py`는 실제 RPCS3 메모리 감시 및 Supabase 업로드 코드이고,
`gui_launcher.py`는 콘솔창 없이 안내 화면을 표시하는 GUI 시작 파일이다.

## 2. Python 확인

PowerShell에서 다음 명령을 실행한다.

```powershell
python --version
```

Python이 설치되어 있지 않다면 Python을 먼저 설치한다.

## 3. 필요한 패키지 설치

다음 명령을 실행한다.

```powershell
python -m pip install Pillow
python -m pip install cairosvg
```

`cairosvg`가 Windows에서 Cairo DLL 오류를 내는 경우에는 아이콘 생성 단계에서
아래의 Pillow 방식으로 생성할 수 있으므로 빌드 자체에는 문제가 없다.

PyInstaller가 설치되어 있는지 확인한다.

```powershell
python -c "import importlib.util; print('PyInstaller available' if importlib.util.find_spec('PyInstaller') else 'PyInstaller missing')"
```

없으면 설치한다.

```powershell
python -m pip install pyinstaller
```

## 4. 웹사이트 아이콘 복사

웹사이트의 SVG 아이콘을 tracker 폴더에 복사한다.

```powershell
Copy-Item -LiteralPath C:\1\ttt2_web\assets\app-icon.svg -Destination C:\1\ttt2_tracker\app-icon.svg -Force
Copy-Item -LiteralPath C:\1\ttt2_web\assets\app-icon-192.png -Destination C:\1\ttt2_tracker\app-icon-192.png -Force
Copy-Item -LiteralPath C:\1\ttt2_web\assets\app-icon-512.png -Destination C:\1\ttt2_tracker\app-icon-512.png -Force
```

## 5. 아이콘 생성

아래 명령은 `TAG2.GG`가 표시된 PNG와 Windows용 ICO를 생성한다.

```powershell
@'
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

font_path = r'C:\Windows\Fonts\arialbi.ttf'

def render(size, path):
    scale = size / 512
    image = Image.new('RGBA', (size, size), '#0c0a18')
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle(
        (24*scale, 24*scale, 488*scale, 488*scale),
        radius=76*scale,
        fill='#17152b',
        outline='#5b8cff',
        width=max(1, round(12*scale))
    )
    font = ImageFont.truetype(font_path, round(86*scale))
    text = 'TAG2.GG'
    box = draw.textbbox((0, 0), text, font=font)
    x = (size - (box[2]-box[0])) / 2 - box[0]
    y = 270*scale - (box[3]-box[1]) / 2 - box[1]
    draw.text((x, y), text, font=font, fill='#f4f0ff')
    r = 27*scale
    cx, cy = 414*scale, 408*scale
    draw.ellipse((cx-r, cy-r, cx+r, cy+r), fill='#ff3f73')
    image.save(path)

web = Path(r'C:\1\ttt2_web\assets')
tracker = Path(r'C:\1\ttt2_tracker')

render(192, web / 'app-icon-192.png')
render(512, web / 'app-icon-512.png')
render(192, tracker / 'app-icon-192.png')
render(512, tracker / 'app-icon-512.png')

Image.open(tracker / 'app-icon-512.png').save(
    tracker / 'app-icon.ico',
    sizes=[(16,16), (24,24), (32,32), (48,48),
           (64,64), (128,128), (256,256)]
)
print('icons generated')
'@ | python -
```

tracker 폴더에 intermediate GUI 리소스도 만든다.

```powershell
@'
from PIL import Image

source = Image.open(r'C:\1\ttt2_tracker\app-icon-512.png')
source.resize((256, 256), Image.Resampling.LANCZOS).save(
    r'C:\1\ttt2_tracker\app-icon-256.png'
)
'@ | python -
```

## 6. EXE 메타데이터

`version_info.txt`에 다음 정보를 넣는다.

```text
Product name: TAG2.GG Tracker
Product version: 0.1.0
File version: 0.1.0.0
Author: legbreaker
Copyright: Copyright (C) 2026 legbreaker
Company name: 공란
File description: TAG2.GG online match tracker
```

PyInstaller가 읽는 실제 `version_info.txt` 형식은 다음과 같다.

```python
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(0, 1, 0, 0),
    prodvers=(0, 1, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          '040904B0',
          [
            StringStruct('CompanyName', ''),
            StringStruct('FileDescription', 'TAG2.GG online match tracker'),
            StringStruct('FileVersion', '0.1.0.0'),
            StringStruct('InternalName', 'TAG2GGTracker'),
            StringStruct('LegalCopyright', 'Copyright (C) 2026 legbreaker'),
            StringStruct('OriginalFilename', 'TAG2GGTracker.exe'),
            StringStruct('ProductName', 'TAG2.GG Tracker'),
            StringStruct('ProductVersion', '0.1.0'),
            StringStruct('Author', 'legbreaker'),
          ]
        )
      ]
    ),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
```

## 7. PyInstaller spec 확인

`TTT2TrackerGUI.spec`는 다음 조건을 포함해야 한다.

```python
a = Analysis(
    ['gui_launcher.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('app-icon-192.png', '.'),
        ('app-icon-256.png', '.'),
        ('app-icon.svg', '.'),
    ],
    hiddenimports=[],
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
    name='TAG2GGTracker',
    icon='app-icon.ico',
    version='version_info.txt',
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
)
```

`console=False`가 CMD 창을 숨기는 핵심 옵션이다.

## 8. 빌드 전 기존 실행 파일 종료

기존 EXE가 실행 중이면 덮어쓰기에 실패할 수 있다.

```powershell
Get-Process -Name TAG2GGTracker -ErrorAction SilentlyContinue |
  ForEach-Object { Stop-Process -Id $_.Id }
```

빌드 spec의 아이콘/데이터 파일 경로가 상대 경로이므로 tracker 폴더에서 빌드한다.

```powershell
Set-Location C:\1\ttt2_tracker
```

## 9. 문법 검사

```powershell
python -m py_compile C:\1\ttt2_tracker\gui_launcher.py C:\1\ttt2_tracker\tracker.py
```

오류가 없으면 다음 빌드 단계로 진행한다.

## 10. EXE 빌드

```powershell
python -m PyInstaller --clean --noconfirm C:\1\ttt2_tracker\TTT2TrackerGUI.spec
```

빌드가 성공하면 결과 파일은 다음 위치에 생성된다.

```text
C:\1\dist\TAG2GGTracker.exe
```

## 11. 빌드 결과 확인

Windows 파일 속성에 들어가기 전에 PowerShell에서 메타데이터를 확인할 수 있다.

```powershell
$v = (Get-Item C:\1\dist\TAG2GGTracker.exe).VersionInfo
$v | Select-Object `
  FileDescription,
  ProductName,
  ProductVersion,
  FileVersion,
  CompanyName,
  LegalCopyright,
  OriginalFilename
```

예상 결과:

```text
FileDescription  : TAG2.GG online match tracker
ProductName      : TAG2.GG Tracker
ProductVersion   : 0.1.0
FileVersion      : 0.1.0.0
CompanyName      :
LegalCopyright   : Copyright (C) 2026 legbreaker
OriginalFilename : TAG2GGTracker.exe
```

## 12. 실행 테스트

```powershell
$p = Start-Process -FilePath C:\1\dist\TAG2GGTracker.exe -PassThru
Start-Sleep -Seconds 2
Get-Process -Id $p.Id | Select-Object Id,ProcessName,Responding
Stop-Process -Id $p.Id
```

`Responding`이 `True`이면 GUI가 정상적으로 열렸다는 뜻이다.

## 13. 배포 시 주의사항

- 사용자의 컴퓨터에는 Python을 설치할 필요가 없다.
- 사용자의 컴퓨터에는 PyInstaller를 설치할 필요가 없다.
- RPCS3와 Tekken Tag Tournament 2는 사용자의 컴퓨터에 설치되어 있어야 한다.
- EXE는 RPCS3가 실행 중일 때 메모리를 읽는다.
- Windows Defender가 처음 실행을 경고할 수 있다.
- EXE를 배포하기 전에 Supabase 키가 포함된 코드가 공개되어도 괜찮은지 확인한다.
