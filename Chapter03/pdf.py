from pyPdf.pdf import PdfFileReader


def printMeta(filename):
    f = PdfFileReader(open(filename, 'rb'))
    info = f.getDocumentInfo()
    print("[*] PDF Metadata for:" + filename)
    for item in info:
        print("[+]", item, ":", info[item])


if __name__ == '__main__':
    printMeta("demo.pdf")
