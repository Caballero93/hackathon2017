from control import Control

def worker(msg):
    print('Worker doing its job, message is {} ...' \
          .format(msg))

if __name__ == '__main__':
    cntrl = Control()

    for data in cntrl.get_data():
        worker(data)
