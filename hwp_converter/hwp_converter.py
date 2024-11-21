import os
import win32com.client as win32
import win32gui
import cv2

hwp_root = 'C:/Users/Darudayu/Desktop/hwp_1/asdfa'
hwp_list = os.listdir(hwp_root)
pdf_dest = 'C:/Users/Darudayu/Desktop/hwp_1/pdfs'
hwp = win32.Dispatch('HWPFrame.HwpObject')
print(hwp)
hwnd = win32gui.FindWindow(None, '빈 문서 1 - 한글')
print(hwnd)
win32gui.ShowWindow(hwnd, 0)
hwp.RegisterModule('FilePathCheckDLL', 'FilePathCheckerModule')

cnt = 0
for hwp_file in hwp_list[:10]:
    e1 = cv2.getTickCount()
    cnt += 1
    print(f'converting... {cnt}/{len(hwp_list)}')

    hwp.Open(f'{hwp_root}/{hwp_file}', Format='HWP', arg='')
    hwp.HAction.GetDefault('FileSaveAsPdf', hwp.HParameterSet.HFileOpenSave.HSet)
    hwp.HParameterSet.HFileOpenSave.filename = os.path.join(pdf_dest, hwp_file.replace('.hwp', '.pdf'))
    hwp.HParameterSet.HFileOpenSave.Format = 'PDF'
    hwp.HAction.Execute('FileSaveAsPdf', hwp.HParameterSet.HFileOpenSave.HSet)


    e2 = cv2.getTickCount()
print(f'Time taken: {(e2-e1)/cv2.getTickFrequency()} seconds')

hwp.Quit()
del hwp
del win32