import subprocess
import sys
import boto3

def check_disk_space():
    print("Checking disk space")
    p1 = subprocess.Popen(["df", "-h"], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(
        ["awk", "{print $5}"], stdin=p1.stdout, stdout=subprocess.PIPE
    )
    p3 = subprocess.Popen(
        ["egrep", "9[0-9]%"], stdin=p2.stdout, stdout=subprocess.PIPE
    )
    out, er = p3.communicate()
    if out:
        print("disk space is running low")
        return True
    return

def send_email(host_name):
    to_addresses = {
        'ToAddresses': ["support@openhealthcare.org.uk"]
    }
    print(f"emailing {to_addresses['ToAddresses']}")
    from_address = "support@openhealthcare.org.uk"
    subject = f"SUDGT Disk Space Alert on {host_name}: Action Required"
    message_body = " ".join(
        [
            "Routine system check on SUDGT has detected a volume with > 90%",
            "disk usage. Please log in and investigate.",
        ]
    )
    message = {
        'Body': {
            'Text': {
                'Charset': 'UTF-8',
                'Data': message_body
            }
        },
        'Subject': {
            'Charset': 'UTF-8',
            'Data': subject
        }
    }
    client = boto3.client('ses')
    client.send_email(
        Destination=to_addresses,
        Message=message,
        Source=from_address
    )

if __name__ == "__main__":
    try:
        _, host_name = sys.argv
        if check_disk_space():
            send_email(host_name)
    except Exception as e:
        print(f"errored with {e}")
