import boto3

def delete_unattached_snapshots():
    ec2_client = boto3.client('ec2')

    response = ec2_client.describe_snapshots(OwnerIds=['self'])
    snapshots = response['Snapshots']

    unattached_snapshots = []
    for snapshot in snapshots:
        if 'fromSnapshotId' not in snapshot['Description']:
            unattached_snapshots.append(snapshot)

    for snapshot in unattached_snapshots:
        print(f"Snapshot ID: {snapshot['SnapshotId']}, Volume ID: {snapshot['VolumeId']}")
        response = input("Do you want to delete this snapshot? (yes/no): ").lower()
        if response == 'yes':
            try:
                ec2_client.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
                print(f"Snapshot {snapshot['SnapshotId']} deleted.")
            except Exception as e:
                print(f"An error occurred while deleting snapshot {snapshot['SnapshotId']}: {str(e)}")
        else:
            print(f"Snapshot {snapshot['SnapshotId']} skipped.")

if __name__ == "__main__":
    delete_unattached_snapshots()
