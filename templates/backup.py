import os
import subprocess
import sys
import shutil
from datetime import datetime

import boto3

BACKUP_DIRECTORY = "/home/ubuntu/backups"
BACKUP_TAR_NAME = "/home/ubuntu/backup.tgz"


def clean_old_backups():
    if os.path.exists(BACKUP_DIRECTORY):
        shutil.rmtree(BACKUP_DIRECTORY)
    os.makedirs(BACKUP_DIRECTORY)

def copy_project():
    shutil.copytree('/var/www/html/sudgt/', os.path.join(BACKUP_DIRECTORY, "files"))

def dump_database(db_name, db_user, db_password):
    print(f"Dumping db_name: {db_name}")
    db_backup = os.path.join(BACKUP_DIRECTORY, "db_backup.sql")
    command = "mysqldump --databases {} -u {} -p{} > {}"
    command = command.format(
        db_name, db_user, db_password, db_backup
    )

    print(f"Running: {command}")
    subprocess.check_call(command, shell=True)

    if not os.path.exists(db_backup):
        raise Exception(f"Database dump not saved for: {db_name}")


def tar_directory():
    if os.path.exists(BACKUP_TAR_NAME):
        os.remove(BACKUP_TAR_NAME)
    subprocess.check_call('tar czf {} --directory={} .'.format(
        BACKUP_TAR_NAME, BACKUP_DIRECTORY), shell=True
    )


def upload(bucket_name):
    """
    """
    today = datetime.now().strftime("%Y-%m-%d")
    backup_name = f"{today}-sudgt.tgz"
    s3 = boto3.resource("s3")
    s3.Bucket(bucket_name).upload_file(BACKUP_TAR_NAME, f"backups/{backup_name}")


def main(db_name, db_user, db_password, bucket_name):
    # remove and create the back up directory
    clean_old_backups()

    # copy /var/wwww/html/sudgt into the backups
    copy_project()

    # dump the database into backups
    dump_database(db_name, db_user, db_password)

    # tar the back ups
    tar_directory()

    # upload the backups
    upload(bucket_name)


if __name__ == "__main__":
    try:
        _, db_name, db_user, db_password, bucket_name = sys.argv
        main(db_name, db_user, db_password, bucket_name)
    except Exception as e:
        print(f"errored with {e}")
