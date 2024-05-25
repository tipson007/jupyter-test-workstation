import boto3

def describe_snapshots(ec2_client):
    try:
        response = ec2_client.describe_snapshots(OwnerIds=['self'])
        return response['Snapshots']
    except Exception as e:
        print(f"Error fetching snapshots: {e}")
        return []

def print_snapshots(snapshots):
    for snapshot in snapshots:
        volume_id = snapshot.get('VolumeId')
        if volume_id:
            print(f"Snapshot ID: {snapshot['SnapshotId']}, Volume ID: {volume_id}")

def delete_snapshots(ec2_client, snapshots):
    for snapshot in snapshots:
        volume_id = snapshot.get('VolumeId')
        if volume_id:
            snapshot_id = snapshot['SnapshotId']
            try:
                print(f"Deleting Snapshot ID: {snapshot_id}, Volume ID: {volume_id}")
                response = ec2_client.delete_snapshot(SnapshotId=snapshot_id)
                print(f"Deleted Snapshot ID: {snapshot_id}: {response}")
            except Exception as e:
                print(f"Error deleting Snapshot ID: {snapshot_id}: {e}")

def main():
    ec2_client = boto3.client('ec2')
    snapshots = describe_snapshots(ec2_client)
    print_snapshots(snapshots)
    delete_snapshots(ec2_client, snapshots)

if __name__ == "__main__":
    main()