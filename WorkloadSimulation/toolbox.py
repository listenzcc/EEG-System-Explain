import struct


def pack(arr):
    return struct.pack('=%sf' % arr.size, *arr.flatten('F'))


def unpack(buffer, size):
    return struct.unpack('=%sf' % size, buffer)


if __name__ == '__main__':
    import numpy as np

    print('\n>> It is a demo of pack and unpack an array using Python struct package')
    num_channels = 100
    num_times = 40
    size = num_channels * num_times

    arr = np.random.rand(size)
    print('>> Generated arr of {}: {} ({}+-{})'.format(
        arr.shape, type(arr), np.mean(arr), np.std(arr)))

    buffer = pack(arr)
    print('>> Packed buffer of {}: {}'.format(len(buffer), type(buffer)))

    rec = unpack(buffer, size)

    print('>> The max diff of unpack is {}'.format(np.max(np.array(rec) - arr)))
    print('>> Done.')
