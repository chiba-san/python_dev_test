from multiprocessing import Pool
import os
import time

BUFFER_SIZE = 512*512


def reading_worker(chunk_start, chunk_size, file_name):
    with open(file_name) as f:
        _share_sum = 0
        f.seek(chunk_start)
        lines = f.read(chunk_size).splitlines()
        for ln in lines:
            _share_sum += float(ln)
        return _share_sum


def get_chunks(file_name, size=BUFFER_SIZE):
    file_end = os.path.getsize(file_name)
    with open(file_name,'rb') as f:
        f.readline()
        chunk_end = f.tell()
        while True:
            chunk_start = chunk_end
            f.seek(size, 1)
            f.readline()
            chunk_end = f.tell()
            yield chunk_start, chunk_end - chunk_start
            if chunk_end > file_end:
                break


if __name__ == '__main__':

    share_sum = 0
    input_file_name = "input.txt"
    output_file_name = "output.txt"

    #clear output file
    with open(output_file_name, 'w'):
        pass

    print("reading started\n")
    start = time.time()

    with Pool(processes=os.cpu_count()) as pool:
        results = [pool.apply_async(reading_worker, (chunk_start, chunk_size, input_file_name)) for chunk_start, chunk_size in get_chunks(input_file_name)]
        for r in results:
            try:
                share_sum += r.get(timeout=1)
            except TimeoutError:
                print("We lacked patience and got a multiprocessing.TimeoutError")

    done = time.time()
    elapsed = done - start
    print("reading complete in {:.3f} sec\n".format(elapsed))
    print("shares sum = {:.3f}\n".format(share_sum))

    print("writing started\n")
    start = time.time()

    with open(output_file_name, "a") as wf:
        with open(input_file_name) as rf:
            rf.readline()
            for ln in rf:
                wf.write('{:.3f}\n'.format(float(ln)/share_sum))

    done = time.time()
    elapsed = done - start
    print("writing complete in {:.3f} sec\n".format(elapsed))
    print("output file size is {:.3f} Kb\n".format(os.path.getsize(output_file_name)/1024))