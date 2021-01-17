class PngPhoto:
    """
    Класс для png фотографий
    PhotoName - имя фото
    PhotoSize - размер фото в условных единицах
    PhotoType - для класса PngPhoto всегда png
    """
    def __init__(self, name, size):
        self.PhotoName = name
        self.PhotoSize = size
        self.PhotoType = "png"


class JpgPhoto:
    """
    Класс для jpg фотографий
    PhotoName - имя фото
    PhotoSize - размер фото в условных единицах
    PhotoType - для класса JpgPhoto всегда jpg
    """
    def __init__(self, name, size):
        self.PhotoName = name
        self.PhotoSize = size
        self.PhotoType = "jpg"


def elimination_of_noise(photo):
    """ Преобразование 1-в-1 без изменения типа объекта. """
    photo.PhotoName += "_no_noise"
    return photo


def blur(photo):
    """ Преобразование 1-в-1 с изменением типа объектов. """

    if photo.PhotoType == "jpg":
        constructor = PngPhoto
    else:
        constructor = JpgPhoto

    return constructor(photo.PhotoName + "_no_blur", photo.PhotoSize)


def HDR(photos):
    """
    Преобразование n-в-1 без изменения типа объекта.
    (не очень уверена насчет списка во входных данных)
    """
    new_name = ""
    new_size = 0
    for i in range(len(photos)):
        new_name += photos[i].PhotoName
        new_size += photos[i].PhotoSize

    if photos[0].PhotoType == "jpg":
        new_photo = JpgPhoto(new_name, new_size)
    else:
        new_photo = PngPhoto(new_name, new_size)

    return new_photo


def slicing(photo, n):
    """
    Преобразование 1-в-n без изменения типа объекта.
    """
    photos = []

    if photo.PhotoType == "jpg":
        constructor = JpgPhoto
    else:
        constructor = PngPhoto

    for i in range(n):
        photos.append(constructor(photo.PhotoName + str(i), photo.PhotoSize / n))

    return photos
