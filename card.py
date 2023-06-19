def main():
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfgen.canvas import Canvas
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase.pdfmetrics import registerFont
    from reportlab.lib.pagesizes import A4
    canv = Canvas('text-on-image.pdf',pagesize=A4)
    img = ImageReader('Wow.jpg')
    registerFont(TTFont('arial','arial.ttf'))
 
    #now begin the work
    x = 113
    y = 217
    w = 103
    h = 119
    canv.drawImage(img,x,y,w,h,anchor='sw',anchorAtXY=True,showBoundary=False)
    canv.setFont('arial',14)
    canv.setFillColor((1,0,0)) #change the text color
    canv.drawCentredString(x+w*0.5,y+h*0.5,'On Top')
    canv.save()

if __name__=='__main__':
    main()