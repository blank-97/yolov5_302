# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET

sets = ['train', 'val', 'test']
# classes = ['ship', 'aircraft carrier', 'warcraft', 'merchant ship', 'Nimitz', 'Enterprise', 'Arleigh Burke',
#            'WhidbeyIsland', 'Perry', 'Sanantonio', 'Ticonderoga', 'Kitty Hawk', 'Kuznetsov', 'Abukuma',
#            'Austen', 'Tarawa', 'Blue Ridge', 'Container', 'OXo', 'Car carrier', 'Hovercraft', 'yacht',
#            'CntShip', 'Cruise', 'submarine', 'lute', 'Medical', 'Car carrier', 'Ford-class', 'Midway-class',
#            'Invincible-class']
classes = ['100000001', '100000002', '100000003', '100000004', '100000005', '100000006', '100000007', '100000008',
           '100000009', '100000010', '100000011', '100000012', '100000013', '100000014', '100000015', '100000016',
           '100000017', '100000018', '100000019', '100000020', '100000022', '100000024', '100000025', '100000026',
           '100000027', '100000028', '100000029', '100000030', '100000031', '100000032', '100000033'
           ]


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
    in_file = open('/home/hkx/hkx_models/datasets/hrsc2016/Annotations/%s.xml' % (image_id), encoding='UTF-8')
    out_file = open('/home/hkx/hkx_models/datasets/hrsc2016/labels/%s.txt' % (image_id), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    w = int(root.find('Img_SizeWidth').text)
    h = int(root.find('Img_SizeHeight').text)
    root_n = root.find('HRSC_Objects')
    for obj in root_n.iter('HRSC_Object'):
        if obj.find('difficult'):
            difficult = obj.find('difficult').text
        else:
            difficult = '0'
        cls = obj.find('Class_ID').text
        if cls not in classes or int(difficult) == 1 or w <= 0 or h <= 0:
            continue
        cls_id = classes.index(cls)
        b = (float(obj.find('box_xmin').text), float(obj.find('box_xmax').text), float(obj.find('box_ymin').text),
             float(obj.find('box_ymax').text))
        b1, b2, b3, b4 = b
        # 标注越界修正
        b2 = min(b2, w)
        b4 = min(b4, h)
        b = (b1, b2, b3, b4)
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


if __name__ == '__main__':
    for image_set in sets:
        image_ids = open('/home/hkx/hkx_models/datasets/hrsc2016/ImageSets/%s.txt' % (image_set)).read().strip().split()
        list_file = open('/home/hkx/hkx_models/datasets/hrsc2016/%s.txt' % (image_set), 'w')
        for image_id in image_ids:
            list_file.write('/home/hkx/hkx_models/datasets/hrsc2016/images/%s.bmp\n' % (image_id))
            convert_annotation(image_id)
        list_file.close()
