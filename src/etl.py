import os
import s3fs
from src.date_time import parse_str_date, split_date, next_day, str_day_of_year
from fsspec.asyn import FSTimeoutError
from tenacity import retry, stop_after_attempt, wait_fixed


@retry(stop=stop_after_attempt(10), 
       wait=wait_fixed(60),
       before_sleep=lambda x: print(f'TimeoutError. Retrying after 60 seconds.'),
       retry_error_callback=lambda x: (print('Max attempts reached. Exiting...'), exit()))
def get_from_remote(fs, remote_path, local_path, recursive=True):
    fs.get(remote_path, local_path, recursive=recursive)


def main():
    local_bucket = 'data'
    remote_bucket = 'noaa-goes16'
    product = 'GLM-L2-LCFA'
    fs = s3fs.S3FileSystem(anon=True)

    dt = parse_str_date('2019-01-01')
    end_date = parse_str_date('2019-01-02')

    print('ETL started')
    while dt <= end_date:
        year, _, _ = split_date(dt)
        year = str(year)
        day_of_year = str_day_of_year(dt)

        path = os.path.join(product, year, day_of_year)
        remote_path = os.path.join(remote_bucket, path)
        local_path = os.path.join(local_bucket, path) + '/'
        try:
            get_from_remote(fs, remote_path, local_path)
        except FSTimeoutError:
            pass
        print(f'Extracted data from {dt}')
        dt = next_day(dt)
    print('ETL finished')
    
    
if __name__ == '__main__':
    main()
