# Standard Library
import os
import subprocess
import sys
from tkinter import Button, Label, Radiobutton, StringVar, Tk, filedialog, messagebox

# Third Party Library
from pypdf import PdfWriter
from send2trash import send2trash

dirname = os.path.dirname(__file__)
iDir = os.path.abspath(dirname)
root = Tk()
root.withdraw()


def files_reading():
    """
    ファイルの読み込み
    読み込まれたファイルのリストを返す
    """
    files_read = filedialog.askopenfilenames(title="開く", 
    filetypes=[("PDF file", "*.pdf")], 
    initialdir=iDir)

    return files_read


def checking(files_read):
    """
    読み込んだファイルのリストの結合前処理（存在の確認や並べ替えなど）
    処理後のリストを返す
    * 状況によりmergingに行かずにchecking段階で処理を終わらせる
    """
    files_found = ""
    for file_name in files_read:
        files_found = files_found + file_name + "\n"

    if files_read != "":  # ファイルが存在する場合
        reverse = messagebox.askquestion(
            "Pdf-merger",
            "現在の状態では以下の" + str(len(files_read)) + "個のファイルが以下の順番で結合されます：\n" + files_found + "\n逆順に並べ替えますか?",
        )

        if reverse == "yes":
            files_read = list(reversed(files_read))
        else:
            files_read = files_read

        files_found = ""
        for file_name in files_read:
            files_found = files_found + file_name + "\n"

        ok = messagebox.askokcancel(
            "Pdf-merger", "以下の" + str(len(files_read)) + "個のファイルを以下の順番で結合します：\n" + files_found + "\nよろしければ、OKを押してください。"
        )

        if ok:
            return files_read

        else:
            messagebox.showinfo("Pdf-merger", "キャンセルされました。\n最初からやり直してください。")
            root.destroy()
            sys.exit()

    else:
        messagebox.showerror("Pdf-merger", "データが選択されていません。\n最初からやり直してください。")
        root.destroy()
        sys.exit()


def merging(files_read):
    """
    結合の本体
    """
    pdf_file_merger = PdfWriter()
    for pdf in files_read:
        pdf_file_merger.append(pdf)

    file_name_save = filedialog.asksaveasfilename(
        title="結合したファイルを名前を付けて保存", 
        filetypes=[("PDF file", "*.pdf")], 
        initialdir=iDir
    )

    if file_name_save.rfind(".pdf") == -1:
        file_name_save = file_name_save + ".pdf"
        # 右から検索して.pdfが無かったら勝手に付け足す

    pdf_file_merger.write(file_name_save)
    pdf_file_merger.close()  # writer を閉じる

    return file_name_save


def option(files_read, file_name_save):
    """
    結合後のオプション機能
    """
    delete = messagebox.askquestion(
        "Pdf-merger",
        "結合に使用したPDFをゴミ箱に移動しますか？",
    )

    if delete == "yes":
        for file_name in files_read:
            file_name_delete = file_name.replace("/", "\\")  
            # get_short_path_name() に対応
            send2trash(file_name_delete)

    compress = messagebox.askquestion(
        "Pdf-merger",
        "結合後のPDFを圧縮しますか？（GhostScriptが必要）",
    )

    if compress == "yes":
        root_s = Tk()
        root_s.geometry('250x240')
        root_s.title("pdf-compressor")

        radio_var = StringVar(root_s)

        radio1 = Radiobutton(
            root_s,
            value="/default",
            variable=radio_var,
            text="/default"
        )
        radio1.pack()
        radio1.place(x=20, y=60)

        radio2 = Radiobutton(
            root_s,
            value="/screen",
            variable=radio_var,
            text="/screen"
        )
        radio2.pack()
        radio2.place(x=20, y=82)

        radio3 = Radiobutton(
            root_s,
            value="/ebook",
            variable=radio_var,
            text="/ebook"
        )
        radio3.pack()
        radio3.place(x=20, y=104)

        radio4 = Radiobutton(
            root_s,
            value="/printer",
            variable=radio_var,
            text="/printer"
        )
        radio4.pack()
        radio4.place(x=20, y=126)

        radio5 = Radiobutton(
            root_s,
            value="/prepress",
            variable=radio_var,
            text="/prepress"
        )
        radio5.pack()
        radio5.place(x=20, y=148)

        def btn_click():
            root_s.quit()
            root_s.destroy()

        label = Label(root_s, text="圧縮の設定を選んでください。")
        label.pack()
        label.place(x=20, y=10)

        button = Button(
            root_s,
            text="OK",
            command=btn_click
        )
        button.place(x=20, y=180)

        root_s.mainloop()

        print(radio_var.get())

        for file_name in files_read:
            pdf_file_name = file_name.replace(".pdf", "_compressed.pdf")
            subprocess.check_output(
                [
                    "gswin64c",
                    "-sDEVICE=pdfwrite",
                    "-dPDFSETTINGS=%s" % (radio_var.get()),
                    "-dBATCH",
                    "-dNOPAUSE",
                    "-dSAFER",
                    "-sOUTPUTFILE=%s" % (pdf_file_name,),
                    file_name,
                ]
            )

    messagebox.showinfo("Pdf-compressor", "処理が完了しました。")
    root.destroy()
    return
