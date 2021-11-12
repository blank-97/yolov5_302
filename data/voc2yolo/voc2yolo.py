# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET

sets = ['train', 'val', 'test']
classes = ['airplane', 'airport', 'baseballfield', 'basketballcourt', 'bridge', 'chimney', 'dam',
        'Expressway-Service-area', 'Expressway-toll-station', 'golffield', 'groundtrackfield', 'harbor',
        'overpass', 'ship', 'stadium', 'storagetank', 'tenniscourt', 'trainstation', 'vehicle', 'windmill']


def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h


def convert_annotation(image_id):
    in_file = open('/home/hkx/hkx_models/datasets/dior/Annotations/%s.xml' % (image_id), encoding='UTF-8')
    out_file = open('/home/hkx/hkx_models/datasets/dior/labels/%s.txt' % (image_id), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    for obj in root.iter('object'):
        if obj.find('difficult'):
            difficult = obj.find('difficult').text
        else:
            difficult = '0'
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1 or w <= 0 or h <= 0:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        b1, b2, b3, b4 = b
        # 标注越界修正
        b2 = min(b2, w)
        b4 = min(b4, h)
        b = (b1, b2, b3, b4)
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


if __name__ == '__main__':
    for image_set in sets:
        image_ids = open('/home/hkx/hkx_models/datasets/dior/ImageSets/%s.txt' % (image_set)).read().strip().split()
        list_file = open('/home/hkx/hkx_models/datasets/dior/%s.txt' % (image_set), 'w')
        for image_id in image_ids:
            list_file.write('/home/hkx/hkx_models/datasets/dior/images/%s.jpg\n' % (image_id))
            convert_annotation(image_id)
        list_file.close()
