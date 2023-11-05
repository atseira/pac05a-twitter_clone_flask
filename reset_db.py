from app import create_app, db
from init_db import init_db

app = create_app()

def delete_all_files_in_minio():
    with app.app_context():
        minio_client = app.minio_client
        bucket_name = 'klonx-bucket'

        # Get the list of all objects in the bucket
        objects_to_delete = minio_client.list_objects(bucket_name)

        # Iterate over the objects and delete them
        for obj in objects_to_delete:
            print(f"Deleting {obj.object_name}...")
            minio_client.remove_object(bucket_name, obj.object_name)

        print("All files in MinIO deleted successfully.")

def reset_db():
    with app.app_context():
        # Drop all tables
        db.drop_all()
        # Initialize database
        init_db()
        # Delete all files in Minio
        delete_all_files_in_minio()

if __name__ == '__main__':
    reset_db()
