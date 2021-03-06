from PIL import Image, ImageDraw, ImageFilter
def mirikora2():
    im1 = Image.open('static/picture/colla/image.png')
    im2 = Image.open('static/picture/colla/コラ.png')
    img_resize = im2.resize(im1.size)
    print(im2.size)
    im1.paste(img_resize,(0,0),img_resize)
    im1.save('static/picture/colla/new.png', quality=95)


def ppp():
    im1 = Image.open('static/picture/colla/image.png')
    im2 = Image.open('static/picture/colla/PPP.png')
    img_resize = im2.resize(im1.size)
    print(im2.size)
    im1.paste(img_resize,(0,0),img_resize)
    im1.save('static/picture/colla/new.png', quality=95)

def deresute_kora():
    im1 = Image.open('static/picture/colla/image.png')
    im2 = Image.open('static/picture/colla/デレステコラ.png')
    img_resize = im2.resize(im1.size)
    print(im2.size)
    im1.paste(img_resize,(0,0),img_resize)
    im1.save('static/picture/colla/new.png', quality=95)


def nhk():
    im1 = Image.open('static/picture/colla/image.png')
    im2 = Image.open('static/picture/colla//nhk.png')
    img_resize = im2.resize((int(im1.size[0]/3.7),int(im1.size[1]/3)))
    print(im1.size)
    print(img_resize.size)
    im1.paste(img_resize,(int(img_resize.size[0]*2.8),int(img_resize.size[1]*2)),img_resize)
    im1.save('static/picture/colla/new.png', quality=95)


def bazirisuku():
    im1 = Image.open('static/picture/colla/image.png')
    im2 = Image.open('static/picture/colla//baji.png')
    img_resize = im2.resize((int(im1.size[0]/1.5),int(im1.size[1]/1.4)))
    print(im1.size)
    print(img_resize.size)
    im1.paste(img_resize,(int(img_resize.size[0]/3.4),int(img_resize.size[1]/3)),img_resize)
    im1.save('static/picture/colla/new.png', quality=95)

def out():
    im1 = Image.open('static/picture/colla/image.png')
    im2 = Image.open('static/picture/colla/all_out.png')
    img_resize = im2.resize((int(im1.size[0]/2),int(im1.size[1]/2)))
    print(im1.size)
    print(img_resize.size)
    im1.paste(img_resize,(int(img_resize.size[0]/2),int(img_resize.size[1])),img_resize)
    im1.save('static/picture/colla/new.png', quality=95)
