import time

def read_data(s):
    return [int(x) for x in s]

data = read_data(open('../data/input16').read().strip())

print(len(data))
# data = read_data("12345678")
# data = read_data("80871224585914546619083218645595")
# data = read_data("19617804207202209144916044189917")

arr = data.copy()

def fft(arr, n_phases=100):
    arr = arr.copy()
    start_time = time.time()

    for _ in range(n_phases):
        new_arr = []
        for i in range(1, len(arr) + 1):
            value = 0
            
            idx = i - 1
            add = True
            while idx < len(arr):
                diff = sum(arr[idx : idx+i])
                if add:
                    value += diff
                else:
                    value -= diff
                add = not add
                idx += 2 * i

            new_arr.append(int(str(value)[-1]))

        arr = new_arr

    print("{:.2f}s".format(time.time() - start_time))

    return arr

def fft_inplace(arr, n_phases=100):
    arr = arr.copy()
    start_time = time.time()

    for _ in range(n_phases):
        for i in range(len(arr)):
            inc = i + 1
            value = 0
            
            idx = inc - 1
            add = True
            while idx < len(arr):
                diff = sum(arr[idx : idx+inc])
                if add:
                    value += diff
                else:
                    value -= diff
                add = not add
                idx += 2 * inc

            arr[i] = int(str(value)[-1])

            # if i % 500 == 0:
            #     print(i, end='..', flush=True)
        # print(arr[:8])
        # print(''.join(str(x) for x in arr))

    print("{:.2f}s".format(time.time() - start_time))

    return arr

def fft_inplace_faster(arr, n_phases=100):
    arr = arr.copy()
    start_time = time.time()

    for p in range(n_phases):
        for i in range(len(arr)):
            inc = i + 1
            value = 0
            
            idx = inc - 1
            for j in range(inc):
                value += sum(arr[idx+j::4*inc])

            idx += 2 * inc
            for j in range(inc):
                value -= sum(arr[idx+j::4*inc])

            arr[i] = int(str(value)[-1])

    print("{:.2f}s".format(time.time() - start_time))

    return arr

# part 1
print(''.join(str(x) for x in fft_inplace(arr)[:8]))
# print(''.join(str(x) for x in fft_inplace_faster(arr)[:8]))
# fft_inplace(arr, n_phases=5)

# part 2
# big_arr = arr * 2
# offset = int(''.join(str(x) for x in big_arr[:7]))
# print(offset)

# big_arr = fft_inplace(big_arr, n_phases=100)

# print(''.join(str(x) for x in big_arr[offset : offset+7]))