import selenium
import json

# Use selenium to add projects individually to squarespace
# (since squarespace doesn't have an API)

# 1. Go to squarespace
# 2. Login
# 3. Go to projects
# 4. Add project
# 5. Fill out project details
# 6. Save project
# 7. Repeat steps 4-6 for each project
# 8. Logout


class SquareSpaceProjectUploader:
    def __init__(self):
        pass

    def upload_project(self):
        pass

    def get_projects(self):
        """return list of projects each with structure

        {
            "id": 32,
            "tag": "Portrait",
            "filename": "brbawalt.JPG",
            "portrait_name": "Walt",
            "date": "2014-01-01",
            "s3_drawing_private_url": "https://sketchyactivitys3.s3.amazonaws.com/media/drawings/brbawalt.JPG?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAWDTAGLLHXMOED4H7%2F20240517%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20240517T105152Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=ed27946195eba2927be8806b040e7b8dc4d9f6fb991603ab29f3e79e2b742f0a",
            "s3_copied_smaller_drawing_private_url": "https://sketchyactivitys3.s3.amazonaws.com/media/copied_smaller_drawings/brbawalt.JPG?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAWDTAGLLHXMOED4H7%2F20240517%2Fus-east-2%2Fs3%2Faws4_request&X-Amz-Date=20240517T105152Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=bf02e5bbc1888160bd3a91404467c981784f0d39978690b65bd30c34b15fc3b0"
        }
        """
        with open("porfolio.json", "r") as f:
            return json.load(f)
