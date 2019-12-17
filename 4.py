mi = 353096
ma = 843212

def num_to_run(num):
    s = str(num)

    run = []
    curr = None
    for c in s:
        if curr is None:
            curr = (c, 1)
        elif curr[0] == c:
            curr = (c, curr[1]+1)
        else:
            run.append(curr)
            curr = (c, 1)
         
    run.append(curr)

    return run

def non_desc(run):
    prev_c = None
    for c, _ in run:
        if prev_c is not None and ord(c) < ord(prev_c):
            return False
        prev_c = c

    return True

def has_double(run):
    for _, count in run:
        if count > 1:
            return True

    return False

def has_better_double(run):
    for _, count in run:
        if count == 2:
            return True

    return False

n_good = 0
for i in range(mi, ma+1):
    run = num_to_run(i)
    if non_desc(run) and has_double(run):
        n_good += 1

print(n_good)

# ans2
n_good = 0
for i in range(mi, ma+1):
    run = num_to_run(i)
    if non_desc(run) and has_better_double(run):
        n_good += 1

print(n_good)