import os
import win32com.client as win32
import win32gui
import cv2

hwp_root = 'C:/Users/Darudayu/Desktop/hwp_1/hwp_1'
hwp_list = os.listdir(hwp_root)
pdf_dest = 'C:/Users/Darudayu/Desktop/hwp_1/pdfs_1'
hwp = win32.gencache.EnsureDispatch('HWPFrame.HwpObject')
print(hwp)
hwnd = win32gui.FindWindow(None, '빈 문서 1 - 한글')
print(hwnd)
win32gui.ShowWindow(hwnd, 0)
hwp.RegisterModule('FilePathCheckDLL', 'FilePathCheckerModule')

cnt = 0
for hwp_file in hwp_list[1704:]:
    e1 = cv2.getTickCount()
    cnt += 1
    print(f'converting... {cnt}/{len(hwp_list)}')
    print(hwp_file)
    hwp.Open(f'{hwp_root}/{hwp_file}')
    hwp.HParameterSet.HFileOpenSave.filename = f'{pdf_dest}/{hwp_file.split(".")[0]}.pdf'
    hwp.HParameterSet.HFileOpenSave.Format = "PDF"
    hwp.HAction.Execute("FileSaveAs_S", hwp.HParameterSet.HFileOpenSave.HSet)

    e2 = cv2.getTickCount()
    print(f'Time taken: {(e2-e1)/cv2.getTickFrequency()} seconds')

hwp.Quit()
del hwp
del win32