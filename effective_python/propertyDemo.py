##利用property实现漏桶算法
from datetime import timedelta, datetime


class Bucket(object):
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.max_quota = 0  # 记录周期的初始配额
        self.quota_consumed = 0

    def __repr__(self):
        return ('Bucket(max_quota=%d,quota_consumed=%d)' % (self.max_quota, self.quota_consumed))

    @property
    def quota(self):
        return self.max_quota - self.quota_consumed

    @quota.setter
    def quota(self, amount):
        delta = self.max_quota - amount
        if amount == 0:
            self.quota_consumed = 0
            self.max_quota = 0
        elif delta < 0:
            assert self.quota_consumed == 0
            self.max_quota = amount
        else:
            assert self.max_quota >= self.quota_consumed
            self.quota_consumed += delta


def fill(bucket, amount):
    now = datetime.now()
    if now - bucket.reset_time > bucket.period_delta:
        return False
    if bucket.quota - amount < 0:
        return False
    bucket.quota -= amount
    return True


def deduct(bucket, amount):
    now = datetime.now()
    if now - bucket.reset_time > bucket.period_delta:
        return False
    if bucket.quota - amount < 0:
        return False
    bucket.quota += amount
    return True


if __name__ == '__main__':
    bucket = Bucket(60)
    print('Initial', bucket)
    fill(bucket, 100)
    print('Filled', bucket)

    if deduct(bucket, 99):
        print('Had 99 quota')
    else:
        print('Not enough for 99 quota')
