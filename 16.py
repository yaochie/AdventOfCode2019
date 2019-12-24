import time

def read_data(s):
    return [int(x) for x in s]

data = read_data(open('../data/input16').read().strip())

print(len(data))
# data = read_data("12345678")
# data = read_data("80871224585914546619083218645595")
# data = read_data("19617804207202209144916044189917")

arr = data.copy()

def format_arr(arr):
    return ''.join(str(x) for x in arr)

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

def fft_inplace(arr, n_phases=100, verbose=False):
    arr = arr.copy()
    start_time = time.time()

    if verbose:
        print(format_arr(arr))
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

        if verbose:
            print(format_arr(arr))

    print("{:.2f}s".format(time.time() - start_time))

    return arr

def fft_end(arr, start_idx, n_phases=100, verbose=False):
    """
    We can quickly compute values in the last half of the array,
    since they just follow the following recursion:

    new[-1] = old[-1]
    new[i] = (old[i] + new[i+1]) % 10
    """
    if start_idx < len(arr) // 2 + 1:
        raise ValueError

    arr_end = arr[start_idx:].copy()

    if verbose:
        print(format_arr(arr_end))

    for p in range(n_phases):
        print(p, end='..', flush=True)
        for j in range(len(arr_end) - 2, -1, -1):
            arr_end[j] = (arr_end[j] + arr_end[j+1]) % 10
        
        if verbose:
            print(format_arr(arr_end))

    print()
    return arr_end

# part 1
arr_100 = fft_inplace(arr)
print(format_arr(arr_100[:8]))

print()

# part 2
print("part 2")

offset = int(''.join(str(x) for x in arr[:7]))
print("Offset:", offset)
print("fraction:", offset / (len(arr) * 10000))

# our offset 
big_arr = arr * 10000

arr_end = fft_end(big_arr, offset)
print(format_arr(arr_end[:8]))